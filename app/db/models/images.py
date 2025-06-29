from sqlalchemy import Column, Integer, BOOLEAN, LargeBinary, String
from ..db_session import SqlAlchemyBase


class Images(SqlAlchemyBase):
    __tablename__ = "Images"
    id: int = Column(Integer, primary_key=True, autoincrement=True)
    bin_data: bytes = Column(LargeBinary, nullable=False)
    type: str = Column(String, nullable=False)
    is_preview = Column(BOOLEAN, nullable=False, default=True)
