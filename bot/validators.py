import logging
from bot.logging_config import logger

def validate_order_inputs(symbol: str, side: str, order_type: str, quantity: float, price: float = None):
    """
    Validates user inputs locally before hitting the Binance API.
    Raises ValueError if any input is invalid.
    """
    # 1. Validate Symbol (Must be a non-empty string, usually uppercase)
    if not symbol or not isinstance(symbol, str):
        logger.error("Validation Failed: Symbol must be a valid text string.")
        raise ValueError("Symbol must be a valid text string (e.g., BTCUSDT).")
    
    symbol_clean = symbol.strip().upper()

    # 2. Validate Side (Must be BUY or SELL)
    side_clean = side.strip().upper()
    if side_clean not in ["BUY", "SELL"]:
        logger.error(f"Validation Failed: Invalid side '{side}'.")
        raise ValueError("Side must be either 'BUY' or 'SELL'.")

    # 3. Validate Order Type (Must be MARKET or LIMIT)
    type_clean = order_type.strip().upper()
    if type_clean not in ["MARKET", "LIMIT"]:
        logger.error(f"Validation Failed: Invalid order type '{order_type}'.")
        raise ValueError("Order type must be either 'MARKET' or 'LIMIT'.")

    # 4. Validate Quantity (Must be greater than zero)
    try:
        qty_float = float(quantity)
        if qty_float <= 0:
            raise ValueError()
    except (TypeError, ValueError):
        logger.error(f"Validation Failed: Invalid quantity '{quantity}'.")
        raise ValueError("Quantity must be a positive number greater than 0.")

    # 5. Validate Price for LIMIT orders (Required and must be greater than zero)
    if type_clean == "LIMIT":
        if price is None:
            logger.error("Validation Failed: Price missing for LIMIT order.")
            raise ValueError("Price is required when the order type is 'LIMIT'.")
        try:
            price_float = float(price)
            if price_float <= 0:
                raise ValueError()
        except (TypeError, ValueError):
            logger.error(f"Validation Failed: Invalid price '{price}'.")
            raise ValueError("Price must be a positive number greater than 0 for LIMIT orders.")
    else:
        # If it's a MARKET order, price isn't used
        price_float = None

    # Return cleaned, properly typed data to pass to the API client safely
    return symbol_clean, side_clean, type_clean, qty_float, price_float