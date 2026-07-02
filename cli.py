import sys
import click
from bot.logging_config import logger
from bot.validators import validate_order_inputs
from bot.client import get_binance_client
from bot.orders import place_futures_order

@click.command()
@click.option('--symbol', required=True, help='The trading pair symbol (e.g., BTCUSDT).')
@click.option('--side', required=True, type=click.Choice(['BUY', 'SELL', 'buy', 'sell']), help='Order side: BUY or SELL.')
@click.option('--type', 'order_type', required=True, type=click.Choice(['MARKET', 'LIMIT', 'market', 'limit']), help='Order type: MARKET or LIMIT.')
@click.option('--quantity', required=True, type=float, help='The asset quantity to trade.')
@click.option('--price', type=float, default=None, help='The target execution price (Strictly required for LIMIT orders).')
def main(symbol, side, order_type, quantity, price):
    """
    Unified Command Line Interface for execution of the Binance Futures Trading Bot.
    """
    logger.info("================ NEW CLI INVOCATION ================")
    logger.info(f"Command parameters received: symbol={symbol}, side={side}, type={order_type}, qty={quantity}, price={price}")

    try:
        # Step 1: Clean and validate inputs locally
        symbol_c, side_c, type_c, qty_c, price_c = validate_order_inputs(
            symbol=symbol,
            side=side,
            order_type=order_type,
            quantity=quantity,
            price=price
        )
        
        # Step 2: Establish connection with Binance Testnet
        client = get_binance_client()
        
        # Step 3: Send order execution request to exchange
        click.echo(click.style("\n🚀 Sending order payload to Binance Futures Testnet...", fg="yellow"))
        response = place_futures_order(
            client=client,
            symbol=symbol_c,
            side=side_c,
            order_type=type_c,
            quantity=qty_c,
            price=price_c
        )
        
        # Step 4: Display beautiful success output summary to user
        click.echo(click.style("\n✅ ORDER EXECUTED SUCCESSFULLY!", fg="green", bold=True))
        click.echo("-" * 45)
        click.echo(f"✨ Order ID:       {response.get('orderId')}")
        click.echo(f"✨ Status:         {response.get('status')}")
        click.echo(f"✨ Executed Qty:   {response.get('executedQty')}")
        click.echo(f"✨ Client OrderID: {response.get('clientOrderId')}")
        click.echo("-" * 45)
        
        logger.info(f"CLI Finished Processing. Order ID {response.get('orderId')} output cleanly displayed.")

    except ValueError as val_err:
        click.echo(click.style(f"\n❌ Validation Error: {val_err}", fg="red", bold=True))
        sys.exit(1)
        
    except ConnectionError as conn_err:
        click.echo(click.style(f"\n❌ Network Connection Error: {conn_err}", fg="red", bold=True))
        sys.exit(1)
        
    except Exception as general_err:
        click.echo(click.style(f"\n❌ Execution Failed: {general_err}", fg="red", bold=True))
        sys.exit(1)

if __name__ == '__main__':
    main()