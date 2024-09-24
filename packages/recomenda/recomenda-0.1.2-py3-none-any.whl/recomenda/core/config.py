# ./src/core/config.py

import os
from typing import Optional
# from dotenv import load_dotenv
from recomenda.core.logger import logger

# load_dotenv()  # Load environment variables from a .env file if present


class EmbedderConfig:
    OPENAI_API_KEY: str = os.getenv('OPENAI_API_KEY')
    if not OPENAI_API_KEY:
        logger.error("OPENAI_API_KEY environment variable is not set.")
        raise EnvironmentError("OPENAI_API_KEY environment variable is not set.")

    OPENAI_EMBEDDING_MODEL: str = os.getenv('OPENAI_EMBEDDING_MODEL', "text-embedding-3-small")


class DatabaseConfig:
    DATABASE_URL: str = os.getenv('DATABASE_URL', 'sqlite:///./recommender.db')


class Config:
    EMBEDDER = EmbedderConfig()
    DATABASE = DatabaseConfig()


config = Config()