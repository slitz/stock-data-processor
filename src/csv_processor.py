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

    def __init__(self, input_dir: str, output_dir: str, count_of_files_to_keep: int):
        """
        Process CSV files in a directory.

        Args:
            input_dir (str): Directory containing CSV files.
            output_dir (str): Directory for the combined output CSV.
            count_of_files_to_keep (int): Number of recent files to keep when culling old files.
        """
        self.input_dir = input_dir
        self.output_dir = output_dir
        self.output_file = os.path.join(self.output_dir, "prices.csv")
        self.count_of_files_to_keep = count_of_files_to_keep

    def combine_csv_files(self):
        csv_files = [
            os.path.join(self.input_dir, file)
            for file in os.listdir(self.input_dir)
            if file.lower().endswith(".csv")
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
    
    def delete_old_files_from_input_dir(self) -> List[Path]:
        base = Path(self.input_dir).expanduser().resolve()

        if not base.exists():
            raise FileNotFoundError(f"Directory does not exist: {base}")
        if not base.is_dir():
            raise NotADirectoryError(f"Not a directory: {base}")

        # Gather only files (skip directories)
        files = [path for path in base.iterdir() if path.is_file()]

        # If there are <= count of files to keep, nothing to do
        if len(files) <= self.count_of_files_to_keep:
            return []

        # Sort by modification time (newest first)
        files.sort(key=lambda p: p.stat().st_mtime, reverse=True)

        # Files to keep (first `count_of_files_to_keep` files), files to delete (the rest)
        files_to_delete = files[self.count_of_files_to_keep:]

        deleted: List[Path] = []
        for file in files_to_delete:
            try:
                file.unlink()
                deleted.append(file)
            except FileNotFoundError:
                # File was already removed; skip
                continue
            except PermissionError as e:
                print(f"PermissionError: cannot delete {file} ({e})")
            except OSError as e:
                print(f"OSError: cannot delete {file} ({e})")

        return deleted

