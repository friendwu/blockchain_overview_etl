from blockchainetl.jobs.base_job import BaseJob
from overviewetl.utils.defillama import DefillamaAPI

MODE_LATEST = "LATEST"
MODE_HISTORICAL = "HISTORICAL"


class ExportDefillamaChainTvl(BaseJob):
    def __init__(
        self,
        slug,
        data_range_mode,
        item_exporter,
    ):
        self.item_exporter = item_exporter
        self.defillama_api = DefillamaAPI()

        if data_range_mode not in [MODE_LATEST, MODE_HISTORICAL]:
            raise Exception(f"invalid data range mode: {data_range_mode}")

        self.data_range_mode = data_range_mode

        if self.data_range_mode == MODE_HISTORICAL and slug is None:
            raise Exception(f"missing chain in {self.data_range_mode}")

        self.slug = slug

    def _start(self):
        self.item_exporter.open()

    def _export(self):
        if self.data_range_mode == MODE_LATEST:
            res = self.defillama_api.get_latest_chain_tvls()
        else:
            res = self.defillama_api.get_historical_chain_tvl(self.slug)

        items = [{**e.asdict(), "type": "defillama_chain_tvl"} for e in res]

        self.item_exporter.export_items(items)

    def _end(self):
        # self.defillama_api.close()
        self.item_exporter.close()
