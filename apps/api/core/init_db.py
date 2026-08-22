from apps.api.core.database import engine, Base

from models.task import Task


def init_db():
    Base.metadata.create_all(bind=engine)
    print("DATABASE INITIALIZED")
    