# ./src/main.py

import asyncio
# import logging
from typing import List, Dict, Any

from recomenda.services.recommender import Recommender
from recomenda.services.async_recommender import AsyncRecommender
from recomenda.core.logger import logger
# from database.database import create_db_and_tables, get_session


# Example for Dummy Items (externalized from main.py)
DUMMY_ITEMS = [{
  'title': 'Smartphone',
  'description':
  'A high-end smartphone with the latest features and a stunning display.',
  'price': 799.99,
  'brand': 'Brand X',
  'category': 'Mobile',
  'stock': 35
}, {
  'title': 'Laptop',
  'description':
  'A powerful laptop with a sleek design, ideal for both work and entertainment.',
  'price': 1299.99,
  'brand': 'Brand Y',
  'category': 'Computers',
  'stock': 20
}, {
  'title': 'Tablet',
  'description':
  'A lightweight tablet with a large screen, perfect for reading and browsing.',
  'price': 499.99,
  'brand': 'Brand G',
  'category': 'Tablets',
  'stock': 50
}, {
  'title': 'Desktop PC',
  'description':
  'A desktop PC with a robust processor and ample storage for gaming and productivity.',
  'price': 1499.99,
  'brand': 'Brand A',
  'category': 'Computers',
  'stock': 15
}, {
  'title': 'Smartwatch',
  'description':
  'A stylish smartwatch with health tracking and seamless smartphone integration.',
  'price': 199.99,
  'brand': 'Brand B',
  'category': 'Wearables',
  'stock': 60
}, {
  'title': 'Wireless Earbuds',
  'description':
  'Compact wireless earbuds with noise-cancellation and high-quality sound.',
  'price': 129.99,
  'brand': 'Brand C',
  'category': 'Audio',
  'stock': 100
}, {
  'title': 'Gaming Console',
  'description':
  'A next-gen gaming console with immersive graphics and exclusive titles.',
  'price': 499.99,
  'brand': 'Brand D',
  'category': 'Gaming',
  'stock': 10
}, {
  'title': 'Smart TV',
  'description':
  'A 4K smart TV with voice control and streaming services integration.',
  'price': 899.99,
  'brand': 'Brand E',
  'category': 'Home Entertainment',
  'stock': 25
}, {
  'title': 'Bluetooth Speaker',
  'description':
  'A portable Bluetooth speaker with deep bass and long battery life.',
  'price': 79.99,
  'brand': 'Brand F',
  'category': 'Audio',
  'stock': 75
}, {
  'title': 'E-Reader',
  'description':
  'An e-reader with a glare-free screen, perfect for reading books on the go.',
  'price': 129.99,
  'brand': 'Brand G',
  'category': 'Reading',
  'stock': 40
}]

# logger = SingletonLogger(timezone='America/New_York', level=logging.DEBUG).get_logger()
# logger.info("Logger initialized with New York timezone and DEBUG level.")


async def main_async():
    """
    Main entry point for the Recommender recommender system.
    Sets up the database, initializes the recommender, and generates recommendations.
    """
    try:
        # Initialize database
        # create_db_and_tables()
        logger.info("Database and tables created successfully.")

        recommend_options = DUMMY_ITEMS  # Use dummy items for demonstration
        recommend_to = 'I like to travel a lot.'
      
        # Initialize recommender with items
        recommender = AsyncRecommender(options=recommend_options, to=recommend_to)
        # await recommender.initialize()  # Ensure embeddings are initialized
        logger.info("Recommender initialized successfully.")

        await recommender.show_recommendations()  # Await the show_recommendations method
        print(await recommender.recommendation)
        await recommender.show_recommendations()  # Await the show_recommendations method
        print(recommender)
  
        # Generate recommendations
        recommendations = await recommender.generate_recommendations()

    except Exception as e:
        logger.error(f"An error occurred in the main process: {e}", exc_info=True)

def main_sync():
    """
    Main entry point for synchronous Recommender recommender system.
    Sets up the database, initializes the recommender, and generates recommendations.
    """
    try:
        recommend = Recommender()
        recommend_options = DUMMY_ITEMS  # Use dummy items for demonstration
        recommend_to = 'I like to play mobile games and I travel a lot.'
        recommend.options = DUMMY_ITEMS
        recommend.to = recommend_to
  
        # recommender = Recommender(options=DUMMY_ITEMS, to="Target Item")
        recommend.how_many = 3

        print(recommend)

        print("Unique recommendation:")
        print(recommend.recommendation)

        print(f"All the {recommend.how_many} recommendations:")
        print(recommend.recommendations)
        recommend.show_recommendations()

        # recommendations = recommender.generate_recommendations()
        # print("Top Recommendations:", recommendations)
        # recommender.show_recommendations()

    except Exception as e:
        logger.error(f"An error occurred in the synchronous main process: {e}", exc_info=True)


if __name__ == "__main__":
    choice = input("Run async (a) or sync (s) version? ").strip().lower()
    if choice == 'a':
        asyncio.run(main_async())
    elif choice == 's':
        main_sync()
    else:
        print("Invalid choice! Please select 'a' for async or 's' for sync.")