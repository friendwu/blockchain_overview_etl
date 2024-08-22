from dataclasses import dataclass

from .domain import Domain


@dataclass
class ChainStats(Domain):
    timestamp: int
    datetime: str
    chain: str
    cmc_id: int  = None
    gecko_id: str  = None
    llama_id: str = None
    nt_name: str = None
    nt_symbol: str = None
    nt_rank: int = None
    nt_total_supply: int = None
    nt_max_supply: int = None
    nt_circulating_supply: int = None
    nt_num_market_pairs: int = None
    nt_price: float = None
    nt_volume_24h: float = None
    nt_market_cap: float = None
    nt_fully_diluted_market_cap: float = None
    nt_market_cap_dominance: float = None

    tvl: int = None

    total_validators: int = None
    total_validator_staked: int = None
    annual_earnings: int = None
