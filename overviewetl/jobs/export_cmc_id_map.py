from blockchainetl.jobs.base_job import BaseJob


class ExportCmcIdMap(BaseJob):
    def __init__(self, api_key):
        self.api_key = api_key
        self.token_ids = ["ethereum"]

        pass

    def _start(self):
        pass

    def _export(self):
        pass

    def _end(self):
        pass
