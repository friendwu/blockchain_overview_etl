import json
from datetime import datetime

from overviewetl.domain.defillama import DefillamaChainTvl
from overviewetl.enumeration.chains import format_chain

from .http import make_retryable_session


class DefillamaAPI(object):
    def __init__(self):
        self.session = make_retryable_session()

        # key: chain name, value: dict("gecko_id", "cmc_id", "lama_id", "token_symbol", "tvl")
        self.chain_map = {}
        self.update_chain_map()

    def __request_defillama_api(self, path, params):
        url = f"https://api.llama.fi{path}"

        # TODO use retry session.
        response = self.session.get(url, params=params)
        data = json.loads(response.text)

        return data

    def update_chain_map(self):
        res = self.get_latest_chain_tvls()
        for e in res:
            self.chain_map[e.slug] = {
                "gecko_id": e.gecko_id,
                "cmc_id": e.cmc_id,
                "symbol": e.symbol,
                "tvl": e.tvl,
                "llama_id": e.llama_id,
            }

        return self.chain_map

    # get current tvl of all chains.
    def get_latest_chain_tvls(self):
        res = self.__request_defillama_api("/chains", None)
        return [
            DefillamaChainTvl(
                cmc_id=int(e["cmcId"] or -1),
                gecko_id=e["gecko_id"],
                llama_id=e["chainId"],
                symbol=e["tokenSymbol"],
                chain=format_chain(e["name"]),
                slug=e["name"],
                timestamp=datetime.now().timestamp(),
                datetime=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                tvl=e["tvl"],
            )
            for e in res
        ]

    # get historical tvl of specified chain.
    # TODO variable chain should be renamed to defillama_chain.
    def get_historical_chain_tvl(self, slug):
        res = self.__request_defillama_api(f"/charts/{slug}", None)

        return [
            DefillamaChainTvl(
                cmc_id=self.chain_map[slug]["cmc_id"],
                gecko_id=self.chain_map[slug]["gecko_id"],
                llama_id=self.chain_map[slug]["llama_id"],
                symbol=self.chain_map[slug]["symbol"],
                chain=format_chain(slug),
                slug=slug,
                timestamp=int(e["date"]),
                datetime=datetime.fromtimestamp(int(e["date"])).strftime(
                    "%Y-%m-%d %H:%M:%S"
                ),
                tvl=e["totalLiquidityUSD"],
            )
            for e in res
        ]
