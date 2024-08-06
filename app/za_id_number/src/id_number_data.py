"""
A data class for South African ID numbers.
"""

from dataclasses import dataclass
from datetime import date

from .citizenship import CITIZENSHIP
from .gender import GENDER


@dataclass
class IDNumberData:
    """
    A data class for South African ID numbers.
    """

    date_of_birth: date
    gender: GENDER
    sequence_number: int
    citizenship: CITIZENSHIP
    checksum: int
