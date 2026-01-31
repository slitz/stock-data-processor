"""Module for processing CSV files"""

import csv
import os
import pandas as pd
from pathlib import Path
from typing import Dict, List, Any
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class CSVProcessor:
    """Handles processing CSV files"""

    def __init__(self, input_dir: str, output_dir: str):
        """
        Combine all CSV files in a directory into a single CSV file.

        Args:
            input_dir (str): Directory containing CSV files.
            output_file (str): Path for the combined output CSV.
        """
        self.input_dir = input_dir
        self.output_dir = output_dir
        self.output_file = os.path.join(self.output_dir, "prices.csv")

    def combine_csv_files(self):
        csv_files = [
            os.path.join(self.input_dir, f)
            for f in os.listdir(self.input_dir)
            if f.lower().endswith(".csv")
        ]

        if not csv_files:
            raise FileNotFoundError("No CSV files found in the input directory.")

        data_frames = []
        for file in csv_files:
            data_frame = pd.read_csv(file)
            data_frames.append(data_frame)

        combined = pd.concat(data_frames, ignore_index=True, sort=False)
        combined.to_csv(self.output_file, index=False)

        return self.output_file


