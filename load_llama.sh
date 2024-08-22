PG_URL=<YOUR PG URL>
# defillama, dydx/sui/sei not available
for slug in Bitcoin Ethereum Optimism Binance Aurora Oasis Polygon Avalanche OKExChain Cronos Fantom Tron Moonbeam Acala Ronin Canto Polkadot Solana Aptos TON Cosmos; do
	echo "----------------- start to export defillama: $slug -----------------"
	echo "python ./overviewetl.py export_defillama_chain_tvl --slug $slug --data-range-mode HISTORICAL --output-file data/defillama/llama_historical_$slug.csv --pg-url $PG_URL"
	python ./overviewetl.py export_defillama_chain_tvl --slug $slug --data-range-mode HISTORICAL --output-file data/defillama/llama_historical_$slug.csv --pg-url $PG_URL"
done



