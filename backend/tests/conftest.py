# import pytest
# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker
# from backend.src.util.db import Base, get_db
# from backend.main import app
#
# SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
#
# engine = create_engine(SQLALCHEMY_DATABASE_URL)
# TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
#
# @pytest.fixture(scope="module")
# def test_db():
#     Base.metadata.create_all(bind=engine)
#     db = TestingSessionLocal()
#     yield db
#     db.close()
#     Base.metadata.drop_all(bind=engine)
#
# def override_get_db():
#     try:
#         db = TestingSessionLocal()
#         yield db
#     finally:
#         db.close()
#
# app.dependency_overrides[get_db] = override_get_db
