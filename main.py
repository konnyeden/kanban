from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Depends
from fastapi import Body
from sqlalchemy.orm import Session
from typing import List
from database import SessionLocal, engine
from .models import Board, BoardColumn, Card
from crud import (
    get_boards, create_board, update_board, delete_board,
    get_columns, create_column, update_column, delete_column,
    get_cards, create_card, update_card, delete_card,
)
from .schemas import BoardOut, ColumnCreate, CardCreate, CardUpdate, BoardCreate, BoardUpdate
from .ws_manager import manager

# Create tables on startup (idempotent)
def init_db():
    import sqlalchemy
    from .database import engine, Base
    Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.on_event("startup")
def on_startup():
    from .database import Base, engine
    Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Boards
@app.get("/boards", response_model=List[BoardOut])
def boards(db: Session = Depends(get_db)):
    return get_boards(db)

@app.post("/boards", response_model=BoardOut)
def create_board_endpoint(payload: BoardCreate, db: Session = Depends(get_db)):
    name = payload.name
    board = create_board(db, name=name)
    # notify via websocket (best-effort)
    import asyncio
    asyncio.create_task(manager.broadcast(board.id, {"event": "board_created", "data": {"id": board.id, "name": board.name}}))
    return board
@app.put("/boards/{board_id}")
def update_board_endpoint(board_id: int, payload: BoardUpdate, db: Session = Depends(get_db)):
    name = payload.name
    board = update_board(db, board_id, name=name)
    if not board:
        return {"detail": "Not found"}
    asyncio = __import__("asyncio")
    asyncio.create_task(manager.broadcast(board_id, {"event": "board_updated", "data": {"id": board.id, "name": board.name}}))
    return {"id": board.id, "name": board.name}

@app.delete("/boards/{board_id}")
def delete_board_endpoint(board_id: int, db: Session = Depends(get_db)):
    ok = delete_board(db, board_id)
    if ok:
        import asyncio
        asyncio.get_event_loop().create_task(manager.broadcast(board_id, {"event": "board_deleted", "data": {"id": board_id}}))
        return {"status": "deleted"}
    return {"error": "not_found"}


# Columns
@app.get("/boards/{board_id}/columns")
def get_columns_endpoint(board_id: int, db: Session = Depends(get_db)):
    return get_columns(db, board_id)

@app.post("/boards/{board_id}/columns")
def create_column_endpoint(board_id: int, payload: ColumnCreate, db: Session = Depends(get_db)):
    # payload is validated by Pydantic
    name = payload.name
    position = payload.position
    col = create_column(db, board_id, name, position)
    return col

@app.put("/boards/{board_id}/columns/{column_id}")
def update_column_endpoint(board_id: int, column_id: int, payload: ColumnCreate, db: Session = Depends(get_db)):
    name = payload.name
    position = payload.position
    col = update_column(db, board_id, column_id, name=name, position=position)
    if not col:
        return {"error": "not_found"}
    return col

@app.delete("/boards/{board_id}/columns/{column_id}")
def delete_column_endpoint(board_id: int, column_id: int, db: Session = Depends(get_db)):
    ok = delete_column(db, board_id, column_id)
    return {"deleted": ok}


# Cards
@app.get("/boards/{board_id}/cards")
def get_cards_endpoint(board_id: int, db: Session = Depends(get_db)):
    return get_cards(db, board_id)

@app.post("/boards/{board_id}/cards")
def create_card_endpoint(board_id: int, payload: CardCreate, db: Session = Depends(get_db)):
    title = payload.title
    description = payload.description
    column_id = payload.column_id
    position = payload.position
    card = create_card(db, board_id, column_id, title, description, position)
    return card
@app.put("/boards/{board_id}/cards/{card_id}")
def update_card_endpoint(board_id: int, card_id: int, payload: CardUpdate, db: Session = Depends(get_db)):
    title = payload.title
    description = payload.description
    column_id = payload.column_id
    position = payload.position
    card = update_card(db, board_id, card_id, title=title, description=description, column_id=column_id, position=position)
    if not card:
        return {"error": "not_found"}
    return card

@app.delete("/boards/{board_id}/cards/{card_id}")
def delete_card_endpoint(board_id: int, card_id: int, db: Session = Depends(get_db)):
    ok = delete_card(db, board_id, card_id)
    return {"deleted": ok}


# WebSocket for real-time updates per board
@app.websocket("/ws/boards/{board_id}")
async def websocket_board(websocket: WebSocket, board_id: int):
    await manager.connect(board_id, websocket)
    try:
        while True:
            # keep connection alive; no client messages required for MVP
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(board_id, websocket)
