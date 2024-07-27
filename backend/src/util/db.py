from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.src.config.config import settings
from sqlalchemy.ext.declarative import declarative_base

SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL

Base = declarative_base()
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


#async version:
        
#from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
#from sqlalchemy.orm import sessionmaker
#from src.config.config import settings

#SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL

#ngine = create_async_engine(SQLALCHEMY_DATABASE_URL, echo=True)
#AsyncSessionLocal = sessionmaker(
#    engine, class_=AsyncSession, expire_on_commit=False
#)

#async def get_db():
#    async with AsyncSessionLocal() as session:
#        try:
#          yield session
#       finally:
#           await session.close()
