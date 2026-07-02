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
@click.option('--price', type=float, default=None, help='The target execution price (Required for LIMIT orders).')

def main(symbol, side, order_type, quantity, price):
    """
    Unified Command Line Interface for execution of the Binance Futures Trading Bot.
    """

    logger.info("================ NEW CLI INVOCATION ================")
    logger.info(
        f"Command parameters received: symbol={symbol}, side={side}, "
        f"type={order_type}, qty={quantity}, price={price}"
    )

    try:
        # Step 1: Validate and clean user inputs
        symbol_c, side_c, type_c, qty_c, price_c = validate_order_inputs(
            symbol=symbol,
            side=side,
            order_type=order_type,
            quantity=quantity,
            price=price
        )

        # Step 2: Connect to Binance Futures Testnet
        client = get_binance_client()

        # Step 3: Print Order Request Summary
        click.echo(click.style("\n📋 ORDER REQUEST SUMMARY", fg="cyan", bold=True))
        click.echo("-" * 45)
        click.echo(f"📌 Symbol:      {symbol_c}")
        click.echo(f"📌 Side:        {side_c}")
        click.echo(f"📌 Order Type:  {type_c}")
        click.echo(f"📌 Quantity:    {qty_c}")

        if type_c == "LIMIT":
            click.echo(f"📌 Price:       {price_c}")

        click.echo("-" * 45)

        click.echo(click.style("\n🚀 Sending order to Binance Futures Testnet...", fg="yellow"))

        # Step 4: Place Order
        response = place_futures_order(
            client=client,
            symbol=symbol_c,
            side=side_c,
            order_type=type_c,
            quantity=qty_c,
            price=price_c
        )

        # Step 5: Display Order Response
        click.echo(click.style("\n✅ ORDER EXECUTED SUCCESSFULLY!", fg="green", bold=True))
        click.echo("-" * 45)
        click.echo(f"🆔 Order ID:        {response.get('orderId')}")
        click.echo(f"📊 Status:          {response.get('status')}")
        click.echo(f"📦 Executed Qty:    {response.get('executedQty')}")

        avg_price = response.get("avgPrice")

        if avg_price and avg_price != "0.0":
            click.echo(f"💰 Average Price:   {avg_price}")
        else:
            click.echo("💰 Average Price:   N/A")

        click.echo("-" * 45)

        logger.info(
            f"CLI Finished Processing. Order ID {response.get('orderId')} output cleanly displayed."
        )

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