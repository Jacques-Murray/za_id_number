"""
This module contains a pytest fixture for generating a list of invalid
South African ID numbers.
"""

import pytest


@pytest.fixture
def invalid_str_id_numbers():
    """
    Returns a list of invalid South African ID numbers with string
    errors.
    """
    return [
        "",
        " ",
        "1",
        "123",
        "123456",
        "123456789",
        "123456789012",
        "12345678901234",
        "12873678ad",
    ]


@pytest.fixture
def invalid_date_id_numbers():
    """
    Returns a list of invalid South African ID numbers with date
    errors.
    """
    return [
        "7514020004087",
        "7502326875085",
        "7113245929185",
        "7405325437186",
        "7702295556082",
    ]


@pytest.fixture
def male_id_numbers():
    """
    Returns a list of valid male South African ID numbers.
    """
    return [
        "0303068942075",
        "1701077451070",
        "5202049057182",
        "5906045026187",
        "8703209120170",
    ]


@pytest.fixture
def female_id_numbers():
    """
    Returns a list of valid female South African ID numbers.
    """
    return [
        "2904251790177",
        "1910252128177",
        "8711094861170",
        "5207272628088",
        "2802294751075",
    ]


@pytest.fixture
def invalid_checksum_id_numbers():
    """
    Returns a list of invalid South African ID numbers with checksum
    errors.
    """
    return ["7106245929181", "7405095437182", "7710165556083"]
