"""
Database
"""

from typing import Annotated

from fastapi import Depends
from sqlalchemy import Engine, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, sessionmaker

from ..settings import Settings, get_settings

Base = declarative_base()


def get_engine(settings: Annotated[Settings, Depends(get_settings)]) -> Engine:
    """Database engine"""
    return create_engine(settings.db_url)


async def get_db(settings: Annotated[Settings, Depends(get_settings)]) -> Session:
    """Database session"""
    engine = get_engine(settings)
    session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    try:
        database = session_local()
        yield database
    finally:
        database.close()
