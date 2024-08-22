import json
from datetime import datetime

from overviewetl.domain.stakingrewards import StakingRewardsStaking
from overviewetl.enumeration.chains import format_chain

from .http import make_retryable_session


class StakingRewardsAPI:
    def __init__(self):
        self.session = make_retryable_session()

        headers = {
            # TODO: authorization.
            "authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJqdGkiOiJzdGFraW5ncmV3YXJkc2NvbSIsImlhdCI6MTYxNDc4MTI1NiwiaXNzIjoiU3Rha2luZ3Jld2FyZHMgUHVibGljIEFQSSJ9.J5KWXqargT77UCNisY7id8tG6ca3l0-9fY4nD-VTwJ8"
        }
        self.session.headers.update(headers)

    # mode in ['7d', '90d', '30d']
    def get_historical_staking(self, slug, mode):
        mode = mode.lower()

        dp = mode[:-1] if mode.endswith("d") else mode

        url = f"https://api-beta.stakingrewards.com/chart/asset/{slug}?days={dp}"

        r = self.session.get(url)
        data = json.loads(r.text)[mode]
        chain = format_chain(slug)

        res = {
            e["timestamp"]: StakingRewardsStaking(
                slug=slug,
                chain=chain,
                timestamp=e["timestamp"],
                datetime=datetime.utcfromtimestamp(e["timestamp"]).strftime(
                    "%Y-%m-%d %H:%M:%S"
                ),
                annual_earnings=e["value"],
            )
            for e in data["annual_earnings"]
        }

        for e in data["total_users"]:
            timestamp = e["timestamp"]

            staking = res.get(timestamp)

            if not staking:
                staking = StakingRewardsStaking(
                    slug=slug,
                    chain=chain,
                    timestamp=e["timestamp"],
                    datetime=datetime.utcfromtimestamp(e["timestamp"]).strftime(
                        "%Y-%m-%d %H:%M:%S"
                    ),
                    total_users=e["value"],
                )
            else:
                staking.total_users = e["value"]

            res[timestamp] = staking

        for e in data["valueLocked"]:
            timestamp = e["timestamp"]

            staking = res.get(timestamp)

            if not staking:
                staking = StakingRewardsStaking(
                    slug=slug,
                    chain=chain,
                    timestamp=e["timestamp"],
                    datetime=datetime.utcfromtimestamp(e["timestamp"]).strftime(
                        "%Y-%m-%d %H:%M:%S"
                    ),
                    value_locked=e["value"],
                )
            else:
                staking.value_locked = e["value"]

            res[timestamp] = staking

        for e in data["priceUsd"]:
            timestamp = e["timestamp"]

            staking = res.get(timestamp)

            if not staking:
                staking = StakingRewardsStaking(
                    slug=slug,
                    chain=chain,
                    timestamp=e["timestamp"],
                    datetime=datetime.utcfromtimestamp(e["timestamp"]).strftime(
                        "%Y-%m-%d %H:%M:%S"
                    ),
                    price=e["value"],
                )
            else:
                staking.price = e["value"]

            res[timestamp] = staking

        return sorted(res.values(), key=lambda e: e.timestamp)
