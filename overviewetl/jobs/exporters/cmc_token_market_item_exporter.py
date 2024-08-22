# from blockchainetl.jobs.exporters.composite_item_exporter import CompositeItemExporter
from overviewetl.domain.coinmarketcap import CmcTokenMarket

from . import gen_multi_item_exporter

# def cmc_token_market_item_exporter(output):
#     return CompositeItemExporter(
#         filename_mapping={
#             "cmc_token_market": output,
#         },
#         field_mapping={
#             "cmc_token_market": CmcTokenMarket.fields,
#         },
#     )


def cmc_token_market_item_exporter(output, pg_url):
    return gen_multi_item_exporter(
        output, pg_url, "cmc_token_market", "cmc_token_markets", CmcTokenMarket.fields
    )
