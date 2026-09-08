import re

# Canonical Lima districts (subset for MVP seed sites)
_CANONICAL: frozenset[str] = frozenset(
    {
        "San Isidro",
        "Miraflores",
        "San Borja",
        "Surquillo",
        "Jesús María",
        "Magdalena",
        "Pueblo Libre",
        "Santa Beatriz",
        "Surco",
        "Chorrillos",
        "Barranco",
        "San Miguel",
        "Breña",
        "Cercado de Lima",
        "Santa Catalina",
    }
)

_ALIASES: dict[str, str] = {
    "san isidro": "San Isidro",
    "san-isidro": "San Isidro",
    "san isidro, lima": "San Isidro",
    "miraflores": "Miraflores",
    "san borja": "San Borja",
    "surquillo": "Surquillo",
    "jesus maria": "Jesús María",
    "jesús maría": "Jesús María",
    "magdalena": "Magdalena",
    "magdalena del mar": "Magdalena",
    "pueblo libre": "Pueblo Libre",
    "santa beatriz": "Santa Beatriz",
    "surco": "Surco",
    "santiago de surco": "Surco",
    "chorrillos": "Chorrillos",
    "barranco": "Barranco",
    "san miguel": "San Miguel",
    "brena": "Breña",
    "breña": "Breña",
    "cercado de lima": "Cercado de Lima",
    "lima cercado": "Cercado de Lima",
    "santa catalina": "Santa Catalina",
}


def normalize_district(raw: str | None) -> str | None:
    if not raw or not raw.strip():
        return None

    cleaned = re.sub(r"\s+", " ", raw.strip())
    if cleaned in _CANONICAL:
        return cleaned

    key = cleaned.lower().replace("ñ", "n") if "ñ" not in cleaned.lower() else cleaned.lower()
    # Try direct alias
    if key in _ALIASES:
        return _ALIASES[key]

    # Strip trailing ", Lima" / " - Lima"
    without_city = re.sub(r"[\s,\-]+lima\s*$", "", key, flags=re.IGNORECASE).strip()
    if without_city in _ALIASES:
        return _ALIASES[without_city]

    # Title-case fallback if it matches canonical after accent fix
    title = cleaned.title().replace("Jesus Maria", "Jesús María")
    if title in _CANONICAL:
        return title

    return cleaned if cleaned in _CANONICAL else None
