## Description
A blockchain data etl library(imitating ethereum-etl's code structure) that support crawling coinmarketcap/defillama/stakingrewards data and export them into Postgresql database or local fs.

For detailed data format, please refer path **schemas/pg/overview.sql**.

## Usage

```
python ./overviewetl.py --help
python ./overviewetl.py export_cmc_token_markets_from_chart --help
python ./overviewetl.py export_cmc_token_markets_from_chart --cmc-id 1 --cmc-api-key $CMC_API_KEY  --data-range-mode 1D --output-file <file.csv/json>

python ./overviewetl.py export_cmc_token_markets_from_chart --cmc-slug ethereum  --cmc-api-key $CMC_API_KEY --data-range-mode 1D --cmc-currency-map-cache-file ./currency_map_cache.json --output-file cmc_token_market_chart.csv
python ./overviewetl.py export_cmc_token_markets_from_listings    --cmc-api-key $CMC_API_KEY --data-range-mode LATEST --currency-map-cache-file ./currency_map_cache.json --output-file cmc_token_market_listing.csv

python ./overviewetl.py export_defillama_chain_tvl --chain Ethereum --data-range-mode HISTORICAL --output-file defillama_chain_tvl_historical.csv

python ./overviewetl.py export_defillama_chain_tvl --chain Ethereum --data-range-mode LATEST --output-file defillama_chain_tvl_latest.csv

python ./overviewetl.py export_stakingrewards_staking --chain cardano --data-range-mode 7D --output-file 3.csv
```

For detailed cli parameters, please refer path **overviewetl/cli/**
