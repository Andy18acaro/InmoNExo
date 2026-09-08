import pytest

from inmonexo_core.district import normalize_district


@pytest.mark.parametrize(
    ("raw", "expected"),
    [
        ("San Isidro", "San Isidro"),
        ("SAN ISIDRO", "San Isidro"),
        ("san-isidro", "San Isidro"),
        ("San Isidro, Lima", "San Isidro"),
        ("Jesús María", "Jesús María"),
        ("jesus maria", "Jesús María"),
        ("Surco", "Surco"),
        ("Magdalena del Mar", "Magdalena"),
    ],
)
def test_normalize_district(raw: str, expected: str) -> None:
    assert normalize_district(raw) == expected


def test_normalize_district_unknown_returns_none() -> None:
    assert normalize_district("") is None
    assert normalize_district("Unknown Place XYZ") is None
