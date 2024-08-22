from dataclasses import dataclass

from .domain import Domain


@dataclass
class StakingRewardsStaking(Domain):
    timestamp: int
    datetime: str
    slug: str
    chain: str = None
    annual_earnings: int = None
    value_locked: int = None
    total_users: int = None
    price: float = None 
