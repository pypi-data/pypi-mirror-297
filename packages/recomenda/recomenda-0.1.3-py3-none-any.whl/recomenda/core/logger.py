# ./src/core/logger.py

import logging
from datetime import datetime
import pytz
from typing import Optional


class ConfigurableFormatter(logging.Formatter):
    def __init__(self, fmt: str, timezone: str = 'UTC'):
        super().__init__(fmt)
        self.timezone = pytz.timezone(timezone)

    def formatTime(self, record, datefmt: Optional[str] = None) -> str:
        dt = datetime.fromtimestamp(record.created, tz=self.timezone)
        if datefmt:
            return dt.strftime(datefmt)
        return dt.isoformat()


class SingletonLogger:
    _logger: Optional[logging.Logger] = None

    def __new__(cls, timezone: str = 'America/Sao_Paulo', level: int = logging.INFO):
        if cls._logger is None:
            cls._logger = logging.getLogger("RecommenderLogger")
            cls._logger.setLevel(level)

            if not cls._logger.handlers:
                # Create a console handler
                console_handler = logging.StreamHandler()

                # Create formatter and add it to the console handler
                formatter = ConfigurableFormatter('%(asctime)s - %(levelname)s - %(message)s', timezone)
                console_handler.setFormatter(formatter)

                # Add console handler to the logger
                cls._logger.addHandler(console_handler)
        return cls._logger

# Now, you can use SingletonLogger directly
logger = SingletonLogger()
