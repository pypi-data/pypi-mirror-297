from pydantic_settings import BaseSettings
from pydantic import Field, ValidationError
from recomenda.core.logger import logger

class EmbedderConfig(BaseSettings):
    """
    Configuration settings for the embedder.

    Attributes:
        OPENAI_API_KEY (str): The API key for OpenAI services.
        OPENAI_EMBEDDING_MODEL (str): The name of the OpenAI embedding model to use.
    """
    OPENAI_API_KEY: str = Field(..., env='OPENAI_API_KEY')  # Required, no default
    OPENAI_EMBEDDING_MODEL: str = Field("text-embedding-3-small", env='OPENAI_EMBEDDING_MODEL')

    class Config:
        env_file = '.env'  # Load environment variables from a .env file if present
        env_file_encoding = 'utf-8'

class DatabaseConfig(BaseSettings):
    """
    Configuration settings for the database.

    Attributes:
        DATABASE_URL (str): The URL for the database connection.
    """
    DATABASE_URL: str = Field('sqlite:///./recommender.db', env='DATABASE_URL')

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'

class Config(BaseSettings):
    """
    Main configuration class that includes embedder and database configurations.

    Attributes:
        EMBEDDER (EmbedderConfig): Configuration for the embedder.
        DATABASE (DatabaseConfig): Configuration for the database.
    """
    EMBEDDER: EmbedderConfig = EmbedderConfig()
    DATABASE: DatabaseConfig = DatabaseConfig()

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'

try:
    config = Config()
except ValidationError as e:
    logger.error(f"Configuration validation error: {e}")
    raise EnvironmentError("One or more configuration variables are not set correctly.")
