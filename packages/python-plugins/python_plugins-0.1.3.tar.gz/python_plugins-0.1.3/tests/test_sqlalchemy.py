from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from python_plugins.models.mixins import PrimaryKeyMixin
from python_plugins.models.mixins import DataMixin
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.schema import CreateTable

from sqlalchemy import create_mock_engine


class Base(DeclarativeBase):
    pass


class Demo(PrimaryKeyMixin, DataMixin, Base):
    __tablename__ = "demo"


def test_info():

    assert Demo.__table__.name == "demo"
    stmt = CreateTable(Demo.__table__)
    # print(stmt)
    assert "id INTEGER" in str(stmt)
    assert "data JSON" in str(stmt)
