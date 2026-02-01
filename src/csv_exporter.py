"""Module for exporting stock data to CSV format"""

import csv
from pathlib import Path
from typing import Dict, List, Any
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class CSVExporter:
    """Handles exporting stock data to CSV files"""

    def __init__(self, daily_quotes_directory: str = "data/daily_quotes"):
        """
        Initialize the CSV exporter.

        Args:
            daily_quotes_directory: Directory where daily CSV files will be saved
        """
        self.output_dir = Path(daily_quotes_directory)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def export_stock_data(self, exchange: str, data: List[Dict[str, Any]], date_stamp: str,) -> str:
        """
        Export stock quote data to a CSV file.

        Args:
            exchange: Exchange code
            data: List of dictionaries containing stock quote data
            date_stamp: str,

        Returns:
            Path to the created CSV file
        """
        filename = f"{exchange}_quotes_{date_stamp}.csv"

        filepath = self.output_dir / filename

        try:
            # EODData Quote List returns a list of records
            if not isinstance(data, list) or len(data) == 0:
                logger.warning(f"No data found for exchange {exchange}")
                return str(filepath)

            # Write to CSV with only symbol, date, and close columns
            with open(filepath, "w", newline="", encoding="utf-8") as csvfile:
                fieldnames = ["symbol", "date", "close"]
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

                writer.writeheader()

                # Write records, mapping EODData fields to desired output fields
                for record in data:
                    row = {
                        "symbol": record.get("symbolCode", ""),
                        "date": record.get("dateStamp", ""),
                        "close": record.get("close", "")
                    }
                    writer.writerow(row)

                logger.info(f"Exported {len(data)} quotes to {filepath}")

            return str(filepath)

        except Exception as e:
            logger.error(f"Failed to export data for {exchange}: {str(e)}")
            raise

    def export_exchange_data(self, exchange_data: Dict[str, List[Dict[str, Any]]], date_stamp: str) -> Dict[str, str]:
        """
        Export exchange quote data to CSV files.

        Args:
            exchange_data: Dictionary mapping exchange codes to their quote lists

        Returns:
            Dictionary mapping exchange codes to their CSV file paths
        """
        results = {}
        for exchange, data in exchange_data.items():
            results[exchange] = self.export_stock_data(exchange, data, date_stamp)

        return results
