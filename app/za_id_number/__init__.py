"""
South African ID Number Validator
"""

from .src.citizenship import CITIZENSHIP
from .src.gender import GENDER
from .src.id_number_data import IDNumberData
from .src.validate import ValidationError, Validator
from .src.za_validator import ZAValidator

__all__ = [
    "CITIZENSHIP",
    "GENDER",
    "IDNumberData",
    "ValidationError",
    "Validator",
    "ZAValidator",
]
