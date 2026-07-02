import os
from binance.client import Client
from dotenv import load_dotenv
from bot.logging_config import logger

# Load environment variables from the .env file automatically
load_dotenv()

def get_binance_client():
    """
    Initializes and returns a secure Binance API client configured 
    specifically for the Futures Testnet/Demo environment.
    """
    # 1. Fetch credentials from our hidden .env file
    api_key = os.getenv("BINANCE_API_KEY")
    api_secret = os.getenv("BINANCE_API_SECRET")

    # 2. Strict check: Ensure keys are present before wasting network resources
    if not api_key or not api_secret:
        logger.error("Authentication Error: Binance API Key or Secret missing from .env file.")
        raise ValueError("API Keys missing! Please check that your .env file is configured correctly.")

    try:
        logger.info("Initializing Binance Futures Client...")
        
        # 3. Create the connection client
        # testnet=True tells the library to route requests to testnet.binancefuture.com
        client = Client(api_key=api_key, api_secret=api_secret, testnet=True)
        
        # 4. Light network test: Verify connection status by fetching server time
        server_time = client.futures_time()
        logger.info(f"Successfully connected to Binance Futures Testnet. Server Time: {server_time['serverTime']}")
        
        return client

    except Exception as e:
        logger.error(f"Network Connection Failed: Connection to Binance API failed. Details: {e}")
        raise ConnectionError(f"Could not connect to Binance Testnet: {e}")