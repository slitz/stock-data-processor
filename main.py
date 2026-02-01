"""Main entry point for the Stock Data Processor application"""

import os
import sys
import json
import argparse
from pathlib import Path

from src.api_client import StockAPIClient
from src.csv_exporter import CSVExporter
from src.csv_processor import CSVProcessor
from src.logger import setup_logging


def load_config(config_file: str = "config/settings.json") -> dict:
    """
    Load configuration from JSON file.

    Args:
        config_file: Path to the configuration file

    Returns:
        Dictionary containing configuration settings
    """
    try:
        with open(config_file, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Config file not found: {config_file}")
        print("Please create config/settings.json with your API key and exchange codes")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"Invalid JSON in config file: {config_file}")
        sys.exit(1)


def main():
    """Main application entry point"""
    # Parse command-line arguments
    parser = argparse.ArgumentParser(
        description="Import stock data from EODData API and export to CSV",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
        ``Examples:
        python main.py                           # Use current date
        python main.py --date 2026-01-24         # Use specific date
        python main.py --date 2026-01-20 -v      # Verbose mode``
        """
    )
    parser.add_argument("--date", type=str, default=None, help="Date for quotes in format YYYY-MM-DD (default: current date)")
    parser.add_argument("-v", "--verbose",  action="store_true", help="Enable verbose logging (DEBUG level)")
    args = parser.parse_args()

    # Setup logging
    log_level = "DEBUG" if args.verbose else "INFO"
    logger = setup_logging(log_level=log_level, log_file="stock_processor.log")

    # Load configuration
    config = load_config("config/settings.json")

    # Validate configuration
    api_key = config.get("api_key")
    exchanges = config.get("exchanges", [])

    if not api_key:
        logger.error("API key not configured in settings.json")
        sys.exit(1)

    if not exchanges:
        logger.error("No exchanges configured in settings.json")
        sys.exit(1)

    # Initialize API client, exporter, and processor
    api_client = StockAPIClient(api_key=api_key)
    exporter = CSVExporter(daily_quotes_directory=config.get("daily_quotes_directory"))
    processor = CSVProcessor(input_dir=config.get("daily_quotes_directory"), 
                             output_dir=config.get("combined_quotes_directory"),
                             count_of_files_to_keep=config.get("count_of_files_to_keep"))
    
    # Get date from command-line argument (defaults to None for current date)
    date_stamp = args.date

    if date_stamp:
        logger.info(f"Starting stock data import for exchanges: {', '.join(exchanges)} on date: {date_stamp}")
    else:
        logger.info(f"Starting stock data import for exchanges: {', '.join(exchanges)} using current date")

    # Fetch and export data
    logger.info("Fetching stock quotes from EODData API...")
    exchange_data = {}
    for exchange in exchanges:
        exchange_data[exchange] = api_client.get_exchange_data(exchange, date_stamp)
    logger.info("Quotes fetched successfully!")

    logger.info("Exporting data to CSV...")
    csv_files = exporter.export_exchange_data(exchange_data, date_stamp)
    for exchange, filepath in csv_files.items():
        logger.info(f"{exchange}: data exported to {filepath}")

    # Process concatenation
    logger.info("Combining CSV files into a single file...")
    combined_file = processor.combine_csv_files()
    logger.info(f"Combined CSV file created at: {combined_file}")

    # Cleanup old files
    logger.info("Cleaning up old files from input directory...")
    files_deleted = processor.delete_old_files_from_input_dir()
    logger.info(f"Deleted {len(files_deleted)} old files from input directory.")
    return 0

if __name__ == "__main__":
    main()
