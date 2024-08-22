import os

import pandas as pd

from blockchainetl.jobs.base_job import BaseJob
from overviewetl.domain.chain_stats import ChainStats
from overviewetl.enumeration.chains import Chains


class ExtractChainStats(BaseJob):
    def __init__(
        self,
        item_exporter,
        cmc_input_file,
        llama_input_file,
        stakingrewards_input_file,
    ):
        if os.path.isdir(cmc_input_file):
            cmc_input_file = [
                os.path.join(cmc_input_file, file)
                for file in os.listdir(cmc_input_file)
                if file.endswith(".csv")
                and os.path.getsize(os.path.join(cmc_input_file, file)) > 0
            ]
        else:
            cmc_input_file = [cmc_input_file]

        if os.path.isdir(llama_input_file):
            llama_input_file = [
                os.path.join(llama_input_file, file)
                for file in os.listdir(llama_input_file)
                if file.endswith(".csv")
                and os.path.getsize(os.path.join(llama_input_file, file)) > 0
            ]
        else:
            llama_input_file = [llama_input_file]

        if os.path.isdir(stakingrewards_input_file):
            stakingrewards_input_file = [
                os.path.join(stakingrewards_input_file, file)
                for file in os.listdir(stakingrewards_input_file)
                if file.endswith(".csv")
                and os.path.getsize(os.path.join(stakingrewards_input_file, file)) > 0
            ]
        else:
            stakingrewards_input_file = [stakingrewards_input_file]

        self.cmc_input_file = cmc_input_file
        self.llama_input_file = llama_input_file
        self.stakingrewards_input_file = stakingrewards_input_file
        self.item_exporter = item_exporter

    def _start(self):
        self.item_exporter.open()

    def _export(self):
        cmc_dfs = []
        llama_dfs = []
        stakingrewards_dfs = []

        for file in self.cmc_input_file or []:
            df = pd.read_csv(file)
            df = df[df["native"] == True]

            if df.empty:
                continue

            df["chain"] = df["chain"].apply(
                lambda x: f"{Chains[x].value}_{x}"
                if Chains[x] == Chains.UNKNOWN_CHAIN
                else Chains[x].value
            )

            cmc_dfs.append(df)

        if len(cmc_dfs) > 0:
            cmc_df = pd.concat(cmc_dfs)
        else:
            cmc_df = pd.DataFrame(
                columns=[
                    "timestamp",
                    "datetime",
                    "cmc_id",
                    "name",
                    "symbol",
                    "native",
                    "rank",
                    "total_supply",
                    "max_supply",
                    "circulating_supply",
                    "price",
                    "volume_24h",
                    "market_cap",
                    "fully_diluted_market_cap",
                    "market_cap_dominance",
                    "chain",
                ]
            )

        for file in self.llama_input_file or []:
            df = pd.read_csv(file)

            df["chain"] = df["chain"].apply(
                lambda x: f"{Chains[x].value}_{x}"
                if Chains[x] == Chains.UNKNOWN_CHAIN
                else Chains[x].value
            )

            llama_dfs.append(df)

        if len(llama_dfs) > 0:
            llama_df = pd.concat(llama_dfs)
        else:
            llama_df = pd.DataFrame(
                columns=[
                    "timestamp",
                    "datetime",
                    "cmc_id",
                    "gecko_id",
                    "llama_id",
                    "symbol",
                    "chain",
                    "tvl",
                ]
            )

        for file in self.stakingrewards_input_file or []:
            df = pd.read_csv(file)

            if df.empty:
                continue

            df = df[df["chain"].notnull()]

            if df.empty:
                continue

            df = df.rename(
                columns={
                    "total_users": "total_validators",
                    "value_locked": "total_validator_staked",
                }
            )

            # TODO: maybe no need to apply chain.
            df["chain"] = df["chain"].apply(
                lambda x: f"{Chains[x].value}_{x}"
                if Chains[x] == Chains.UNKNOWN_CHAIN
                else Chains[x].value
            )
            stakingrewards_dfs.append(df)

        if len(stakingrewards_dfs) > 0:
            stakingrewards_df = pd.concat(stakingrewards_dfs)
        else:
            stakingrewards_df = pd.DataFrame(
                columns=[
                    "timestamp",
                    "datetime",
                    "chain",
                    "slug",
                    "price",
                    "total_validators",
                    "total_validator_staked",
                    "annual_earnings",
                ]
            )

        # reference: https://pandas.pydata.org/docs/user_guide/merging.html#merging-join
        final_df = pd.merge(
            cmc_df, llama_df, how="outer", on=["timestamp", "datetime", "cmc_id"]
        )
        final_df["chain"] = final_df["chain_y"].fillna(final_df["chain_x"])
        final_df["symbol"] = final_df["symbol_y"].fillna(final_df["symbol_x"])

        final_df = final_df.drop(["chain_x", "chain_y", "symbol_x", "symbol_y"], axis=1)

        final_df = pd.merge(
            final_df,
            stakingrewards_df,
            how="outer",
            on=["timestamp", "datetime", "chain"],
        )

        final_df["price"] = final_df["price_y"].fillna(final_df["price_x"])
        final_df = final_df.drop(["price_x", "price_y"], axis=1)

        final_df = final_df.reset_index()  # make sure indexes pair with number of rows
        # final_df.to_csv("final_df1.csv")

        final_df = final_df.where(pd.notnull(final_df), None)

        # get row 100 of final_df         
        # final_df.to_csv("final_df2.csv")

        # final_df.drop_duplicates(subset=["timestamp", "datetime", "chain"], inplace=True)

        # final_df.to_csv("final_df.csv")

        cs = []

        for _, row in final_df.iterrows():
            cs.append(
                # TODO: optimise this too many pd.notnull
                ChainStats(
                    timestamp=row["timestamp"],
                    datetime=row["datetime"],
                    chain=row["chain"] if pd.notnull(row["chain"]) else None,
                    cmc_id=row["cmc_id"] if pd.notnull(row["cmc_id"]) else None,
                    gecko_id=row["gecko_id"] if pd.notnull(row["gecko_id"]) else None,
                    llama_id=row["llama_id"] if pd.notnull(row["llama_id"]) else None,
                    nt_name=row["name"] if pd.notnull(row["name"]) else None,
                    nt_symbol=row["symbol"] if pd.notnull(row["symbol"]) else None,
                    nt_rank=row["rank"] if pd.notnull(row["rank"]) else None,
                    nt_total_supply=row["total_supply"] if pd.notnull(row["total_supply"]) else None,
                    nt_max_supply=row["max_supply"] if pd.notnull(row["max_supply"]) else None,
                    nt_circulating_supply=row["circulating_supply"] if pd.notnull(row["circulating_supply"]) else None,
                    nt_num_market_pairs=row["num_market_pairs"]     if pd.notnull(row["num_market_pairs"]) else None,
                    nt_price=row["price"] if pd.notnull(row["price"]) else None,
                    nt_volume_24h=row["volume_24h"] if pd.notnull(row["volume_24h"]) else None,
                    nt_market_cap=row["market_cap"] if pd.notnull(row["market_cap"]) else None,
                    nt_fully_diluted_market_cap=row["fully_diluted_market_cap"] if pd.notnull(row["fully_diluted_market_cap"]) else None,
                    nt_market_cap_dominance=row["market_cap_dominance"] if pd.notnull(row["market_cap_dominance"]) else None,
                    tvl=row["tvl"] if pd.notnull(row["tvl"]) else None,
                    total_validators=row["total_validators"] if pd.notnull(row["total_validators"]) else None,
                    total_validator_staked=row["total_validator_staked"] if pd.notnull(row["total_validator_staked"]) else None,
                    annual_earnings=row["annual_earnings"] if pd.notnull(row["annual_earnings"]) else None,
                )
            )

        items = [{**e.asdict(), "type": "chain_stats"} for e in cs]

        self.item_exporter.export_items(items)

    def _end(self):
        self.item_exporter.close()
