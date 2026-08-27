
# importing the libraries required 

import requests

import logging

import logging.config


# load the logging configuration file

logging.config.fileConfig(fname = 'config/logging.conf')

logger = logging.getLogger(__name__)


BIN_URL = "https://api.binance.com/api/v3/ticker/price"

FRANK_URL = "https://api.frankfurter.dev/v2/rate/USD/KES"


# Extract crypto currency price 

def get_crypto_price(symbol):
    """This function will call the latest cryptocurrency price from binance in USDT"""
    try:

        logger.info("Fetching {} price from Binance...".format(str(symbol)))

        print("[EXTRACT] Fetching {} from Binance...".format(str(symbol)))
        response = requests.get(url=BIN_URL,params={"symbol": symbol},timeout=10)
        response.raise_for_status()
        data = response.json()
        crypto_price = float(data["price"])

    except requests.exceptions.HTTPError:
        logger.error(f"Invalid Binance symbol or HTTP error for {symbol}")

        raise ValueError(f"{symbol} is not a valid Binance trading pair.")

    
    except requests.exceptions.RequestException as error:
        logger.error(f"Unable to connect to Binance API: {error}",exc_info=True)

        raise ConnectionError("Unable to connect to Binance API.\nPlease check your internet connection.")

    except Exception as error:
        logger.error("Unable to extract data from Binance due to error :{}".format(str(error)),exc_info=True)
        print()
        raise

    else:
        logger.info(f"The price has been fetched successfully:{crypto_price}")

    return crypto_price


# Extracting the current usd kes exchange rates

def get_usd_kes_rate():
    """This function will fetch the current USD/KES exchange rate"""
    try:
        logger.info("Fetching USD/KES exchange rate...")
        print("[EXTRACT] Fetching USD/KES exchange rate...")
        response = requests.get(url=FRANK_URL,timeout=10)
        response.raise_for_status()
        data = response.json()
        #print(data)
        usd_kes_rate = float(data["rate"])

    except requests.exceptions.RequestException as error:
        logger.error(f"Unable to connect to FrankFurter API: {error}",exc_info=True)
    
        raise ConnectionError("Unable to connect to FrankFurter API.\nPlease check your internet connection.")
    


    except Exception as error:
        logger.error("Unable to retrieve the USD/KES exchange rate :{}".format(str(error)),exc_info=True)
        raise
    else:
        logger.info(f"The kes usd exchange rate has been fetched successfully:{usd_kes_rate}")
    return usd_kes_rate




        


