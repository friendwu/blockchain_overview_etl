import click

from blockchainetl.logging_utils import logging_basic_config
from overviewetl.jobs.exporters.token_market_item_exporter import (
    token_market_item_exporter,
)
from overviewetl.jobs.extract_token_markets import ExtractTokenMarkets

logging_basic_config()


@click.command()
@click.option(
    "--input-file",
    "-i",
    type=str,
    default=None,
    help="coinmarketcap id map cache file",
)
@click.option("--output-file", type=str, default=None, help="file to be exported to")
@click.option(
    "--pg-url", type=str, default=None, help="postgresql db url to be exported to"
)
def extract_token_markets(input_file, output_file, pg_url):
    job = ExtractTokenMarkets(
        input_file=input_file,
        item_exporter=token_market_item_exporter(output_file, pg_url),
    )
    job.run()
