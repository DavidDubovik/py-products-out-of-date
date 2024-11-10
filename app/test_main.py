import datetime
import pytest
from unittest.mock import patch
from freezegun import freeze_time
from app.main import outdated_products


@pytest.mark.parametrize(
    "products, expected", [
        (
            [
                {
                    "name": "salmon",
                    "expiration_date": datetime.date(2022, 2, 10),
                    "price": 600,
                },
                {
                    "name": "chicken",
                    "expiration_date": datetime.date(2022, 2, 5),
                    "price": 120,
                },
                {
                    "name": "duck",
                    "expiration_date": datetime.date(2022, 2, 1),
                    "price": 160,
                },
            ],
            ["duck"],
        ),
        ([], []),
        (
            [
                {
                    "name": "salmon",
                    "expiration_date": datetime.date(2022, 2, 2),
                    "price": 600,
                },
                {
                    "name": "chicken",
                    "expiration_date": datetime.date(2022, 1, 5),
                    "price": 120,
                },
                {
                    "name": "duck",
                    "expiration_date": datetime.date(2022, 2, 1),
                    "price": 160,
                },
            ],
            ["chicken", "duck"],
        ),
    ]
)
@freeze_time("2022-02-02")
@patch("datetime.date.today")
def test_outdated_products(
    mock_today: patch, products: list[dict], expected: list[str]
) -> None:
    mock_today.return_value = datetime.date(2022, 2, 2)

    result = outdated_products(products)
    assert result == expected
