"""Run only CSV combination and cleanup operations."""

import json
import logging
import sys
from pathlib import Path

from dotenv import load_dotenv
from src.csv_processor import CSVProcessor
from src.logger import setup_logging


def load_config(config_file: str = "config/settings.json") -> dict:
    try:
        with open(config_file, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        raise FileNotFoundError(f"Config file not found: {config_file}")
    except json.JSONDecodeError:
        raise ValueError(f"Invalid JSON in config file: {config_file}")


def main() -> int:
    logger = setup_logging(log_level="INFO", log_file="stock_processor.log")

    # Load environment variables from project root .env for consistency with main.py
    load_dotenv(dotenv_path=Path(__file__).resolve().parent / ".env")

    config = load_config("config/settings.json")

    input_dir = config.get("daily_quotes_directory")
    output_dir = config.get("combined_quotes_directory")
    count_to_keep = config.get("count_of_files_to_keep")

    if not input_dir:
        logger.error("Missing daily_quotes_directory in config/settings.json")
        return 1
    if not output_dir:
        logger.error("Missing combined_quotes_directory in config/settings.json")
        return 1
    if count_to_keep is None:
        logger.error("Missing count_of_files_to_keep in config/settings.json")
        return 1

    processor = CSVProcessor(input_dir=input_dir, output_dir=output_dir, count_of_files_to_keep=count_to_keep)

    try:
        logger.info("Combining CSV files...")
        combined_file = processor.combine_csv_files()
        logger.info(f"Combined CSV file created at: {combined_file}")
    except Exception as exc:
        logger.error(f"Failed to combine CSV files: {exc}")
        return 1

    try:
        logger.info("Deleting old CSV files from input directory...")
        deleted_files = processor.delete_old_files_from_input_dir()
        logger.info(f"Deleted {len(deleted_files)} old file(s) from {input_dir}.")
    except Exception as exc:
        logger.error(f"Failed to delete old files: {exc}")
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
