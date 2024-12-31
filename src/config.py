import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    # API Keys
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    COINGECKO_API_KEY = os.getenv('COINGECKO_API_KEY')
    ETHERSCAN_API_KEY = os.getenv('ETHERSCAN_API_KEY')
    TWITTER_API_KEY = os.getenv('TWITTER_API_KEY')
    
    # Browser Config
    VIEWPORT_SIZE = {"width": 1920, "height": 1080}
    USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    
    # Paths
    BASE_DIR = Path(__file__).parent.parent
    SCREENSHOT_DIR = BASE_DIR / "analysis_screenshots"
    ANALYSIS_DIR = BASE_DIR / "analysis_results"
    
    # Timeouts
    PAGE_LOAD_TIMEOUT = 30000  # milliseconds
    SCREENSHOT_TIMEOUT = 10000  # milliseconds
