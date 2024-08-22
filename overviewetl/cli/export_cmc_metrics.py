import click

from blockchainetl.logging_utils import logging_basic_config
from overviewetl.jobs.export_cmc_token_markets import (
    ExportCmcTokenMarketsFromChart,
    ExportCmcTokenMarketsFromListings,
)
from overviewetl.jobs.exporters.cmc_token_market_item_exporter import (
    cmc_token_market_item_exporter,
)

logging_basic_config()


@click.command()
@click.option(
    "--cmc-api-key",
    required=True,
    type=str,
    help="coinmarketcap API key",
)
@click.option("--cmc-slug", type=str, help="coinmarketcap slug")
@click.option(
    "--data-range-mode",
    required=True,
    type=click.Choice(
        ["1D", "7D", "1M", "3M", "1Y", "YTD", "ALL"], case_sensitive=False
    ),
    help="data range mode",
)
@click.option(
    "--cmc-currency-map-cache-file",
    default=None,
    help="coinmarketcap currency map cache file",
)
@click.option("--output-file", default=None, help="file to be exported to")
@click.option("--pg-url", default=None, help="postgres url")
def export_cmc_token_markets_from_chart(
    cmc_slug, cmc_api_key, data_range_mode, cmc_currency_map_cache_file, output_file, pg_url
):
    job = ExportCmcTokenMarketsFromChart(
        item_exporter=cmc_token_market_item_exporter(output_file, pg_url),
        cmc_slug=cmc_slug,
        data_range_mode=data_range_mode,
        api_key=cmc_api_key,
        currency_map_cache_file=cmc_currency_map_cache_file,
    )
    job.run()


@click.command()
@click.option(
    "--cmc-api-key",
    required=True,
    type=str,
    help="coinmarketcap API key",
)
@click.option(
    "--data-range-mode",
    required=True,
    type=click.Choice(["HISTORICAL", "LATEST"], case_sensitive=False),
    help="data range mode",
)
@click.option(
    "--date",
    type=str,
    default=None,
    help="historical date, needed in historical mode",  # TODO date format.
)
@click.option(
    "--currency-map-cache-file",
    type=str,
    default=None,
    help="coinmarketcap currency map cache file",
)
@click.option("--pg-url", default=None, help="postgres url")
@click.option("--output-file", type=str, default=None, help="file to be exported to")
def export_cmc_token_markets_from_listings(
    cmc_api_key, data_range_mode, date, currency_map_cache_file, output_file, pg_url
):
    job = ExportCmcTokenMarketsFromListings(
        item_exporter=cmc_token_market_item_exporter(output_file, pg_url),
        data_range_mode=data_range_mode,
        date=date,
        api_key=cmc_api_key,
        currency_map_cache_file=currency_map_cache_file,
    )
    job.run()
