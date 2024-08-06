"""
South African ID number validator
"""

import re
from abc import ABC, abstractmethod
from datetime import date, datetime

from .citizenship import CITIZENSHIP
from .gender import GENDER
from .id_number_data import IDNumberData
from .validate import ValidationError

id_number_validation = re.compile(r"^\d{13}$")


class ZAValidator(ABC):
    """
    South African ID number validator
    """

    def _clean_id_number(self, id_number: str) -> str:
        """
        Remove any non-numeric characters from the ID number
        """
        cleaned_id_number = re.sub(r"\D", "", id_number)
        cleaned_id_number = cleaned_id_number.strip().replace(" ", "")

        if not self._validate_str(cleaned_id_number):
            raise ValidationError("Invalid ID number")

        return cleaned_id_number

    def _validate_str(self, id_number: str) -> bool:
        """
        Check if the ID number is a valid string
        """
        if not id_number_validation.match(id_number):
            return False

        return True

    def _fix_millenium(self, two_digit_year: int) -> int:
        """
        Fix the two-digit year to a four-digit year
        """
        current_year_two_digits = datetime.now().year % 100

        if two_digit_year < current_year_two_digits:
            return two_digit_year + 2000
        else:
            return two_digit_year + 1900

    def _validate_date_of_birth(self, id_number: str) -> bool:
        """
        Validate the date of birth in the ID number
        """
        day = int(id_number[4:6])
        month = int(id_number[2:4])
        year = int(id_number[0:2])
        year = self._fix_millenium(year)

        try:
            date_of_birth = date(year=year, month=month, day=day)
        except ValueError:
            return False

        if (
            date_of_birth.year == year
            and date_of_birth.month == month
            and date_of_birth.day == day
        ):
            return True

        return False

    def _validate_checksum(self, id_number: str) -> bool:
        """
        Validate the checksum of the ID number
        """
        check_digit = int(id_number[-1])

        return check_digit == self.generate_checksum(id_number)

    def generate_checksum(self, id_number: str) -> int:
        """
        Generate the checksum for the ID number
        """
        digits = list(map(int, str(id_number)))
        odd_digits = digits[-2::-2]
        even_digits = digits[-1::-2]

        checksum = 0
        checksum += sum(odd_digits)

        for digit in even_digits:
            checksum += sum(divmod(digit * 2, 10))

        return (10 - (checksum % 10)) % 10

    @abstractmethod
    def validate(self, id_number: str) -> bool:
        """
        Validate the ID number
        """
        if not self._validate_str(id_number=id_number):
            return False

        if not self._validate_date_of_birth(id_number=id_number):
            return False

        if not self._validate_checksum(id_number=id_number):
            return False

        return True

    def parse_date_of_birth(self, id_number: str) -> date:
        """
        Parse the date of birth from the ID number
        """
        if not self.validate(id_number=id_number):
            raise ValidationError("Invalid ID number")

        day = int(id_number[4:6])
        month = int(id_number[2:4])
        year = int(id_number[0:2])

        year = self._fix_millenium(year)

        return date(year=year, month=month, day=day)

    def parse_gender(self, id_number: str) -> GENDER:
        """
        Parse the gender from the ID number
        """
        if not self.validate(id_number=id_number):
            raise ValidationError("Invalid ID number")

        digit = id_number[6]

        if digit in ["0", "1", "2", "3", "4"]:
            return GENDER.FEMALE
        else:
            return GENDER.MALE

    def parse_checksum(self, id_number: str) -> int:
        """
        Parse the checksum from the ID number
        """
        if not self.validate(id_number=id_number):
            raise ValidationError("Invalid ID number")

        return int(id_number[-1])

    def parse_citizenship(self, id_number: str) -> CITIZENSHIP:
        """
        Parse the citizenship from the ID number
        """
        if not self.validate(id_number=id_number):
            raise ValidationError("Invalid ID number")

        digit = int(id_number[10:11])

        if digit == 8:
            return CITIZENSHIP.CITIZEN
        else:
            return CITIZENSHIP.PERMANENT_RESIDENT

    @abstractmethod
    def parse_id_number_data(self, id_number: str) -> IDNumberData:
        """
        Parse the ID number data
        """
        if not self.validate(id_number=id_number):
            raise ValidationError("Invalid ID number")

        return IDNumberData(
            date_of_birth=self.parse_date_of_birth(id_number=id_number),
            gender=self.parse_gender(id_number=id_number),
            sequence_number=int(id_number[7:12]),
            citizenship=self.parse_citizenship(id_number=id_number),
            checksum=self.parse_checksum(id_number=id_number),
        )
