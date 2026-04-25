from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base


class Board(Base):
    __tablename__ = 'boards'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

    columns = relationship("BoardColumn", back_populates="board", cascade="all, delete-orphan")
    cards = relationship("Card", back_populates="board", cascade="all, delete-orphan")


class BoardColumn(Base):
    __tablename__ = 'columns'
    id = Column(Integer, primary_key=True)
    board_id = Column(Integer, ForeignKey('boards.id'), nullable=False)
    name = Column(String, nullable=False)
    position = Column(Integer, nullable=False)

    board = relationship("Board", back_populates="columns")
    cards = relationship("Card", back_populates="column", cascade="all, delete-orphan")


class Card(Base):
    __tablename__ = 'cards'
    id = Column(Integer, primary_key=True)
    board_id = Column(Integer, ForeignKey('boards.id'), nullable=False)
    column_id = Column(Integer, ForeignKey('columns.id'), nullable=False)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    position = Column(Integer, nullable=False)

    board = relationship("Board", back_populates="cards")
    column = relationship("BoardColumn", back_populates="cards")
