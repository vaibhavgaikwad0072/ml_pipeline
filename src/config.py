import os

# Base Directories
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(PROJECT_ROOT, "data")

RAW_DATA_DIR = os.path.join(DATA_DIR, "raw")
PROCESSED_DATA_DIR = os.path.join(DATA_DIR, "processed")
METRICS_DIR = os.path.join(DATA_DIR, "metrics")

# Crawler Configuration
TARGET_WEBSITES = [
    "https://www.databricks.com",
    "https://www.snowflake.com",
    "https://www.confluent.io",
    "https://www.elastic.co",
    "https://www.mongodb.com"
]

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
REQUEST_TIMEOUT = 10

# Processor Configuration
# Heuristics for finding sections
NAVBAR_TAGS = ['nav', 'header']
NAVBAR_CLASSES = ['navbar', 'nav', 'header', 'menu']
FOOTER_TAGS = ['footer']
FOOTER_CLASSES = ['footer', 'bottom']
