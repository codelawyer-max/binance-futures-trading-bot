import os
import logging

def setup_logging():
    """Sets up a robust, structured logger for the trading bot."""
    # Step A: Ensure a dedicated logs directory exists at the root level
    os.makedirs("logs", exist_ok=True)
    
    logger = logging.getLogger("TradingBot")
    logger.setLevel(logging.INFO)
    
    # Step B: Prevent duplicate log entries if this file is imported multiple times
    if logger.handlers:
        return logger

    # Step C: File Handler - Captures detailed records into a permanent file (trading.log)
    file_handler = logging.FileHandler("logs/trading.log")
    file_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)

    # Step D: Console Handler - Prints clean, immediate feedback to you in the terminal window
    console_handler = logging.StreamHandler()
    console_formatter = logging.Formatter('%(levelname)s: %(message)s')
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)

    return logger

# Step E: Create a single reusable tracker to import across our other scripts
logger = setup_logging()