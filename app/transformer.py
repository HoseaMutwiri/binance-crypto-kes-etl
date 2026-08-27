import logging
import logging.config
from datetime import datetime


# load the logging configuration file

logging.config.fileConfig(fname = 'config/logging.conf')

logger = logging.getLogger(__name__)


def transform_crypto_price(symbol, price_usdt, usd_kes_rate):
    """This function converts a cryptocurrency price from USDT to approximate kes"""
    try:
        logger.info("Calculating approximate KES value for {}".format(str(symbol)))

        price_kes = price_usdt * usd_kes_rate
    except Exception as error:
        logger.error(f"Unable to calculate due to error {error}")
        raise
    else:
        logger.info(f"Calculation done and the price in kes is {price_kes}")

    return {
        "symbol": symbol,
        "price_usdt": round(price_usdt,2),
        "usd_kes_rate": round(usd_kes_rate,2),
        "price_kes": round(price_kes,2),
        "extracted_at": datetime.now().isoformat()
        }





