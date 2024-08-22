CMC_API_KEY=<YOUR CMC API KEY>
PG_URL=<YOUR PG URL>

for slug in bitcoin ethereum optimism-ethereum bnb aurora oasis-network polygon avalanche okb cronos fantom tron moonbeam acala ronin canto polkadot-new solana aptos nervos-network ton cosmos dydx; do
	echo "----------------- start to export cmc: $slug -----------------"
	echo "python ./overviewetl.py export_cmc_token_markets_from_chart --cmc-slug $slug  --cmc-api-key $CMC_API_KEY --data-range-mode ALL --cmc-currency-map-cache-file ./currency_map_cache.json --output-file ./data/cmc/cmc_chart_ALL_$slug.csv --pg-url $PG_URL"
	python ./overviewetl.py export_cmc_token_markets_from_chart --cmc-slug $slug  --cmc-api-key $CMC_API_KEY --data-range-mode ALL --cmc-currency-map-cache-file ./currency_map_cache.json --output-file ./data/cmc/cmc_chart_ALL_$slug.csv --pg-url $PG_URL
done


