from sqlalchemy import Table, Column, Integer, ForeignKey
from ..db_session import SqlAlchemyBase

film_place_association = Table(
    'film_place_association',
    SqlAlchemyBase.metadata,
    Column('film_id', Integer, ForeignKey('Films.id')),
    Column('place_id', Integer, ForeignKey('Places.id'))
)

place_hint_association = Table(
    'place_img_association',
    SqlAlchemyBase.metadata,
    Column('film_id', Integer, ForeignKey('Places.id')),
    Column('hint_id', Integer, ForeignKey('Images.id'))
)
