from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, scoped_session, sessionmaker
import redis

from app import settings


class Base(DeclarativeBase):
    pass


engine = create_engine(settings.db_string, echo=True)
session_factory = sessionmaker(bind=engine)
database = scoped_session(session_factory)

redis = redis.Redis.from_url(settings.redis_url)
