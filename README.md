# Binance Futures Testnet Trading Bot (USDT-M)

A clean, structured Python Command Line Interface (CLI) application built to interact safely with the Binance Futures Testnet environment. This bot lets you quickly validate and place MARKET and LIMIT orders while saving detailed session logs to a dedicated file.

---

## 🏗️ Architecture & Project Structure

The application separates the presentation (CLI) layer from the core exchange logic and input validation:

trading_bot/
├── bot/
│   ├── __init__.py
│   ├── client.py          # Safely initializes the Binance Testnet Client
│   ├── logging_config.py  # Handles simultaneous file + console logging
│   ├── orders.py          # Core layer for mapping and sending order payloads
│   └── validators.py      # Local input verification & sanity checks
├── logs/
│   └── trading.log        # Automatically generated session log file
├── .env                   # Local Environment Variables (Git ignored for security)
├── .gitignore             # Config to keep sensitive/unneeded files out of Git
├── cli.py                 # Main entry point using the Click framework
└── requirements.txt       # Project dependencies manifest

---

## 🛠️ Local Installation & Setup

Follow these steps to set up the project and run it locally:

### 1. Project Initialization
Clone or extract this project folder, open your terminal in the root directory, and set up a virtual environment:

```bash
# Create an isolated virtual environment
python -m venv venv

# Activate the environment (Windows PowerShell)
venv\Scripts\activate
2. Install Dependencies
Install the required packages listed in the requirements file:

Bash
pip install -r requirements.txt
3. Configure API Keys
Create a file named .env in the root directory and add your Binance Demo trading credentials:

Code snippet
BINANCE_API_KEY=your_testnet_api_key_here
BINANCE_API_SECRET=your_testnet_api_secret_here
(Note: The .env file is included in .gitignore so your private API keys are never pushed to GitHub.)

🚀 How to Run the Bot
You can check the built-in help menu at any time by running:

Bash
python cli.py --help
A. Execute an Instant MARKET Order
Place an immediate market order by specifying the symbol, side, order type, and quantity:

Bash
python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.001
B. Execute a Resting LIMIT Order
Place a targeted limit order by including the target price.
(Note: Ensure your total order value satisfies Binance's minimum $50 notional threshold.)

Bash
python cli.py --symbol BTCUSDT --side BUY --type LIMIT --quantity 0.0015 --price 40000


🧠 Design Assumptions & Guardrails
Testnet Safety: The application enforces testnet=True when connecting to the Binance library. This ensures all traffic hits the sandbox environment (testnet.binancefuture.com) and zero real capital is at risk.

Smart Input Validation: User parameters are cleaned and validated locally before hitting the network. For example, text inputs like buy or market are automatically formatted to uppercase (BUY, MARKET), and prices/quantities are checked for validity.

Notional Value Errors: If an order falls below Binance's minimum asset threshold (e.g., Error Code -4164 for under $50 total value), the bot catches the exchange exception gracefully instead of crashing out.





