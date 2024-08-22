from aenum import Enum


def format_chain(chain):
    res = Chains[chain].value
    if res == "NaN":
        res = chain.lower().capitalize()

    return res


class Chains(Enum):
    BITCOIN = "Bitcoin"
    ETHEREUM = "Ethereum"
    ARBITRUM = "Arbitrum"
    STARKNET = "Starknet"
    OPTIMISM = "Optimism"
    ZKSYNC = "ZkSync"
    BINANCE_SMART_CHAIN = "BSC"
    AURORA = "Aurora"
    OASIS = "Oasis"
    POLYGON = "Polygon"
    AVALANCHE = "Avalanche"
    OKCHAIN = "OKChain"
    CRONOS = "Cronos"
    FANTOM = "Fantom"
    TRON = "Tron"
    MOONBEAM = "Moonbeam"
    ACALA = "Acala"
    IMMUTABLEX = "Immutablex"
    RONIN = "Ronin"
    CANTO = "Canto"
    POLKADOT = "Polkadot"
    SUI = "Sui"
    SOLANA = "Solana"
    APTOS = "Aptos"
    NERVOS = "Nervos"
    TON = "Ton"
    COSMOS = "Cosmos"
    SEI = "Sei"
    DYDX = "Dydx"

    UNKNOWN_CHAIN = "NaN"

    @classmethod
    def _missing_name_(cls, name):
        _m = {
            # cmc
            "bnb": cls.BINANCE_SMART_CHAIN,
            "bsc": cls.BINANCE_SMART_CHAIN,
            "optimism-ethereum": cls.OPTIMISM,
            "okb": cls.OKCHAIN,
            "oasis-network": cls.OASIS,
            "polkadot-new": cls.POLKADOT,
            "nervos-network": cls.NERVOS,
            # defillama
            "OKExChain": cls.OKCHAIN,
            "binance": cls.BINANCE_SMART_CHAIN,
            # stakingrewards
            "ethereum-2-0": cls.ETHEREUM,
            # "arbitrum": cls.ARBITRUM,
            "binance-smart-chain": cls.BINANCE_SMART_CHAIN,
            "aurora-near": cls.AURORA,
            # "oasis-network": cls.OASIS,
            "matic-network": cls.POLYGON,
            # "avalanche": cls.AVALANCHE,
            "crypto-com-coin": cls.CRONOS,
            # "fantom": cls.FANTOM,
            # "tron": cls.TRON,
            # "moonbeam": cls.MOONBEAM,
            # "acala": cls.ACALA,
            # "canto": cls.CANTO,
            # "polkadot": cls.POLKADOT,
            # "solana": cls.SOLANA,
            # "aptos": cls.APTOS,
            # "cosmos": cls.COSMOS,
            # "dydx": cls.DYDX,
        }

        for member in cls:
            if member.name.lower() == name.lower():
                return member

        return _m.get(name.lower(), cls.UNKNOWN_CHAIN)
