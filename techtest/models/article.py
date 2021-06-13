from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import Text
from sqlalchemy import Table
from sqlalchemy.orm import relationship

from techtest.connector import BaseModel

_article_region_table = Table(
    'article_region',
    BaseModel.metadata,
    Column('article_id', Integer, ForeignKey('article.id')),
    Column('region_id', Integer, ForeignKey('region.id')),
)

_article_author_table = Table(
    'article_author',
    BaseModel.metadata,
    Column('article_id', Integer, ForeignKey('article.id')),
    Column('author_id', Integer, ForeignKey('author.id')),
)


class Article(BaseModel):
    __tablename__ = 'article'

    id = Column(
        Integer,
        name='id',
        nullable=False,
        primary_key=True,
        autoincrement=True,
    )

    title = Column(
        Text,
        name='title',
    )

    content = Column(
        Text,
        name='content',
    )

    regions = relationship(
        'Region',
        secondary=_article_region_table,
        order_by='Region.id'
    )

    authors = relationship(
        'Author',
        secondary=_article_author_table,
        order_by='Author.id'
    )
