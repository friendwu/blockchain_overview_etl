import click

from blockchainetl.logging_utils import logging_basic_config
from overviewetl.jobs.exporters.chain_stats_item_exporter import (
    chain_stats_item_exporter,
)
from overviewetl.jobs.extract_chain_stats import ExtractChainStats

logging_basic_config()


@click.command()
@click.option(
    "--cmc-input-file",
    "-c",
    type=str,
    default=None,
    help="cmc input file",
)
@click.option(
    "--llama-input-file",
    "-l",
    type=str,
    default=None,
    help="defillama input file",
)
@click.option(
    "--stakingrewards-input-file",
    "-s",
    type=str,
    default=None,
    help="stakingrewards input file",
)
@click.option("--output-file", type=str, default=None, help="file to be exported to")
@click.option(
    "--pg-url", type=str, default=None, help="postgresql db url to be exported to"
)
def extract_chain_stats(
    cmc_input_file, llama_input_file, stakingrewards_input_file, output_file, pg_url
):
    job = ExtractChainStats(
        item_exporter=chain_stats_item_exporter(output_file, pg_url),
        cmc_input_file=cmc_input_file,
        llama_input_file=llama_input_file,
        stakingrewards_input_file=stakingrewards_input_file,
    )
    job.run()
