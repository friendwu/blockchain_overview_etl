PG_URL=<YOUR PG URL>
# arbitrum/optimism/starknet/zksync/okb/immutablex/ronin/nervos-network/ton/sei not available
for slug in ethereum-2-0 binance-smart-chain aurora-near oasis-network matic-network avalanche crypto-com-coin fantom tron moonbeam acala canto polkadot solana aptos cosmos dydx; do
	echo "----------------- start to export stakingrewards: $slug -----------------"
	echo "python ./overviewetl.py export_stakingrewards_staking --slug $slug --data-range-mode 90D --output-file data/stakingrewards/stakingrewards_90D_$slug.csv --pg-url $PG_URL"
	python ./overviewetl.py export_stakingrewards_staking --slug $slug --data-range-mode 90D --output-file data/stakingrewards/stakingrewards_90D_$slug.csv --pg-url $PG_URL"
done

#
# # not available: immutablex sui ton sei arbitrum starknet zksync
