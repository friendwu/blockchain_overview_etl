#!/bin/bash

python ./overviewetl.py extract_chain_stats  -c data/cmc  -l data/defillama -s data/stakingrewards --output-file chain_stats.csv --pg-url "postgresql://superset:superset@127.0.0.1/superset"
# python ./overviewetl.py extract_chain_stats  -c data/cmc  -l data/defillama -s data/stakingrewards --output-file chain_stats.csv
