from sqlalchemy import Table, create_engine
from sqlalchemy.orm import declarative_base

from blockchainetl.jobs.exporters.composite_item_exporter import CompositeItemExporter
from blockchainetl.jobs.exporters.multi_item_exporter import MultiItemExporter
from blockchainetl.jobs.exporters.postgres_item_exporter import PostgresItemExporter
from blockchainetl.streaming.postgres_utils import create_insert_statement_for_table
from overviewetl.domain.token_market import TokenMarket

Base = declarative_base()


def token_market_item_exporter(output, pg_url):
    exporters = []

    if pg_url:
        engine = create_engine(pg_url)
        # table definition auto-detection, from here:
        # https://stackoverflow.com/questions/72714556/sqlalchemy-orm-get-table-definition-from-db
        table = Table(
            "token_markets",
            Base.metadata,
            autoload_with=engine,
            schema="blockchain_overview",
        )

        exporters.append(
            PostgresItemExporter(
                pg_url,
                {"token_market": create_insert_statement_for_table(table)},
                print_sql=False,
            )
        )

    if output:
        exporters.append(
            CompositeItemExporter(
                filename_mapping={
                    "token_market": output,
                },
                field_mapping={
                    "token_market": TokenMarket.fields,
                },
            )
        )

    return MultiItemExporter(exporters)
