from .db import DatabaseManager

from ..config import settings
from ..models.db import Base


# Создание подключения
db = DatabaseManager(settings.DB_PARAMS.db_url)

# Создание таблиц при первом запуске
Base.metadata.create_all(db.engine)

__all__ = [
    "db",
    "DatabaseManager",
]