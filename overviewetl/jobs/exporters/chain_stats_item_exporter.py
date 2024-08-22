from sqlalchemy import Table, create_engine
from sqlalchemy.orm import declarative_base

from blockchainetl.jobs.exporters.composite_item_exporter import CompositeItemExporter
from blockchainetl.jobs.exporters.multi_item_exporter import MultiItemExporter
from blockchainetl.jobs.exporters.postgres_item_exporter import PostgresItemExporter
from blockchainetl.streaming.postgres_utils import create_insert_statement_for_table
from overviewetl.domain.chain_stats import ChainStats

Base = declarative_base()


# TODO: merge code with token_market_item_exporter.
def chain_stats_item_exporter(output, pg_url):
    exporters = []

    if pg_url:
        engine = create_engine(pg_url)
        # table definition auto-detection, reference:
        # https://stackoverflow.com/questions/72714556/sqlalchemy-orm-get-table-definition-from-db
        table = Table(
            "chain_stats",
            Base.metadata,
            autoload_with=engine,
            schema="blockchain_overview",
        )

        exporters.append(
            PostgresItemExporter(
                pg_url,
                {"chain_stats": create_insert_statement_for_table(table)},
                print_sql=False,
            )
        )

    if output:
        exporters.append(
            CompositeItemExporter(
                filename_mapping={
                    "chain_stats": output,
                },
                field_mapping={
                    "chain_stats": ChainStats.fields,
                },
            )
        )

    return MultiItemExporter(exporters)
