from sqlalchemy import Column, Integer, BOOLEAN, LargeBinary, String
from ..db_session import SqlAlchemyBase
from sqlalchemy.orm import relationship


class Media(SqlAlchemyBase):
    __tablename__ = "Media"
    id: int = Column(Integer, primary_key=True, autoincrement=True)
    bin_data: bytes = Column(LargeBinary, nullable=False)
    type: str = Column(String, nullable=False)
