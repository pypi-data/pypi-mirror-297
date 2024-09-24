# ./src/services/base_recommender.py

import logging
from typing import List, Optional, Any
from scipy.spatial.distance import cosine
from services.embedder import Embedder
from core.config import config
from core.logger import logger


class BaseRecommender:
    def __init__(
        self,
        api_key: str = config.EMBEDDER.OPENAI_API_KEY,
        model: str = config.EMBEDDER.OPENAI_EMBEDDING_MODEL,
        embedder: Optional[Embedder] = None
    ) -> None:
        """
        Initializes the BaseRecommender with the specified API key and model.
        Automatically creates an Embedder instance with the provided API key and model.
        """
        self.api_key: str = api_key
        self.model: str = model
        self.embedder = embedder or Embedder(model=self.model, api_key=self.api_key)  # Embedder initialized internally
        logger.debug(f"BaseRecommender initialized with model: {self.model} and api_key: {self.api_key}")

    async def generate_embeddings(self, data: List[str]) -> List[List[float]]:
        """
        Asynchronously generates embeddings for a list of data items.
        """
        logger.debug(f"Generating embeddings for data: {data}")
        try:
            embeddings = await self.embedder.embed_items_async(data)
            logger.debug(f"Generated embeddings: {embeddings}")
            return embeddings
        except Exception as e:
            logger.error(f"Error generating embeddings: {e}", exc_info=True)
            raise

    def generate_embeddings_sync(self, data: List[str]) -> List[List[float]]:
        """
        Synchronously generates embeddings for a list of data items.
        """
        logger.debug(f"Generating embeddings for data synchronously: {data}")
        try:
            embeddings = self.embedder.embed_items_sync(data)
            logger.debug(f"Generated embeddings: {embeddings}")
            return embeddings
        except Exception as e:
            logger.error(f"Error generating embeddings: {e}", exc_info=True)
            raise

    def calculate_similarity(self, embed1: List[float], embed2: List[float]) -> float:
        """
        Calculates cosine similarity between two embeddings.
        """
        try:
            similarity = 1 - cosine(embed1, embed2)
            logger.debug(f"Calculated similarity: {similarity}")
            return similarity
        except Exception as e:
            logger.error(f"Error calculating similarity: {e}", exc_info=True)
            raise

    def set_logger(self, logger_instance: logging.Logger) -> None:
        """
        Sets a custom logger instance.
        """
        global logger
        logger = logger_instance
        logger.debug("Logger instance has been updated.")
