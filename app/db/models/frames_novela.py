from sqlalchemy import Column, Integer, ForeignKey, LargeBinary, String
from ..db_session import SqlAlchemyBase
from sqlalchemy.orm import relationship


class FramesNovela(SqlAlchemyBase):
    __tablename__ = "FramesNovela"
    id: int = Column(Integer, primary_key=True, autoincrement=True)
    bin_data: bytes = Column(LargeBinary, nullable=True)
    type: str = Column(String, nullable=True)
