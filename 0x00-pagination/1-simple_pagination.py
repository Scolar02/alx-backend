#!/usr/bin/env python3
"""Pagination helper module.
"""
import csv
from typing import List, Tuple


def index_range(page: int, page_size: int) -> Tuple[int, int]:
    """Calculate the start and end index for pagination.

    Args:
        page (int): The page number (1-indexed).
        page_size (int): The number of items per page.

    Returns:
        Tuple[int, int]: A tuple containing the start index and end index.
    """
    start = (page - 1) * page_size
    end = start + page_size
    return start, end


class Server:
    """Server class to paginate a database of popular baby names.
    """
    DATA_FILE = "Popular_Baby_Names.csv"

    def __init__(self):
        """Initialize the Server instance and dataset.
        """
        self.__dataset = None

    def dataset(self) -> List[List]:
        """Load and cache the dataset if not already loaded.

        Returns:
            List[List]: The dataset as a list of rows.
        """
        if self.__dataset is None:
            with open(self.DATA_FILE) as f:
                reader = csv.reader(f)
                dataset = [row for row in reader]
            self.__dataset = dataset[1:]  # Skip header

        return self.__dataset

    def get_page(self, page: int = 1, page_size: int = 10) -> List[List]:
        """Retrieve a page of the dataset.

        Args:
            page (int): The page number (1-indexed). Defaults to 1.
            page_size (int): The number of items per page. Defaults to 10.

        Returns:
            List[List]: A list of rows for the given page, or an empty list if out of range.
        """
        # Validate arguments
        assert isinstance(
            page, int) and page > 0, "Page must be a positive integer"
        assert isinstance(
            page_size, int) and page_size > 0, "Page size must be a positive integer"

        # Retrieve dataset
        data = self.dataset()

        # Calculate indices for pagination
        start, end = index_range(page, page_size)

        # Return the subset of the dataset or an empty list if out of range
        return data[start:end] if start < len(data) else []
