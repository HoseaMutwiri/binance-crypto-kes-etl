import logging
import logging.config
import json
import csv
import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()


# load the logging configuration file

logging.config.fileConfig(fname = 'config/logging.conf')

logger = logging.getLogger(__name__)



def load_table(data):

    """Print transformed crypto data as a table."""

    logger.info("Loading data to terminal")
    print()

    print("-" * 60)

    print("BINANCE CRYPTO PRICE")

    print("-" * 60)

    print(
        f"{'SYMBOL':<15}"
        f"{'USDT PRICE':>20}"
        f"{'APPROXIMATE KES':>25}")

    # print(f"{'Symbol:':<20}{data['symbol']}") # Left-align within 20 characters.

    # print(f"{'Price USDT:':<20}${data['price_usdt']:,.2f}") # Thousands separator + 2 decimal places.

    # print(f"{'USD/KES Rate:':<20}{data['usd_kes_rate']:,.2f}")

    # print(f"{'Approx. Price KES:':<20}KSh {data['price_kes']:,.2f}")
    for dat in data:
        print(
            f"{dat['symbol']:<15}"
            f"${dat['price_usdt']:>20,.2f}"
            f"      KSh {dat['price_kes']:>15,.2f}"
            )


    print("-" * 60)

    print("Source: Binance")

    print("Status: SUCCESS")

    print("-" * 60)






def load_json(data):

    """Print transformed crypto data as JSON."""

    logger.info(
        f"Loading {len(data)} crypto records as JSON"
    )

    print(json.dumps(data, indent=4))



def load_csv(data):
    """Write transformed crypto data to a CSV file."""
    logger.info(f"Loading {len(data)} crypto records to CSV")
    with open("data/crypto_prices.csv", "w", newline="") as file: #create/open a file in write mode

        columns = ["symbol","price_usdt","usd_kes_rate","price_kes","extracted_at"] #define the columns names
        writer = csv.DictWriter(file,fieldnames=columns)

        writer.writeheader() #create the columns

        writer.writerows(data) #write all the records

    print("CSV file created successfully: data/crypto_prices.csv")


def load_postgres(data):
    """Load transformed crypto data into PostgreSQL."""

    logger.info(f"Loading {len(data)} crypto records to PostgreSQL")

    connection = None # initiatialize connection we will close it later

    try:
        # establish a connection btwn app & postgresql
        connection = psycopg2.connect(
            host=os.getenv("POSTGRES_HOST"),
            port=os.getenv("POSTGRES_PORT"),
            database=os.getenv("POSTGRES_DB"),
            user=os.getenv("POSTGRES_USER"),
            password=os.getenv("POSTGRES_PASSWORD")
        )

        cursor = connection.cursor() # create cursor obeject



        insert_query = """
            INSERT INTO crypto_prices (
                symbol,
                price_usdt,
                usd_kes_rate,
                price_kes,
                extracted_at
            )
            VALUES (%s, %s, %s, %s, %s)
        """

        for record in data:
            cursor.execute(insert_query,
                (
                    record["symbol"],
                    record["price_usdt"],
                    record["usd_kes_rate"],
                    record["price_kes"],
                    record["extracted_at"]
                )
            )

        connection.commit()

        print(
            f"[LOAD] Successfully loaded "
            f"{len(data)} records into PostgreSQL."
        )

        cursor.close()

    except Exception as error:

        if connection: # if the connection was created the return value is TRue
            connection.rollback() # to allow redo prevents a partially completed transaction from being left behind

        logger.error(f"Unable to load data into PostgreSQL: {error}",exc_info=True)
        raise

    finally:
        if connection: #If a connection exists, close it
            connection.close()





def load_data(data, output):

    if output == "table":
        load_table(data)

    elif output == "json":
        load_json(data)

    elif output == "csv":
        load_csv(data)

    elif output == "postgres":
        load_postgres(data)