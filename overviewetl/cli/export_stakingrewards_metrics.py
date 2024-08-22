import click

from blockchainetl.logging_utils import logging_basic_config
from overviewetl.jobs.export_stakingrewards_staking import \
    ExportStakingRewardsStaking
from overviewetl.jobs.exporters.stakingrewards_staking_item_exporter import \
    stakingrewards_staking_item_exporter

logging_basic_config()


@click.command()
@click.option(
    "--slug", required=True, type=str, help="chain name, eg: Cardano, Ethereum-2-0"
)
@click.option(
    "--data-range-mode",
    type=click.Choice(["7D", "30D", "90D"], case_sensitive=False),
    help="data range mode",
)
@click.option("--output-file", default=None, help="output file")
@click.option("--pg-url", default=None, help="postgres url")
def export_stakingrewards_staking(slug, data_range_mode, output_file, pg_url):
    job = ExportStakingRewardsStaking(
        slug,
        data_range_mode,
        stakingrewards_staking_item_exporter(output_file, pg_url),
    )
    job.run()
