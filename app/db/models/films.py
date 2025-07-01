from sqlalchemy import Column, DateTime, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from ..db_session import SqlAlchemyBase
from datetime import datetime


class Films(SqlAlchemyBase):
    __tablename__ = "Films"
    id: int = Column(Integer, primary_key=True, autoincrement=True)
    name: str = Column(String(150), unique=True, nullable=False)
    img_id: int = Column(Integer, ForeignKey("Media.id"), nullable=False)
    id_introduction: int = Column(Integer, ForeignKey("ImgWithAudios.id"), nullable=True)
    id_conclusion: int = Column(Integer, ForeignKey("ImgWithAudios.id"), nullable=True)
    last_modification: datetime = Column(DateTime, nullable=False, default=datetime.now)
    places = relationship(
        "Places",
        secondary="film_place_association",
        back_populates="films"
    )
