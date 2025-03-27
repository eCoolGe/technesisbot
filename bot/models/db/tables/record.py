from sqlalchemy import Column, Integer, String

from . import Base


class Record(Base):
    """
    Модель записи в базе данных.
    """
    __tablename__ = "records"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    url = Column(String, nullable=False)
    xpath = Column(String, nullable=False)
