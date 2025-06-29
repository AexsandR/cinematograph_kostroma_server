from sqlalchemy import Column, Integer, LargeBinary, String
from ..db_session import SqlAlchemyBase

class Hints(SqlAlchemyBase):
    __tablename__ = "Hints"
    id: int = Column(Integer, primary_key=True, autoincrement=True)
    bin_data: bytes = Column(LargeBinary, nullable=False)
    type: str = Column(String, nullable=False)
