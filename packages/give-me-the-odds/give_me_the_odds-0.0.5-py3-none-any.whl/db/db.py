from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


def init_db(path: str):
    engine = create_engine(path)
    db_session = scoped_session(sessionmaker(autocommit=False,
                                            autoflush=False,
                                            bind=engine))
    Base.query = db_session.query_property()
    import db.route
    Base.metadata.create_all(bind=engine)
    return db_session
