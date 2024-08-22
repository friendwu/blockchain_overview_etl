from blockchainetl.jobs.base_job import BaseJob
from overviewetl.utils.stakingrewards import StakingRewardsAPI


class ExportStakingRewardsStaking(BaseJob):
    def __init__(self, slug, data_range_mode, item_exporter):
        self.slug = slug
        self.item_exporter = item_exporter
        self.stakingrewards_api = StakingRewardsAPI()
        self.data_range_mode = data_range_mode

    def _start(self):
        self.item_exporter.open()

    def _export(self):
        res = self.stakingrewards_api.get_historical_staking(
            self.slug, self.data_range_mode
        )

        items = [{**e.asdict(), "type": "stakingrewards_staking"} for e in res]

        self.item_exporter.export_items(items)

    def _end(self):
        self.item_exporter.close()
