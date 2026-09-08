import html as html_lib
import re
from urllib.parse import urljoin, urlparse


def clean_text(value: str) -> str:
    return html_lib.unescape(" ".join(value.split()))


def canonical_url(base: str, href: str) -> str:
    full = urljoin(base, href.strip())
    parsed = urlparse(full)
    path = parsed.path.strip("/")
    if not path:
        return f"{parsed.scheme}://{parsed.netloc}/"
    return f"{parsed.scheme}://{parsed.netloc}/{path}/"


def slug_to_title(slug: str) -> str:
    return " ".join(part.capitalize() for part in slug.split("-") if part)


def is_price(text: str) -> bool:
    return bool(re.search(r"(?i)s/\s*[\d.,]+|\$\s*[\d.,]+|usd\s*[\d.,]+", text))
