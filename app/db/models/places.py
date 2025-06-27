from sqlalchemy import Column, DateTime, Integer, String, Float, ForeignKey 
from ..db_session import SqlAlchemyBase
from datetime import datetime


class Places(SqlAlchemyBase):
    __tablename__ = "Places"
    id: int = Column(Integer, primary_key=True, autoincrement=True)
    name_place: str = Column(String(300), unique=True, nullable=False)
    description: str = Column(String(500), nullable=True)
    latitude: float = Column(Float, nullable=True)
    longitude: float = Column(Float, nullable=True)
    radius: float = Column(Float, nullable=True)
    img_id: int = Column(Integer, ForeignKey("Images.id"), nullable=True)
    last_modification: datetime = Column(DateTime, nullable=True, default=datetime.now)
