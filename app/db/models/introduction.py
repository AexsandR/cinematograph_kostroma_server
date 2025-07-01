from sqlalchemy import Column, DateTime, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from ..db_session import SqlAlchemyBase
from datetime import datetime


class Introduction(SqlAlchemyBase):
    __tablename__ = "Introductions"
    id: int = Column(Integer, primary_key=True, autoincrement=True)
    id_img: int = Column(Integer, ForeignKey("Media.id"), nullable=True)
    id_audio: int = Column(Integer, ForeignKey("Media.id"), nullable=True)
