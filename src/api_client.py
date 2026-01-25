"""API client for fetching stock data from EODData API"""

import requests
from typing import Dict, List, Any
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class StockAPIClient:
    """Client for fetching stock data from EODData API"""

    VALID_EXCHANGES = ["NASDAQ", "NYSE"]

    def __init__(self, api_key: str, base_url: str = "https://api.eoddata.com"):
        """
        Initialize the API client.

        Args:
            api_key: API key for authentication
            base_url: Base URL for the API endpoint
        """
        self.api_key = api_key
        self.base_url = base_url
        self.session = requests.Session()

    def get_exchange_quotes(
        self,
        exchange: str,
        date_stamp: str = None
    ) -> List[Dict[str, Any]]:
        """
        Fetch all stock quotes for a given exchange.

        Args:
            exchange: Exchange code ('NASDAQ' or 'NYSE')
            date_stamp: Optional date in format 'YYYY-MM-DD'. Defaults to current date.

        Returns:
            List of dictionaries containing stock quote data
        """
        # Validate exchange code
        if exchange not in self.VALID_EXCHANGES:
            logger.error(f"Invalid exchange code: {exchange}. Valid codes are: {', '.join(self.VALID_EXCHANGES)}")
            return []

        # Use current date if not specified
        if not date_stamp:
            date_stamp = datetime.now().strftime("%Y-%m-%d")

        # EODData API endpoint format: /Quote/List/{exchangeCode}
        endpoint = f"{self.base_url}/Quote/List/{exchange}"
        params = {
            "ApiKey": self.api_key,
            "DateStamp": date_stamp
        }

        try:
            logger.info(f"Fetching quotes for exchange: {exchange} on date: {date_stamp}")
            response = self.session.get(endpoint, params=params, timeout=30)
            response.raise_for_status()
            data = response.json()

            if isinstance(data, dict) and "error" in data:
                logger.error(f"API Error: {data['error']}")
                return []

            logger.info(f"Retrieved {len(data)} quotes from {exchange}")
            return data if isinstance(data, list) else []

        except requests.RequestException as e:
            logger.error(f"Request failed for exchange {exchange}: {str(e)}")
            return []

    def get_exchange_data(
        self,
        exchange: str,
        date_stamp: str = None
    ) -> List[Dict[str, Any]]:
        """
        Fetch all stock data for an exchange.

        Args:
            exchange: Exchange code
            date_stamp: Optional date in format 'YYYY-MM-DD'. Defaults to current date.

        Returns:
            List of stock data dictionaries
        """
        return self.get_exchange_quotes(exchange, date_stamp)
