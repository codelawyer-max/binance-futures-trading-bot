from binance.client import Client
from binance.exceptions import BinanceAPIException
from bot.logging_config import logger

def place_futures_order(client: Client, symbol: str, side: str, order_type: str, quantity: float, price: float = None):
    """
    Sends the structured trade request to the Binance Futures Testnet API.
    Captures raw response metrics or handles exceptions safely.
    """
    try:
        # 1. Structure the parameter arguments dynamically based on order type
        params = {
            "symbol": symbol,
            "side": side,
            "type": order_type,
            "quantity": quantity
        }
        
        # Limit orders strictly require a price target
        if order_type == "LIMIT":
            params["price"] = str(price)
            params["timeInForce"] = "GTC"  # 'Good Till Cancelled' - standard industry execution

        logger.info(f"Sending Order Payload -> Symbol: {symbol} | Side: {side} | Type: {order_type} | Qty: {quantity}")

        # 2. Execute the order using the python-binance client instance
        response = client.futures_create_order(**params)
        
        logger.info(f"Order Executed Successfully! Order ID: {response.get('orderId')}")
        return response

    except BinanceAPIException as api_err:
        # Handles specific exchange rejections (e.g., balance too low, invalid leverage)
        logger.error(f"Binance Exchange Rejected Order: Code {api_err.code} | Message: {api_err.message}")
        raise api_err
        
    except Exception as e:
        # Handles broader runtime failures (e.g., sudden network disconnects)
        logger.error(f"Unexpected Critical Exception while placing order: {e}")
        raise e