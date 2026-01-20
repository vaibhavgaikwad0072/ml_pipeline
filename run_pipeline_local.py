import logging
import sys
import os

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Add src to path
sys.path.append(os.getcwd())

from src.crawler import run_crawler
from src.processor import run_processor
from src.aggregator import run_aggregator

def main():
    logger.info("Starting Local Pipeline Execution...")
    
    logger.info("Step 1: Crawling...")
    try:
        run_crawler()
    except Exception as e:
        logger.error(f"Crawling failed: {e}")
        return

    logger.info("Step 2: Processing...")
    try:
        run_processor()
    except Exception as e:
        logger.error(f"Processing failed: {e}")
        return

    logger.info("Step 3: Aggregating...")
    try:
        run_aggregator()
    except Exception as e:
        logger.error(f"Aggregation failed: {e}")
        return

    logger.info("Pipeline completed successfully.")

if __name__ == "__main__":
    main()
