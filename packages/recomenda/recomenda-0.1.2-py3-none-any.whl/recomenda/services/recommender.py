# ./src/services/recommender.py

import hashlib
from typing import List, Optional, Dict, Any

from recomenda.services.embedder import Embedder
from recomenda.services.base_recommender import BaseRecommender
from recomenda.core.config import config
from recomenda.core.logger import logger


class Recommender(BaseRecommender):
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
        logger.debug("Initializing Recommender class")
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

        if self._options:
            self._initialize_embeddings_sync()
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
            self._initialize_embeddings_sync(options_to_embed)
        else:
            logger.info("No changes detected in options. No re-embedding needed.")

    def _initialize_embeddings_sync(self, options_to_embed: Optional[List[Dict[str, Any]]] = None) -> None:
        logger.debug("Initializing embeddings for options synchronously.")
        if not self._options:
            logger.warning("No options available to embed.")
            return

        if options_to_embed is None:
            options_to_embed = self._options

        try:
            new_embeddings = self.embedder.embed_items_sync(options_to_embed)

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

    def generate_recommendations(
        self,
        to: Optional[str] = None,
        how_many: Optional[int] = None,
        force: bool = False  # Added force parameter
    ) -> List[Dict[str, Any]]:
        logger.debug("Starting generate_recommendations method")

        # Only generate recommendations if they are not already available, or force is True
        if not force and self._recommendations and (how_many is None or len(self._recommendations) >= how_many):
            return self._recommendations

        if not self.options_embeddings:
            self._initialize_embeddings_sync()

        if not self.options_embeddings:
            logger.error("Options data is empty. Please set the options data first.")
            raise ValueError("Options data is empty. Please set the options data first.")

        target = to or self.to
        if not target:
            logger.error("No target provided for recommendations.")
            raise ValueError("No target provided for recommendations.")

        try:
            logger.debug(f"Generating embeddings for target: {target}")
            self.to_embeddings = self.embedder.embed_item_sync(target)

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
            if not self._recommendation:
                self._recommendation = self._recommendations[0]['option'] if self._recommendations else None

            logger.debug(f"Generated {len(self._recommendations)} recommendations")
            return self._recommendations
        except Exception as e:
            logger.error(f"Error generating recommendations: {e}", exc_info=True)
            raise
        finally:
            logger.debug("Finished generate_recommendations method")

    def generate_recommendation(self) -> Optional[Dict[str, Any]]:
        logger.debug("Starting generate_recommendation method")
        # Check if a single recommendation has already been generated
        if not self._recommendation:
            # Generate a single recommendation, but do not limit _recommendations
            if not self._recommendations:
                all_recommendations = self.generate_recommendations(force=True)  # Generate all recommendations
                if all_recommendations:
                    self._recommendation = all_recommendations[0]  # Take the first as the single recommendation
        logger.debug(f"Generated single recommendation: {self._recommendation}")
        return self._recommendation

    @property
    def complete_recommendations(self) -> List[Dict[str, Any]]:
        logger.debug("Accessing complete_recommendations property")
        if self._recommendations is None and self.to:
            self.generate_recommendations(force=True)  # Force to ensure full recommendations list
        return self._recommendations or []

    @property
    def complete_recommendation(self) -> Optional[Dict[str, Any]]:
        logger.debug("Accessing complete_recommendation property")
        if self._recommendation is None and self.to:
            self.generate_recommendation()
        return self._recommendation

    def show_complete_recommendations(self) -> None:
        logger.debug("Showing all complete recommendations")
        if self._recommendations is None:
            self.generate_recommendations(force=True)
        if self._recommendations:
            for index, reco in enumerate(sorted(self._recommendations, key=lambda x: x['similarity'], reverse=True)):
                print(f"Option: {reco['option']}, Similarity: {reco['similarity']}, Ranking: {index + 1}")
        else:
            logger.warning("No recommendations available to show.")
            logger.debug(f"Current recommendations: {self._recommendations}")

    def show_complete_recommendation(self) -> None:
        logger.debug("Showing single complete recommendation")
        if self._recommendation is None:
            self.generate_recommendation()
        if self._recommendation:
            print(f"Recommended Option: {self._recommendation}")
        else:
            logger.warning("No recommendation available to show.")
            logger.debug(f"Current recommendation: {self._recommendation}")

    @property
    def recommendations(self) -> List[Any]:  # Only returning options without extra details
        logger.debug("Accessing recommendations property")
        if self._recommendations is None and self.to:
            self.generate_recommendations(force=True)
        return [reco['option'] for reco in (self._recommendations or [])]

    @property
    def recommendation(self) -> Optional[Any]:  # Only returning single option without extra details
        logger.debug("Accessing recommendation property")
        if self._recommendation is None and self.to:
            self.generate_recommendation()
        return self._recommendation

    def show_recommendations(self) -> None:  # Simplified display of options
        logger.debug("Showing all recommendations")
        if self._recommendations is None:
            self.generate_recommendations(force=True)
        if self._recommendations:
            for reco in self._recommendations:
                print(f"Option: {reco['option']}")
        else:
            logger.warning("No recommendations available to show.")
            logger.debug(f"{self._recommendations}")

    def show_recommendation(self) -> None:  # Simplified display of a single option
        logger.debug("Showing single recommendation")
        if self._recommendation is None:
            self.generate_recommendation()
        if self._recommendation:
            print(f"{self._recommendation}")
        else:
            logger.warning("No recommendation available to show.")
            logger.debug(f"Current recommendation: {self._recommendation}")

    def __str__(self) -> str:
        return f"Recommender(how_many={self.how_many}, options={self.options} to={self.to})"