from sqlalchemy import Column, DateTime, Integer, String, Float, ForeignKey
from ..db_session import SqlAlchemyBase
from datetime import datetime
from sqlalchemy.orm import relationship


class Places(SqlAlchemyBase):
    __tablename__ = "Places"
    id: int = Column(Integer, primary_key=True, autoincrement=True)
    name_place: str = Column(String(300), nullable=False)
    latitude: float = Column(Float, nullable=False)
    longitude: float = Column(Float, nullable=False)
    radius: float = Column(Float, nullable=False, default=25)
    fact_id: int = Column(Integer, ForeignKey("Media.id"), nullable=False)
    id_distorted_frame: int = Column(Integer, ForeignKey("Media.id"), nullable=False)
    id_orig_frame: int = Column(Integer, ForeignKey("Media.id"), nullable=False)
    id_video: int = Column(Integer, ForeignKey("Media.id"), nullable=False)
    id_frame_text: int = Column(Integer, ForeignKey("Media.id"), nullable=False)
    last_modification: datetime = Column(DateTime, nullable=False, default=datetime.now)
    id_question: int = Column(Integer, ForeignKey("Questions.id"), nullable=False)
    films = relationship(
        "Films",
        secondary="film_place_association",
        back_populates="places"
    )
