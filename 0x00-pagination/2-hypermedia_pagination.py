#!/usr/bin/env python3
"""Hypermedia Pagination with Deletion Resilience
"""
import csv
from typing import Dict, List


class Server:
    """A class to handle pagination for a dataset of popular baby names.
    """
    DATA_FILE = "Popular_Baby_Names.csv"

    def __init__(self):
        """Initialize the Server instance with cached dataset and indexed dataset.
        """
        self.__dataset = None
        self.__indexed_dataset = None

    def dataset(self) -> List[List]:
        """Load and cache the dataset if not already cached.

        Returns:
            List[List]: The dataset as a list of rows, excluding the header.
        """
        if self.__dataset is None:
            with open(self.DATA_FILE) as file:
                reader = csv.reader(file)
                dataset = [row for row in reader]
            self.__dataset = dataset[1:]  # Skip header row

        return self.__dataset

    def indexed_dataset(self) -> Dict[int, List]:
        """Create and cache an indexed dataset.

        Returns:
            Dict[int, List]: A dictionary mapping index positions to rows of the dataset.
        """
        if self.__indexed_dataset is None:
            dataset = self.dataset()
            self.__indexed_dataset = {
                i: dataset[i] for i in range(len(dataset))
            }
        return self.__indexed_dataset

    def get_hyper_index(self, index: int = 0, page_size: int = 10) -> Dict:
        """Get a paginated view of the dataset with deletion resilience.

        Args:
            index (int): The starting index for pagination.
            page_size (int): The number of items to include per page.

        Returns:
            Dict: A dictionary with the pagination details including:
                - 'index': The starting index.
                - 'next_index': The index to start the next page, if any.
                - 'page_size': The number of items in the current page.
                - 'data': The list of items in the current page.
        """
        data = self.indexed_dataset()
        assert index is not None and index >= 0 and index <= max(data.keys()), "Index out of bounds"
        
        page_data = []
        data_count = 0
        next_index = None

        for i, item in data.items():
            if i >= index and data_count < page_size:
                page_data.append(item)
                data_count += 1
                if data_count == page_size:
                    next_index = i + 1
                    break
        
        return {
            'index': index,
            'next_index': next_index,
            'page_size': len(page_data),
            'data': page_data,
        }
