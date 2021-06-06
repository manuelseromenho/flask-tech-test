from contextlib import contextmanager
import functools

from dictalchemy import DictableModel
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine("sqlite:///database.db", echo=True)
_db_session = sessionmaker(bind=engine)

BaseModel = declarative_base(cls=DictableModel)


@contextmanager
def db_session():
    """Provide a transactional scope around a series of operations.
    Taken from http://docs.sqlalchemy.org/en/latest/orm/session_basics.html.
    This handles rollback and closing of session, so there is no need
    to do that throughout the code.
    Usage:
        with db_session() as session:
            session.execute(query)
    """
    session = _db_session()
    try:
        yield session
        session.commit()
    except Exception as ex:
        session.rollback()
        raise ex
    finally:
        session.close()


def db_session_wrap(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        session = kwargs.pop('session', None)
        if session:
            return func(*args, session=session, **kwargs)
        else:
            with db_session() as session:
                return func(*args, session=session, **kwargs)

    return wrapper
