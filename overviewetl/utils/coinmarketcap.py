import json
import os
from datetime import datetime

from overviewetl.domain.coinmarketcap import CmcTokenMarket
from overviewetl.enumeration.chains import format_chain
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium_stealth import stealth
from webdriver_manager.chrome import ChromeDriverManager

from .http import make_retryable_session

# import undetected_chromedriver as uc

DATA_RANGE_ALL = "ALL"
DATA_RANGE_YTD = "YTD"
DATA_RANGE_1Y = "1Y"
DATA_RANGE_3M = "3M"
DATA_RANGE_1M = "1M"
DATA_RANGE_7D = "7D"
DATA_RANGE_1D = "1D"

MODES = [
    DATA_RANGE_ALL,
    DATA_RANGE_YTD,
    DATA_RANGE_1Y,
    DATA_RANGE_3M,
    DATA_RANGE_1M,
    DATA_RANGE_7D,
    DATA_RANGE_1D,
]


class CoinmarketcapAPI(object):
    def __init__(self, api_key, currency_map_cache_file):
        self.api_key = api_key
        headers = {
            "Accepts": "application/json",
            "X-CMC_PRO_API_KEY": self.api_key,
        }

        self.session = make_retryable_session()
        self.session.headers.update(headers)
        self.browser = None
        self.currency_map_cache_file = currency_map_cache_file

        if currency_map_cache_file and (os.path.exists(currency_map_cache_file) and os.path.getsize(
                currency_map_cache_file) > 0):
            self.currency_map = json.load(open(currency_map_cache_file, "rb"))
        else:
            self.currency_map = self.load_currency_map()
            if currency_map_cache_file:
                with open(self.currency_map_cache_file, "w") as f:
                    json.dump(self.currency_map, f)

    def __init_selenium(self):
        # https://www.usessionbuddy.com/post/How-To-Install-Selenium-Chrome-On-Centos-7/
        options = webdriver.ChromeOptions()
        options.headless = True
        options.add_argument("start-maximized")
        options.add_argument("--remote-debugging-port=9222")
        options.add_argument("--no-sandbox")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option("useAutomationExtension", False)
        service = ChromeService(ChromeDriverManager(cache_valid_range=365).install())
        self.browser = webdriver.Chrome(options=options, service=service)
        stealth(
            self.browser,
            languages=["en-US", "en"],
            vendor="Google Inc.",
            platform="Win32",
            webgl_vendor="Intel Inc.",
            renderer="Intel Iris OpenGL Engine",
            fix_hairline=True,
        )
        # self.browser = uc.Chrome(options=options)

    def __request_pro_api(self, path, params):
        url = f"https://pro-api.coinmarketcap.com{path}"

        response = self.session.get(url, params=params)
        data = json.loads(response.text)
        return data

    # return a dict, key: id, value format eg:
    # {
    #       "id": 23333,
    #       "name": "Okage Inu",
    #       "symbol": "OKAGE",
    #       "slug": "okage-inu",
    #       "rank": 3321,
    #       "displayTV": 1,
    #       "manualSetTV": 0,
    #       "tvCoinSymbol": "",
    #       "is_active": 1,
    #       "first_historical_data": "2023-01-27T17:59:00.000Z",
    #       "last_historical_data": "2023-01-29T02:09:00.000Z",
    #       "platform": {
    #         "id": 1027,
    #         "name": "Ethereum",
    #         "symbol": "ETH",
    #         "slug": "ethereum",
    #         "token_address": "0x8dfc8cc3201425669fae803e1eb125cddd4189ec"
    #       }
    # }
    def load_currency_map(self):
        # docs: https://coinmarketcap.com/api/documentation/v1/#operation/getV1CryptocurrencyMap
        path = "/v1/cryptocurrency/map"
        ids = self.__request_pro_api(path, params={})["data"]

        return {str(e["slug"]): e for e in ids}

    def get_currency_map(self):
        return self.currency_map

    def get_historical_token_markets(self, slug, mode):
        if mode not in MODES:
            raise Exception(f"invalid mode {mode}")

        if not self.currency_map.get(slug):
            raise Exception(f"token: {slug} info missing")

        cmc_info = self.currency_map[slug]

        if not self.browser:
            self.__init_selenium()

        self.browser.get(
            f"https://api.coinmarketcap.com/data-api/v3/cryptocurrency/detail/chart?id={cmc_info['id']}&range={mode}"
        )

        try:
            text = self.browser.find_element(by=By.XPATH, value="//pre").text
            points = json.loads(text)["data"]["points"]

            res = []
            for e in points.items():
                native, chain = self.__get_native_and_chain(slug)

                c = CmcTokenMarket(
                    timestamp=int(e[0]),
                    datetime=datetime.utcfromtimestamp(int(e[0])).strftime(
                        "%Y-%m-%d %H:%M:%S"
                    ),  # TODO.
                    cmc_id=cmc_info["id"],
                    slug=slug,
                    native=native,
                    chain=chain,
                    name=cmc_info["name"],
                    symbol=cmc_info["symbol"],
                    price=e[1]["v"][0],
                    volume_24h=e[1]["v"][1],
                    market_cap=e[1]["v"][2],
                    # rank=int(e[1]["v"][3]),  # FIXME this is not rank.
                    circulating_supply=e[1]["v"][4],
                )
                res.append(c)

            return sorted(res, key=lambda e: e.timestamp)
        except Exception as e:
            raise Exception(
                f"failed to get token price of {cmc_info['slug']}:{slug}, {e}"
            )

    def __get_native_and_chain(self, slug):
        cmc_info = self.currency_map[slug]
        platform = cmc_info["platform"]
        native = False
        chain = None

        if not platform:
            native = True
            chain = cmc_info["slug"]
        else:
            platform_id = platform["id"]
            chain = platform["slug"]
            if platform_id == cmc_info["id"]:
                native = True

        c = format_chain(chain)

        return native, c

    def __convert_listing_item(self, raw):
        timestamp = int(
            datetime.strptime(raw["last_updated"], "%Y-%m-%dT%H:%M:%S.%fZ").timestamp()
        )

        native, chain = self.__get_native_and_chain(raw["slug"])

        return CmcTokenMarket(
            cmc_id=raw["id"],
            slug=raw["slug"],
            name=raw["name"],
            symbol=raw["symbol"],
            num_market_pairs=raw["num_market_pairs"],
            timestamp=timestamp,
            datetime=datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M:%S"),
            rank=raw["cmc_rank"],
            total_supply=raw["total_supply"],
            max_supply=raw.get("max_supply"),
            native=native,
            chain=chain,
            circulating_supply=raw["circulating_supply"],
            price=raw["quote"]["USD"].get("price"),
            market_cap=raw["quote"]["USD"].get("market_cap"),
            market_cap_dominance=raw["quote"]["USD"].get("market_cap_dominance"),
            fully_diluted_market_cap=raw["quote"]["USD"].get(
                "fully_diluted_market_cap"
            ),
            volume_24h=raw["quote"]["USD"].get("volume_24h"),
            # TODO: percent_change_1h/percent_change_24h/percent_change_7d
        )

    def listings_latest_token_markets(self):
        # docs: https://coinmarketcap.com/api/documentation/v1/#operation/getV1CryptocurrencyListingsLatest

        start = 1
        limit = 5000
        res = []

        while True:
            path = f"/v1/cryptocurrency/listings/latest?start={start}&limit={limit}"

            r = self.__request_pro_api(path, params={})["data"]

            if not r or len(r) == 0:
                break

            res.extend(
                [
                    self.__convert_listing_item(e)
                    for e in r
                    if e["slug"] in self.currency_map
                ]
            )

            start += limit

        return res

    def listings_historical_token_markets(self, date):
        # docs: https://coinmarketcap.com/api/documentation/v1/#operation/getV1CryptocurrencyListingsHistorical
        path = f"/v1/cryptocurrency/listings/historical?date={date}"

        start = 1
        limit = 5000
        res = []

        while True:
            r = self.__request_pro_api(path, params={}).get("data")
            if not r or len(r) == 0:
                break

            res.extend(
                [
                    self.__convert_listing_item(e)
                    for e in r
                    if e["slug"] in self.currency_map
                ]
            )
            start += limit

        return res

    def close(self):
        if self.browser:
            self.browser.quit()
