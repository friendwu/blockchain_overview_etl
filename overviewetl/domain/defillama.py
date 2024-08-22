from dataclasses import dataclass

from .domain import Domain


@dataclass(frozen=True)
class DefillamaChainTvl(Domain):
    timestamp: int
    chain: str
    slug: str 
    datetime: str
    tvl: float = None
    cmc_id: int = None
    gecko_id: str = None
    llama_id: int = None
    symbol: str = None
