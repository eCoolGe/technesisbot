import logging
import os
from .config import settings

# Проверка существования папки логов
log_dir = os.path.dirname(settings.LOG_FILE_PATH)
os.makedirs(log_dir, exist_ok=True)

# Настройка логгера
file_handler = logging.FileHandler(settings.LOG_FILE_PATH, encoding="utf-8")
console_handler = logging.StreamHandler()

logging.basicConfig(
    format="%(filename)s [ LINE:%(lineno)+3s ]#%(levelname)+8s [%(asctime)s]  %(message)s",
    level=logging.INFO,
    handlers=[file_handler, console_handler],
)

log = logging.getLogger(__name__)
log.info("====================")
