from sqlalchemy.orm import Session
from .models import Board, BoardColumn, Card
from .schemas import BoardOut, ColumnOut, CardOut


def get_boards(db: Session):
    return db.query(Board).all()


def get_board(db: Session, board_id: int):
    return db.query(Board).filter(Board.id == board_id).first()


def create_board(db: Session, name: str) -> Board:
    board = Board(name=name)
    db.add(board)
    db.commit()
    db.refresh(board)
    return board


def update_board(db: Session, board_id: int, name: str):
    board = get_board(db, board_id)
    if not board:
        return None
    board.name = name
    db.commit()
    db.refresh(board)
    return board


def delete_board(db: Session, board_id: int) -> bool:
    board = get_board(db, board_id)
    if not board:
        return False
    db.delete(board)
    db.commit()
    return True


def get_columns(db: Session, board_id: int):
    return db.query(BoardColumn).filter(BoardColumn.board_id == board_id).order_by(BoardColumn.position).all()


def create_column(db: Session, board_id: int, name: str, position: int) -> BoardColumn:
    col = BoardColumn(board_id=board_id, name=name, position=position)
    db.add(col)
    db.commit()
    db.refresh(col)
    return col


def update_column(db: Session, board_id: int, column_id: int, name: str | None = None, position: int | None = None):
    col = db.query(BoardColumn).filter(BoardColumn.board_id == board_id, BoardColumn.id == column_id).first()
    if not col:
        return None
    if name is not None:
        col.name = name
    if position is not None:
        col.position = position
    db.commit()
    db.refresh(col)
    return col


def delete_column(db: Session, board_id: int, column_id: int) -> bool:
    col = db.query(BoardColumn).filter(BoardColumn.board_id == board_id, BoardColumn.id == column_id).first()
    if not col:
        return False
    db.delete(col)
    db.commit()
    return True


def get_cards(db: Session, board_id: int):
    return db.query(Card).filter(Card.board_id == board_id).order_by(Card.position).all()


def create_card(db: Session, board_id: int, column_id: int, title: str, description: str | None, position: int) -> Card:
    card = Card(board_id=board_id, column_id=column_id, title=title, description=description, position=position)
    db.add(card)
    db.commit()
    db.refresh(card)
    return card


def update_card(db: Session, board_id: int, card_id: int, title=None, description=None, column_id=None, position=None):
    card = db.query(Card).filter(Card.id == card_id, Card.board_id == board_id).first()
    if not card:
        return None
    if title is not None:
        card.title = title
    if description is not None:
        card.description = description
    if column_id is not None:
        card.column_id = column_id
    if position is not None:
        card.position = position
    db.commit()
    db.refresh(card)
    return card


def delete_card(db: Session, board_id: int, card_id: int) -> bool:
    card = db.query(Card).filter(Card.id == card_id, Card.board_id == board_id).first()
    if not card:
        return False
    db.delete(card)
    db.commit()
    return True
