#!/usr/bin/env python3
"""Deletion-resilient hypermedia pagination
"""

import csv
from typing import Dict, List, Optional


class Server:
    """Server class to paginate a database of popular baby names.
    """
    DATA_FILE = "Popular_Baby_Names.csv"

    def __init__(self):
        """Initializes a new Server instance.
        """
        self.__dataset = None
        self.__indexed_dataset = None

    def dataset(self) -> List[List]:
        """Cached dataset
        """
        if self.__dataset is None:
            with open(self.DATA_FILE) as f:
                reader = csv.reader(f)
                dataset = [row for row in reader]
            self.__dataset = dataset[1:]

        return self.__dataset

    def indexed_dataset(self) -> Dict[int, List]:
        """Dataset indexed by sorting position, starting at 0
        """
        if self.__indexed_dataset is None:
            dataset = self.dataset()
            self.__indexed_dataset = {
                i: dataset[i] for i in range(len(dataset))
            }
        return self.__indexed_dataset

    def get_hyper_index(self, index: int = 0, page_size: int = 10) -> Dict:
        """Retrieves info about a page from a given index and with a
        specified size.
        """
        assert isinstance(
            index, int) and index >= 0, "Index must be a non-negative integer"
        assert isinstance(
            page_size, int) and page_size > 0, "Page size must be a positive integer"

        data = self.indexed_dataset()
        sorted_indexes = sorted(data.keys())

        # If index is out of the dataset bounds
        if index not in sorted_indexes:
            return {
                'index': index,
                'next_index': None,
                'page_size': 0,
                'data': []
            }

        # Collect the requested page data
        page_data = []
        next_index = None
        data_count = 0

        for i in sorted_indexes:
            if i >= index and data_count < page_size:
                page_data.append(data[i])
                data_count += 1
                next_index = i + 1
            elif data_count >= page_size:
                break

        return {
            'index': index,
            'next_index': next_index,
            'page_size': len(page_data),
            'data': page_data,
        }
