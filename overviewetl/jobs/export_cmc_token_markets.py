from blockchainetl.jobs.base_job import BaseJob
from overviewetl.utils.coinmarketcap import CoinmarketcapAPI


class ExportCmcTokenMarketsFromChart(BaseJob):
    def __init__(
            self, item_exporter, cmc_slug, data_range_mode, api_key, currency_map_cache_file
    ):
        self.cmc_slug = cmc_slug
        self.data_range_mode = data_range_mode
        self.cmc_api = CoinmarketcapAPI(api_key, currency_map_cache_file)
        self.item_exporter = item_exporter

        self.currency_map = self.cmc_api.get_currency_map()
        if not self.currency_map.get(cmc_slug):
            raise Exception(f"cannot find {cmc_slug} in currency map")

    def _start(self):
        self.item_exporter.open()

    def _export(self):
        res = self.cmc_api.get_historical_token_markets(
            self.cmc_slug, self.data_range_mode
        )

        items = [{**e.asdict(), "type": "cmc_token_market"} for e in res]

        self.item_exporter.export_items(items)

    def _end(self):
        self.item_exporter.close()
        self.cmc_api.close()


class ExportCmcTokenMarketsFromListings(BaseJob):
    def __init__(
            self, item_exporter, data_range_mode, date, api_key, currency_map_cache_file
    ):
        self.data_range_mode = data_range_mode
        self.cmc_api = CoinmarketcapAPI(api_key, currency_map_cache_file)
        self.item_exporter = item_exporter
        self.date = date

        # self.currency_map = self.cmc_api.get_currency_map()

    def _start(self):
        self.item_exporter.open()

    def _export(self):
        if self.data_range_mode == "LATEST":
            res = self.cmc_api.listings_latest_token_markets()
        else:
            res = self.cmc_api.listings_historical_token_markets(self.date)

        items = []
        for e in res:
            item = e.asdict()
            item["type"] = "cmc_token_market"

            items.append(item)

        self.item_exporter.export_items(items)

    def _end(self):
        self.item_exporter.close()
        self.cmc_api.close()
