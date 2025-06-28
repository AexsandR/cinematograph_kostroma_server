from sqlalchemy import Column, Integer, ForeignKey, LargeBinary, String
from ..db_session import SqlAlchemyBase


class Images(SqlAlchemyBase):
    __tablename__ = "Images"
    id: int = Column(Integer, primary_key=True, autoincrement=True)
    bin_data: bytes = Column(LargeBinary, nullable=True)
    type: str = Column(String, nullable=True)


