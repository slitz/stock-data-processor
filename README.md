# Stock Data Importer

A Python application that imports stock market data from the EODData API and exports it to CSV files.

## Features

- Fetch stock data from EODData API
- Support for multiple stock symbols and exchanges
- Export data to CSV format with timestamps
- Comprehensive logging
- Configuration via JSON settings file

## Project Structure

```
stock-data-importer/
├── src/
│   ├── __init__.py
│   ├── api_client.py       # API client for fetching stock data
│   ├── csv_exporter.py     # CSV export functionality
│   └── logger.py           # Logging configuration
├── config/
│   └── settings.json       # Configuration file (create before running)
├── output/                 # Directory for exported CSV files
├── main.py                 # Main application entry point
├── requirements.txt        # Python dependencies
├── .gitignore              # Git ignore rules
└── README.md              # This file
```

## Installation

1. **Clone or download the project:**
   ```bash
   cd stock-data-importer
   ```

2. **Create a virtual environment (recommended):**
   ```bash
   python -m venv venv
   # On Windows
   venv\Scripts\activate
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Configuration

1. **Get an API Token:**
   - Sign up at [EODData](https://www.eoddata.com/) for an API token

2. **Update `config/settings.json`:**
   ```json
   {
     "api_key": "YOUR_API_TOKEN_HERE",
     "base_url": "https://api.eoddata.com",
     "exchanges": ["NASDAQ", "NYSE"],
     "output_directory": "output"
   }
   ```

3. **Configuration Options:**
   - `api_key`: Your EODData API token
   - `base_url`: Base URL for the API (default: https://api.eoddata.com)
   - `exchanges`: List of exchange codes to fetch data from (valid values: NASDAQ, NYSE)
   - `output_directory`: Directory where CSV files will be saved

4. **Supported Exchange Codes:**
   - NASDAQ: NASDAQ Stock Exchange
   - NYSE: New York Stock Exchange

## Usage

Run the application from the command line:

```bash
# Use current date
python main.py

# Use a specific date
python main.py --date 2026-01-24

# Enable verbose logging
python main.py --date 2026-01-24 -v
```

**Command-line Options:**
- `--date YYYY-MM-DD`: Optional date for quotes. Overrides config file setting. If not provided, uses config file date or current date.
- `-v, --verbose`: Enable verbose (DEBUG) logging output

The application will:
1. Read configuration from `config/settings.json`
2. Override date if `--date` parameter is provided
3. Fetch all stock quotes for the specified exchange(s) from the EODData Quote List endpoint
4. Export the data to CSV files in the `output/` directory
5. Log all operations to console and `stock_importer.log`

## Output

CSV files will be generated in the `output/` directory with the naming format:
```
{EXCHANGE_CODE}_quotes_YYYYMMDD_HHMMSS.csv
```

Each CSV file contains three columns:
- **symbol**: Stock ticker symbol (e.g., AAPL, GOOGL)
- **date**: Quote date in format (e.g., 9-Dec-25)
- **close**: Closing price

Example:
```
symbol,date,close
AACB,9-Dec-25,10.3399
AACBR,9-Dec-25,0.3587
AACG,9-Dec-25,0.951
AADR,9-Dec-25,85.215
```

## Customization

### Using a Different API

To use a different stock API, modify the `StockAPIClient` class in `src/api_client.py`:
- Update the `base_url` parameter
- Adjust the `get_exchange_quotes()` method to match your API's endpoint and parameters
- Update the request parameters and response parsing
- Modify `csv_exporter.py` if the data structure is different from EODData's format

## Error Handling

The application includes error handling for:
- Missing API keys
- Network request failures
- Invalid API responses
- File I/O errors

All errors are logged to the console and log file for debugging.

## Logging

Logs are written to:
- **Console:** Real-time application output
- **File:** `stock_importer.log` (created on first run)

## License

This project is open source. Feel free to modify and use as needed.

## Support

For issues or questions:
1. Check the log file: `stock_importer.log`
2. Verify your API token in `config/settings.json`
3. Ensure valid exchange codes are used (NASDAQ or NYSE only)
4. Ensure you have internet connectivity
5. Check the EODData API rate limits and usage
