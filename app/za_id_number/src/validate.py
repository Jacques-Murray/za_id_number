"""
This module contains the custom exception that is raised when the ID number is
invalid.
"""

from typing import Protocol

from .id_number_data import IDNumberData


class Validator(Protocol):
    """
    A protocol for the ID number validator
    """

    def validate(self, id_number: str) -> bool:
        """
        Validate the ID number
        """

    def parse_id_number_data(self, id_number: str) -> IDNumberData:
        """
        Parse the ID number data
        """


class ValidationError(Exception):
    """
    A custom exception that is raised when the ID number validation fails.
    """
