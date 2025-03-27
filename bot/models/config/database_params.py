from pydantic import BaseModel
from sqlalchemy import URL


class DatabaseParamsModel(BaseModel):
    """
    Описывает параметры для подключения к SQLite
    """

    path: str

    @property
    def db_url(self):
        return URL.create(
            drivername="sqlite",
            database=self.path
        )
