import click

from overviewetl.cli.export_cmc_metrics import (
    export_cmc_token_markets_from_chart,
    export_cmc_token_markets_from_listings,
)
from overviewetl.cli.export_defillama_metrics import export_defillama_chain_tvl
from overviewetl.cli.export_stakingrewards_metrics import export_stakingrewards_staking
from overviewetl.cli.extract_chain_stats import extract_chain_stats
from overviewetl.cli.extract_token_markets import extract_token_markets


@click.group()
@click.version_option(version="0.1.0")
@click.pass_context
def cli(ctx):
    pass


# export
cli.add_command(
    export_cmc_token_markets_from_chart, "export_cmc_token_markets_from_chart"
)
cli.add_command(
    export_cmc_token_markets_from_listings, "export_cmc_token_markets_from_listings"
)
cli.add_command(export_defillama_chain_tvl, "export_defillama_chain_tvl")
cli.add_command(export_stakingrewards_staking, "export_stakingrewards_staking")
cli.add_command(extract_token_markets, "extract_token_markets")
cli.add_command(extract_chain_stats, "extract_chain_stats")
