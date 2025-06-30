from sqlalchemy import Column, Integer, BOOLEAN, LargeBinary, String
from ..db_session import SqlAlchemyBase


class Questions(SqlAlchemyBase):
    __tablename__ = "Questions"
    id: int = Column(Integer, primary_key=True, autoincrement=True)
    question: str = Column(String(500), nullable=False)
    answer1: str = Column(String(300), nullable=False)
    answer2: str = Column(String(300))
    answer3: str = Column(String(300))
    answer4: str = Column(String(300))
