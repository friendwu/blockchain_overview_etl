import os

from overviewetl.utils.coinmarketcap import *

api_key = os.getenv("CMC_API_KEY")
api = CoinmarketcapAPI(api_key, "id_map_cache.json")

# print(json.dumps(api.get_currency_map(), indent=2))

# l = api.listings_latest_token_markets()

# print(json.dumps([e.asdict() for e in l], indent=2))

print(json.dumps(api.get_historical_token_markets("bitcoin", DATA_RANGE_7D), indent=2))

api.close()
