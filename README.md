## Binance Crypto Price ETL

A containerized Python ETL application that:

1. Extracts cryptocurrency prices from Binance
2. Extracts the USD/KES exchange rate from Frankfurter
3. Converts crypto prices from USDT to approximate KES
4. Loads results to the terminal, CSV, or PostgreSQL

### Docker Hub

Image: `hoseamutwiri/binance-etl:latest`

### Pull the image

```BASH
docker pull hoseamutwiri/binance-etl:latest
```

### Run

```BASH
docker run --rm hoseamutwiri/binance-etl:latest --symbol BTCUSDT
```

### Run Multiple symbols

```BASH
docker run --rm hoseamutwiri/binance-etl:latest --symbol BTCUSDT,ETHUSDT,SOLUSDT
```

### PostgreSQL

Create a `.env` file containing:

```TEXT
POSTGRES_HOST=
POSTGRES_PORT=
POSTGRES_DB=
POSTGRES_USER=
POSTGRES_PASSWORD=
```

Then run:

```BASH
docker run --rm --env-file .env hoseamutwiri/binance-etl:latest --symbol BTCUSDT --output postgres
```

### CSV

```BASH
# Create a data dir
mkdir -p data

# Then run
docker run --rm -v "$(pwd)/data:/app/data" hoseamutwiri/binance-etl:latest --symbol BTCUSDT,SOLUSDT --output csv
```
csv file will be in : `data/crypto_prices.csv`

### Logs

```BASH

# Create a logs dir

mkdir -p logs

# Then run

docker run --rm -v "$(pwd)/logs:/app/logs" hoseamutwiri/binance-etl:latest --symbol BTCUSDT
```

Logs will be available in: `logs/bin_crypto_pipeline.log`