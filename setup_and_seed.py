from techtest.models import *
from techtest.models.article import Article
from techtest.models.region import Region
from techtest.models.author import Author
from techtest.connector import engine, BaseModel, db_session

BaseModel.metadata.create_all(engine)

with db_session() as session:
    au = Region(code="AU", name="Australia")
    uk = Region(code="UK", name="United Kingdom")
    us = Region(code="US", name="United States of America")
    author1 = Author(first_name="Ben", last_name="Tyron")
    author2 = Author(first_name="Hughes", last_name="Jeff")
    author3 = Author(first_name="Louis", last_name="Jamie")

    session.add_all([
        au,
        uk,
        us,
        author1,
        author2,
        author3,
        Article(
            title='Post 1',
            content='This is a post body',
            regions=[au, uk],
            authors=[author1, author2],
        ),
        Article(
            title='Post 2',
            content='This is the second post body',
            regions=[au, us],
            authors=[author2, author3]
        ),
        Article(
            title='Post 3',
            content='This is the third post body',
            regions=[au, uk],
            authors=[author1]
        ),

    ])
