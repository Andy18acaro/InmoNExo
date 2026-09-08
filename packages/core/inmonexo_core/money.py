from dataclasses import dataclass
import re

from inmonexo_core.enums import Currency

_MIL_PATTERN = re.compile(
    r"(?i)(?:desde\s+)?(?:precio\s+desde\s*:?\s*)?"
    r"(?:s/?\s*|pen\s*|soles?\s*)?"
    r"([\d.,]+)\s*(?:mil|k)\b"
)
_USD_PATTERN = re.compile(
    r"(?i)(?:desde\s+)?(?:usd|\$\s*|us\$)\s*([\d.,]+)\s*(?:mil|k)?\b"
)
_PEN_PATTERN = re.compile(
    r"(?i)(?:desde\s+)?(?:precio\s+desde\s*:?\s*)?"
    r"(?:s/?\s*|pen\s*|soles?\s*)"
    r"([\d.,]+)\b"
)


@dataclass(frozen=True, slots=True)
class Money:
    amount: int
    currency: Currency


def _parse_amount(raw: str, *, multiplier: int = 1) -> int:
    cleaned = raw.replace(",", "").replace(".", "")
    if not cleaned.isdigit():
        raise ValueError(f"Invalid numeric amount: {raw!r}")
    return int(cleaned) * multiplier


def parse_money(text: str) -> Money | None:
    """Parse Peruvian real-estate marketing price strings into Money."""
    if not text or not text.strip():
        return None

    normalized = " ".join(text.split())

    mil_match = _MIL_PATTERN.search(normalized)
    if mil_match:
        return Money(_parse_amount(mil_match.group(1), multiplier=1000), Currency.PEN)

    usd_match = _USD_PATTERN.search(normalized)
    if usd_match:
        amount_raw = usd_match.group(1)
        if re.search(r"(?i)(?:mil|k)\b", normalized[usd_match.end() : usd_match.end() + 8]):
            return Money(_parse_amount(amount_raw, multiplier=1000), Currency.USD)
        return Money(_parse_amount(amount_raw), Currency.USD)

    pen_match = _PEN_PATTERN.search(normalized)
    if pen_match:
        return Money(_parse_amount(pen_match.group(1)), Currency.PEN)

    return None
