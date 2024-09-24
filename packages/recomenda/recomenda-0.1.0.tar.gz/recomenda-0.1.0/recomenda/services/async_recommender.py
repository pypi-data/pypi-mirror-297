# ./src/services/async_recommender.py

from typing import List, Optional, Dict, Any
import asyncio
import hashlib
from services.base_recommender import BaseRecommender
from core.config import config
from core.logger import logger
from services.embedder import Embedder


class AsyncRecommender(BaseRecommender):
    def __init__(
        self,
        embedder: Optional[Embedder] = None,
        how: str = "default",
        how_many: int = 5,
        options: Optional[List[Dict[str, Any]]] = None,
        to: Optional[str] = None,
        api_key: str = config.EMBEDDER.OPENAI_API_KEY,
        model: str = config.EMBEDDER.OPENAI_EMBEDDING_MODEL
    ) -> None:
        logger.debug("Initializing AsyncRecommender class")
        self.embedder = embedder or Embedder(api_key=api_key, model=model)
        super().__init__(api_key=api_key, model=model, embedder=self.embedder)
        self.how = how
        self.how_many = how_many
        self._options: List[Dict[str, Any]] = options or []
        self.to = to
        self.options_embeddings: Optional[List[List[float]]] = None
        self.to_embeddings: Optional[List[float]] = None
        self._recommendation: Optional[Dict[str, Any]] = None
        self._recommendations: Optional[List[Dict[str, Any]]] = None
        self._options_hash: Dict[str, str] = {}
        self._initialization_task = None

        if self._options:
            self._initialization_task = asyncio.create_task(self._initialize_embeddings())
        logger.debug(f"Initialized with how={how}, how_many={how_many}, options={options}, to={to}")

    @staticmethod
    def hash_option(option: Dict[str, Any]) -> str:
        option_string = str(sorted(option.items()))
        return hashlib.sha256(option_string.encode()).hexdigest()

    def update_option_hashes(self) -> List[Dict[str, Any]]:
        new_hashes = {self.hash_option(option): option for option in self._options}
        options_to_embed = [
            option for hash_key, option in new_hashes.items()
            if hash_key not in self._options_hash or self._options_hash[hash_key] != hash_key
        ]
        self._options_hash = new_hashes
        return options_to_embed

    @property
    def options(self) -> List[Dict[str, Any]]:
        return self._options

    @options.setter
    def options(self, new_options: List[Dict[str, Any]]):
        logger.debug("Options updated. Checking for changes.")
        self._options = new_options
        options_to_embed = self.update_option_hashes()
        if options_to_embed:
            logger.info(f"New or modified options detected, embedding required for {len(options_to_embed)} options.")
            self._initialization_task = asyncio.create_task(self._initialize_embeddings(options_to_embed))
        else:
            logger.info("No changes detected in options. No re-embedding needed.")

    async def _initialize_embeddings(self, options_to_embed: Optional[List[Dict[str, Any]]] = None) -> None:
        logger.debug("Initializing embeddings for options.")
        if not self._options:
            logger.warning("No options available to embed.")
            return

        if options_to_embed is None:
            options_to_embed = self._options

        try:
            new_embeddings = await self.embedder.embed_items_async(options_to_embed)

            if self.options_embeddings is None:
                self.options_embeddings = []

            for option, embedding in zip(options_to_embed, new_embeddings):
                option_hash = self.hash_option(option)
                if option_hash in self._options_hash:
                    index = list(self._options_hash.keys()).index(option_hash)
                    if index < len(self.options_embeddings):
                        self.options_embeddings[index] = embedding
                    else:
                        self.options_embeddings.append(embedding)
                else:
                    self.options_embeddings.append(embedding)

            logger.info("Embeddings updated successfully for modified options.")
        except Exception as e:
            logger.error(f"Error updating embeddings: {e}", exc_info=True)
            raise

    async def generate_recommendations(
        self,
        to: Optional[str] = None,
        how_many: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        logger.debug("Starting generate_recommendations method")
        if self._initialization_task:
            await self._initialization_task

        if not self.options_embeddings:
            logger.error("Options data is empty. Please set the options data first.")
            raise ValueError("Options data is empty. Please set the options data first.")

        target = to or self.to
        if not target:
            logger.error("No target provided for recommendations.")
            raise ValueError("No target provided for recommendations.")

        try:
            logger.debug(f"Generating embeddings for target: {target}")
            self.to_embeddings = await self.embedder.embed_item_async(target)

            logger.debug("Calculating similarities and sorting recommendations")
            recommendations = [
                {
                    'option': option,
                    'similarity': self.calculate_similarity(self.to_embeddings, embedding)
                }
                for option, embedding in zip(self.options, self.options_embeddings)
            ]

            logger.debug(f"Unsorted recommendations: {recommendations}")

            recommendations.sort(key=lambda x: x['similarity'], reverse=True)
            n = how_many if how_many is not None else self.how_many
            self._recommendations = recommendations[:n]
            self._recommendation = self._recommendations[0]['option'] if self._recommendations else None

            logger.debug(f"Generated {len(self._recommendations)} recommendations")
            return self._recommendations
        except Exception as e:
            logger.error(f"Error generating recommendations: {e}", exc_info=True)
            raise
        finally:
            logger.debug("Finished generate_recommendations method")

    async def generate_recommendation(self) -> Optional[Dict[str, Any]]:
        logger.debug("Starting generate_recommendation method")
        if self._recommendations:
            recommendation = await self._recommendations[0]
        else:
            temp_recommendations = await self.generate_recommendations(how_many=1)
            recommendation = temp_recommendations[0] if temp_recommendations else None
        logger.debug(f"Generated single recommendation: {recommendation}")
        return recommendation

    @property
    async def complete_recommendations(self) -> List[Dict[str, Any]]:
        logger.debug("Accessing recommendations property")
        if self._recommendations is None and self.to:
            self._recommendations = await self.generate_recommendations()
        return self._recommendations or []

    @property
    async def complete_recommendation(self) -> Optional[Dict[str, Any]]:
        logger.debug("Accessing recommendation property")
        if self._recommendation is None and self.to:
            self._recommendation = await self.generate_recommendation()
        return self._recommendation

    async def show_complete_recommendations(self) -> None:
        logger.debug("Showing all recommendations")
        if self._initialization_task:
            await self._initialization_task
        if self._recommendations is None:
            await self.generate_recommendations()
        if self._recommendations:
            for index, reco in enumerate(sorted(self._recommendations, key=lambda x: x['similarity'], reverse=True)):
                print(f"Option: {reco['option']}, Similarity: {reco['similarity']}, Ranking: {index + 1}")
        else:
            logger.warning("No recommendations available to show.")
            logger.debug(f"Current recommendations: {self._recommendations}")

    async def show_complete_recommendation(self) -> None:
        logger.debug("Showing single recommendation")
        if self._initialization_task:
            await self._initialization_task
        if self._recommendation is None:
            await self.generate_recommendation()
        if self._recommendation:
            print(f"Recommended Option: {self._recommendation}")
        else:
            logger.warning("No recommendation available to show.")
            logger.debug(f"Current recommendation: {self._recommendation}")

    @property
    async def recommendations(self) -> List[Any]:  # Only returning options without extra details
        logger.debug("Accessing recommendations property")
        if self._recommendations is None and self.to:
            await self.generate_recommendations()
        return [reco['option'] for reco in (self._recommendations or [])]

    @property
    async def recommendation(self) -> Optional[Any]:  # Only returning single option without extra details
        logger.debug("Accessing recommendation property")
        if self._recommendation is None and self.to:
            await self.generate_recommendation()
        return self._recommendation

    async def show_recommendations(self) -> None:  # Simplified display of options
        logger.debug("Showing all recommendations")
        if self._initialization_task:
            await self._initialization_task
        if self._recommendations is None:
            await self.generate_recommendations()
        if self._recommendations:
            print(f"{self._recommendations}")
                
        else:
            logger.warning("No recommendations available to show.")
            logger.debug(f"Current recommendations: {self._recommendations}")

    async def show_recommendation(self) -> None:  # Simplified display of a single option
        logger.debug("Showing single recommendation")
        if self._initialization_task:
            await self._initialization_task
        if self._recommendation is None:
            await self.generate_recommendation()
        if self._recommendation:
            print(f"{self._recommendation}")
        else:
            logger.warning("No recommendation available to show.")
            logger.debug(f"Current recommendation: {self._recommendation}")

    async def get_recommendations_str(self) -> str:
        recommendations = await self.recommendations
        if recommendations:
            return '\n'.join([str(reco) for reco in recommendations])
        else:
            return "No recommendations available."

    def __str__(self) -> str:
        return f"AsyncRecommender({self.how_many}, options={self.options} to={self.to})"