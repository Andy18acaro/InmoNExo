from inmonexo_scrapers.base import BaseProvider
from inmonexo_scrapers.providers.albamar import AlbamarProvider
from inmonexo_scrapers.providers.grupomg import GrupoMgProvider
from inmonexo_scrapers.providers.hldi import HlProvider
from inmonexo_scrapers.providers.morada import MoradaProvider
from inmonexo_scrapers.providers.unio import UnioProvider

PROVIDERS: dict[str, BaseProvider] = {
    "hldi": HlProvider(),
    "grupomg": GrupoMgProvider(),
    "albamar": AlbamarProvider(),
    "unio": UnioProvider(),
    "morada": MoradaProvider(),
}

__all__ = [
    "AlbamarProvider",
    "GrupoMgProvider",
    "HlProvider",
    "MoradaProvider",
    "PROVIDERS",
    "UnioProvider",
]
