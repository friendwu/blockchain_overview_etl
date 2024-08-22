import click

from blockchainetl.logging_utils import logging_basic_config
from overviewetl.jobs.export_defillama_tvl import ExportDefillamaChainTvl
from overviewetl.jobs.exporters.defillama_tvl_item_exporter import (
    defillama_chain_tvl_item_exporter,
)

logging_basic_config()


# defillama supported chains(2023-2-17)
# Ethereum,BSC,Tron,Arbitrum,Polygon,Avalanche,Optimism,Fantom,
# Solana,Cronos,Mixin,DefiChain,Klaytn,Kava,Algorand,Parallel,Acala,Osmosis,
# Canto,Fusion,Hedera,Celo,Bitcoin,Gnosis,Thorchain,Waves,Near,Moonbeam,Cardano,
# EOS,Astar,MultiversX,Aurora,Ronin,Heco,Aptos,NEO,Rootstock,Metis,OKExChain,KCC,
# Terra2,Telos,Tezos,Icon,Bifrost,Moonriver,IoTeX,Oasis,Stellar,Karura,Ontology,
# Stride,Tlchain,Injective,Vision,Sora,Everscale,Wanchain,Theta,Conflux,Bittorrent,
# Crescent,DFK,Terra Classic,Heiko,Stacks,Kujira,Ultron,Ultra,Harmony,TON,Flow,
# Dogechain,GodwokenV1,Velas,Secret,Zilliqa,Juno,smartBCH,Vite,Step,Carbon,Songbird,
# Boba,Proton,Interlay,Kardia,Ergo,SXnetwork,Milkomeda C1,Meter,Umee,XDC,ThunderCore,
# CSC,Nuls,Comdex,Kadena,Libre,Hydra,OntologyEVM,Fuse,Bitgert,LBRY,VeChain,Syscoin,
# Elastos,Filecoin,Kintsugi,Godwoken,Energi,Obyte,Arbitrum Nova,Starknet,Callisto,
# FunctionX,Nahmii,Zeniq,Tombchain,Wax,CosmosHub,Genshiro,Flare,Evmos,Bitindi,
# EthereumPoW,Starcoin,Litecoin,EnergyWeb,Nova Network,Map,TomoChain,Ubiq,Shiden,
# EthereumClassic,Boba_Bnb,ICP,Empire,Hoo,Cube,MultiVAC,Findora,Doge,Echelon,
# Milkomeda A1,Lamden,ZYX,Stafi,REI,Lachain,Sifchain,Dexit,HPB,Polkadot,Boba_Avax,
# REIchain,CLV,MUUCHAIN,GoChain,Polis,Stargaze,Kusama,Crab,Palm,Kekchain,Omax,zkSync, Coti
@click.command()
@click.option("--slug", default=None, type=str, help="chain name, eg: Ethterum")
@click.option(
    "--data-range-mode",
    type=click.Choice(["LATEST", "HISTORICAL"], case_sensitive=False),
    required=True,
    help="data range mode",
)
@click.option("--output-file", required=True, help="output file")
@click.option("--pg-url", default=None, help="Postgres database url")
def export_defillama_chain_tvl(slug, data_range_mode, output_file, pg_url):
    job = ExportDefillamaChainTvl(
        slug,
        data_range_mode,
        defillama_chain_tvl_item_exporter(output_file, pg_url),
    )
    job.run()
