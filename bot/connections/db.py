from typing import Type

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import NoResultFound
from ..models.db import Base, Record
from ..logger import log
from ..lang.ru import LOG_MSG_DEFAULT_ERROR


class DatabaseManager:
    """
    Класс для работы с базой данных SQLite.
    """

    def __init__(self, db_url):
        self.engine = create_engine(db_url, echo=False)
        self.__sessionmaker = sessionmaker(bind=self.engine)
        self.session = self.__sessionmaker()

    @staticmethod
    def _database_operation(func):
        """
        Декоратор для обработки исключений в БД.
        """

        def wrapper(self, *args, **kwargs):
            try:
                return func(self, *args, **kwargs)
            except NoResultFound:
                return None
            except Exception as error:
                log.error(LOG_MSG_DEFAULT_ERROR, error)
                self.session.rollback()
                return None
            finally:
                self.session.close()

        return wrapper

    @_database_operation
    def insert_record(self, title: str, url: str, xpath: str) -> int:
        """
        Вставляет новую запись в БД.
        """
        record = Record(title=title, url=url, xpath=xpath)
        self.session.add(record)
        self.session.commit()
        return record.id

    @_database_operation
    def get_record(self, record_id: int) -> Type[Record] | None:
        """
        Получает запись по ID.
        """
        return self.session.query(Record).filter_by(id=record_id).one()

    @_database_operation
    def get_all_records(self) -> list[Type[Record]]:
        """
        Возвращает список всех записей.
        """
        return self.session.query(Record).all()

    @_database_operation
    def update_record(self, record_id: int, title: str = None, url: str = None, xpath: str = None) -> bool:
        """
        Обновляет запись по ID.
        """
        record = self.session.query(Record).filter_by(id=record_id).one()
        if title:
            record.title = title
        if url:
            record.url = url
        if xpath:
            record.xpath = xpath
        self.session.commit()
        return True

    @_database_operation
    def delete_record(self, record_id: int) -> bool:
        """
        Удаляет запись по ID.
        """
        record = self.session.query(Record).filter_by(id=record_id).one()
        self.session.delete(record)
        self.session.commit()
        return True

    def reset_database(self) -> bool:
        """
        Полностью пересоздает базу данных.
        """
        try:
            self.session.close()
            self.engine.dispose()
            Base.metadata.drop_all(self.engine)
            Base.metadata.create_all(self.engine)
            self.session = self.__sessionmaker()
            return True
        except Exception as error:
            log.error(LOG_MSG_DEFAULT_ERROR, error)
            return False


