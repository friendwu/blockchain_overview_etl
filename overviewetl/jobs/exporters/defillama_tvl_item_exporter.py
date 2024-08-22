from overviewetl.domain.defillama import DefillamaChainTvl

from . import gen_multi_item_exporter


def defillama_chain_tvl_item_exporter(output, pg_url):
    return gen_multi_item_exporter(
        output,
        pg_url,
        "defillama_chain_tvl",
        "defillama_chain_tvls",
        DefillamaChainTvl.fields,
    )
