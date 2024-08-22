import csv

from blockchainetl.jobs.base_job import BaseJob
from overviewetl.domain.coinmarketcap import CmcTokenMarket
from overviewetl.domain.token_market import TokenMarket


class ExtractTokenMarkets(BaseJob):
    def __init__(self, input_file, item_exporter):
        self.input_file = input_file
        self.item_exporter = item_exporter

    def _start(self):
        self.item_exporter.open()

    def _export(self):
        for file in self.input_file:
            with open(file, "r") as f:
                reader = csv.DictReader(f)
                cmc_items = [CmcTokenMarket(**row) for row in reader]

                chain_stats_items = [
                    TokenMarket(
                        cmc_id=e.cmc_id,
                        timestamp=e.timestamp,
                        symbol=e.symbol,
                        name=e.name,
                        total_supply=e.total_supply,
                    )  # TODO: complete all fields.
                    for e in cmc_items
                ]

                items = [{**e, "type": "token_markets"} for e in chain_stats_items]

                self.item_exporter.export_items(items)

    def _end(self):
        self.item_exporter.close()
