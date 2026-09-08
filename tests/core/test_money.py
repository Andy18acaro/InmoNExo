import pytest

from inmonexo_core.enums import Currency
from inmonexo_core.money import parse_money


@pytest.mark.parametrize(
    ("raw", "amount", "currency"),
    [
        ("Desde S/ 350,000", 350_000, Currency.PEN),
        ("S/350K", 350_000, Currency.PEN),
        ("Precio desde: 350 mil soles", 350_000, Currency.PEN),
        ("USD 120,000", 120_000, Currency.USD),
        ("Desde S/ 268000", 268_000, Currency.PEN),
        ("S/ 292,769*", 292_769, Currency.PEN),
    ],
)
def test_parse_money(raw: str, amount: int, currency: Currency) -> None:
    result = parse_money(raw)
    assert result is not None
    assert result.amount == amount
    assert result.currency == currency


def test_parse_money_returns_none_for_empty() -> None:
    assert parse_money("") is None
    assert parse_money("Consultar precio") is None
