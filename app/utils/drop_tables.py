from app.config.database import Base, engine
from app.models.sessions import PeepSession
from app.models.templates import Template


def drop_tables():
    """
    Drops all database tables defined in the application.
    """
    Base.metadata.drop_all(bind=engine)
    PeepSession.metadata.drop_all(bind=engine)
    Template.metadata.drop_all(bind=engine)
