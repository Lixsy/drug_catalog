import pytest
from fastapi.testclient import TestClient
from api.api import app
from api import models

from api.database import SessionLocal

db = SessionLocal()


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)


@pytest.fixture(autouse=True)
def clear_db():
    db.query(models.DrugModel).delete()
    db.query(models.CategoryModel).delete()
    db.commit()
