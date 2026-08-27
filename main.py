
import logging
import logging.config
import sys
from app.extractor import get_crypto_price,get_usd_kes_rate
from app.transformer import transform_crypto_price
from app.loader import load_data
from app.argument_parser import parse_arguments




# load the logging configuration file
logging.config.fileConfig(fname = 'config/logging.conf')

logger = logging.getLogger(__name__)


def run_main_pipeline():
    try:
        args = parse_arguments()

        usd_kes_rate = get_usd_kes_rate()

        symbol_no_split = args.symbol.upper()

        symbols = [symbol.strip() for symbol in symbol_no_split.split(",")]

        results = []

        for symbol in symbols:

            crypto_price = get_crypto_price(symbol)

            print("[TRANSFORM] Calculating approximate KES value...")

            data = transform_crypto_price(symbol=symbol,price_usdt=crypto_price,usd_kes_rate=usd_kes_rate)
            results.append(data)
        load_data(results, args.output)


    except Exception as error:
        logger.error("Unexpected error occurred in run_main_pipeline function {}".format(str(error)),exc_info=True)
        print(f"ERROR: {error}")
        sys.exit(1)
    else:
        logging.info("crypto pipeline has been executed successfully!")


if __name__ == "__main__":
    logging.info("main_pipeline function started")
    run_main_pipeline()


