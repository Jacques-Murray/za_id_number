"""
Test the ZAValidator class
"""

import pytest

from app.za_id_number.src.gender import GENDER
from app.za_id_number.src.validate import ValidationError
from app.za_id_number.src.za_validator import ZAValidator


class TestZAValidator:
    """
    Test the ZAValidator class
    """

    def test_clean_id_number(self, dummy_validator: ZAValidator):
        """
        Test the clean_id_number method
        """
        assert "8205055097080" == dummy_validator._clean_id_number(
            "820505 5097 08 0"
        )

        with pytest.raises(ValidationError):
            dummy_validator._clean_id_number("820505 509 708 0d")

    def test_correct_length(self, dummy_validator: ZAValidator):
        """
        Test the correct_length method
        """
        invalid_id = "820505509708"
        assert not dummy_validator._validate_str(invalid_id)

        valid_id = "8205055097080"
        assert dummy_validator._validate_str(valid_id)

    def test_invalid_dob(
        self,
        dummy_validator: ZAValidator,
        valid_id_numbers: list[str],
        invalid_date_id_numbers: list[str],
    ):
        """
        Test the _validate_date_of_birth method
        """
        for id_number in invalid_date_id_numbers:
            assert not dummy_validator._validate_date_of_birth(id_number)

        for id_number in valid_id_numbers:
            assert dummy_validator._validate_date_of_birth(id_number)

    def test_checksum(
        self, dummy_validator: ZAValidator, valid_id_numbers: list[str]
    ):
        """
        Test the _validate_checksum method
        """
        for id_number in valid_id_numbers:
            check_digit = int(id_number[-1])

            for i in range(10):
                test_id_number = id_number[:-1] + str(i)

                if i == check_digit:
                    assert dummy_validator._validate_checksum(test_id_number)
                else:
                    assert not dummy_validator._validate_checksum(
                        test_id_number
                    )

    def test_validate(
        self,
        validator: ZAValidator,
        valid_id_numbers: list[str],
        invalid_id_numbers: list[str],
        invalid_date_id_numbers: list[str],
        invalid_checksum_id_numbers: list[str],
    ):
        """
        Test the validate method
        """
        for id_number in valid_id_numbers:
            assert validator.validate(id_number)

        for id_number in invalid_id_numbers:
            assert not validator.validate(id_number)

        for id_number in invalid_date_id_numbers:
            assert not validator.validate(id_number)

        for id_number in invalid_checksum_id_numbers:
            assert not validator.validate(id_number)

    def test_generate_checksum(
        self, dummy_validator: ZAValidator, valid_id_numbers: list[str]
    ):
        """
        Test the _generate_checksum method
        """
        for id_number in valid_id_numbers:
            assert int(id_number[-1]) == dummy_validator.generate_checksum(
                id_number[:-1]
            )

    def test_parse_date_of_birth(
        self,
        dummy_validator: ZAValidator,
        valid_id_numbers: list[str],
        invalid_date_id_numbers: list[str],
    ):
        """
        Test the parse_date_of_birth method
        """
        for id_number in invalid_date_id_numbers:
            with pytest.raises(ValidationError):
                dummy_validator.parse_date_of_birth(id_number)

        for id_number in valid_id_numbers:
            date_of_birth = dummy_validator.parse_date_of_birth(id_number)
            assert date_of_birth.month == int(id_number[2:4])
            assert date_of_birth.day == int(id_number[4:6])

        date_of_birth = dummy_validator.parse_date_of_birth("8205055097080")
        assert date_of_birth.year == 1982

        date_of_birth = dummy_validator.parse_date_of_birth("1001015097080")
        assert date_of_birth.year == 2010

        date_of_birth = dummy_validator.parse_date_of_birth("0001015097080")
        assert date_of_birth.year == 2000

        date_of_birth = dummy_validator.parse_date_of_birth("5001015097080")
        assert date_of_birth.year == 1950

    def test_parse_gender(
        self,
        dummy_validator: ZAValidator,
        invalid_id_numbers: list[str],
        male_id_numbers: list[str],
        female_id_numbers: list[str],
    ):
        """
        Test the parse_gender method
        """
        for id_number in invalid_id_numbers:
            with pytest.raises(ValidationError):
                dummy_validator.parse_gender(id_number)

        for id_number in male_id_numbers:
            gender = dummy_validator.parse_gender(id_number)
            assert gender == GENDER.MALE

        for id_number in female_id_numbers:
            gender = dummy_validator.parse_gender(id_number)
            assert gender == GENDER.FEMALE
