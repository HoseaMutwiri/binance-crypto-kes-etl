
import argparse

def parse_arguments():
    """Looks at arguments that are after python3 main.py"""

    # create the argument parser

    parser = argparse.ArgumentParser(description="Binance Crypto Price ETL") # the desc will appear after --help

    parser.add_argument("--symbol",required=True,help="Crypto trading pair, e.g. BTCUSDT") #required =T means user must provide --symbol argument

    parser.add_argument("--output",
                        choices=["table", "json", "csv", "postgres"], 
                        default="table",
                        help="Output format: table, json, csv, or postgres") #the user can select one of the output option
    return parser.parse_args() # where argparse reads what the user typed





