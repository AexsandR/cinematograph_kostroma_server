from sqlalchemy import Column, Integer, BOOLEAN, LargeBinary, String
from ..db_session import SqlAlchemyBase
from sqlalchemy.orm import relationship


class Images(SqlAlchemyBase):
    __tablename__ = "Images"
    id: int = Column(Integer, primary_key=True, autoincrement=True)
    bin_data: bytes = Column(LargeBinary, nullable=False)
    type: str = Column(String, nullable=False)
    places = relationship(
        "Places",
        secondary="place_img_association",
        back_populates="hints"
    )
