# test_main.py

import datetime
import pytest
from unittest.mock import patch
from io import StringIO

from main import Book, Library, main  # Asegúrate de ajustar la importación según la estructura de tu proyecto

@pytest.fixture
def library_fixture():
    return Library()

def test_validate_quantity_positive(library_fixture):
    result = library_fixture.validate_quantity("5")
    assert result == 5

def test_validate_quantity_negative(library_fixture):
    result = library_fixture.validate_quantity("-3")
    assert result == -1

def test_checkout_books_successful(library_fixture):
    selections = [{"book_index": 0, "quantity": 2}]
    with patch("builtins.input", side_effect=["1"]):
        total_late_fees = library_fixture.checkout_books(selections)
        assert total_late_fees == 0
        assert library_fixture.books[0].quantity_available == 3
        assert library_fixture.books[0].checked_out == 2

def test_checkout_books_insufficient_quantity(library_fixture):
    selections = [{"book_index": 0, "quantity": 10}]
    with patch("builtins.input", side_effect=["1"]):
        total_late_fees = library_fixture.checkout_books(selections)
        assert total_late_fees == -1


if __name__ == "__main__":
    pytest.main()
