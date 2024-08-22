from dataclasses import dataclass

from .domain import Domain


# TODO No need any more.
@dataclass(frozen=True)
class TokenMarket(Domain):
    cmc_id: int
    timestamp: int
    symbol: str
    name: str
    date: str = None
    rank: int = None

    total_supply: int = None
    max_supply: int = None
    circulating_supply: int = None
    num_market_pairs: int = None

    price: float = None
    volume_24h: float = None
    market_cap: float = None
    fully_diluted_market_cap: float = None
    market_cap_dominance: float = None
