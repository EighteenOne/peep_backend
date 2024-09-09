from app.config.database import Base, engine
from app.models.sessions import PeepSession
from app.models.templates import Template


def create_tables():
    """
    Creates all database tables defined in the application.
    """
    Base.metadata.create_all(bind=engine)
    PeepSession.metadata.create_all(bind=engine)
    Template.metadata.create_all(bind=engine)
