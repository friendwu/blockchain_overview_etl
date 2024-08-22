CREATE SCHEMA IF NOT EXISTS blockchain_overview;

CREATE TABLE IF NOT EXISTS "blockchain_overview"."cmc_token_markets" (
    "id" BIGSERIAL NOT NULL,
    "cmc_id" bigint NOT NULL,
    "timestamp" bigint NOT NULL,
    "datetime" timestamp,
    "symbol" text,
    "name" text,
    "slug" text,
    "native" boolean,
    "chain" text,
    "rank" bigint,
    "total_supply" numeric,
    "max_supply" numeric,
    "circulating_supply" numeric,
    "num_market_pairs" numeric,
    "price" numeric,
    "volume_24h" numeric,
    "market_cap" numeric,
    "fully_diluted_market_cap" numeric,
    "market_cap_dominance" numeric,
    "last_updated" timestamp,
    PRIMARY KEY ("cmc_id", "timestamp")
);

CREATE TABLE IF NOT EXISTS "blockchain_overview"."defillama_chain_tvls" (
    "id" BIGSERIAL NOT NULL,
    "timestamp" bigint NOT NULL,
    "chain" text NOT NULL,
    "slug" text NOT NULL,
    "datetime" timestamp NOT NULL,
    "cmc_id" bigint,
    "gecko_id" text,
    "llama_id" bigint,
    "tvl" numeric,
    PRIMARY KEY ("chain", "timestamp")
);

CREATE TABLE IF NOT EXISTS "blockchain_overview"."stakingrewards_stakings" (
    "id" BIGSERIAL NOT NULL,
    "timestamp" bigint not null,
    "chain" text NOT NULL,
    "slug" text,
    "datetime" timestamp NOT NULL,
    "total_users" bigint,
    "value_locked" numeric,
    "annual_earnings" numeric,
    PRIMARY KEY ("slug", "timestamp")
);

CREATE TABLE "blockchain_overview"."chain_stats" (
    "id" BIGSERIAL NOT NULL,
    "timestamp" bigint NOT NULL,
    "datetime" timestamp,
    "chain" text NOT NULL,
    "cmc_id" bigint,
    "gecko_id" text,
    "llama_id" bigint,
    "nt_name" text,
    "nt_symbol" text,
    "nt_rank" bigint,
    "nt_total_supply" bigint,
    "nt_max_supply" bigint,
    "nt_circulating_supply" bigint,
    "nt_num_market_pairs" bigint,
    "nt_price" numeric,
    "nt_volume_24h" numeric,
    "nt_market_cap" numeric,
    "nt_fully_diluted_market_cap" numeric,
    "nt_market_cap_dominance" numeric,
    "tvl" numeric,
    "total_validators" bigint,
    "total_validator_staked" numeric,
    "annual_earnings" numeric,
    PRIMARY KEY ("timestamp", "chain")
);

-- CREATE TABLE IF NOT EXISTS "blockchain_overview"."chain_stats" (
--     "id" bigint NOT NULL DEFAULT,
--     "chain" text NOT NULL,
--     "cmc_id" bigint,
--     "gecko_id" text,
--     "timestamp" timestamp NOT NULL,
--     "tvl" numeric,
--     "total_validators" bigint,
--     "total_validator_staked" bigint,
--     "annual_earnings" numeric,
--     -- "total_validator_staked_in_usdt" numeric, can be calculated through multiplication.
--     "nt_name" text,
--     "nt_symbol" text,
--     "nt_rank": int4,
--     "nt_total_supply": bigint,
--     "nt_max_supply": bigint,
--     "nt_circulating_supply": bigint,
--     "nt_num_market_pairs": bigint,
--     "nt_price": numeric,
--     "nt_volume_24h": numeric,
--     "nt_market_cap": numeric,
--     "nt_fully_diluted_market_cap" numeric,
--     "nt_market_cap_dominance" numeric PRIMARY KEY ("chain", "timestamp")
-- );
-- CREATE TABLE IF NOT EXISTS blockchain_overview.token_vesting_schedule (
--     "id" bigint NOT NULL DEFAULT,
--     "cmc_id" bigint,
--     "gecko_id" text,
--     "name" text,
--     "symbol" text,
--     "native" int4,
--     "chain" text,
--     "timestamp" timestamp NOT NULL,
--     "group" text NOT NULL,
--     Total,
--     Marketing / Team / etc."token_cnt" bigint NOT NULL,
-- );
-- CREATE TABLE IF NOT EXISTS blockchain_overview.cmc_id_map (
--     id BIGSERIAL,
--     name TEXT,
--     symbol TEXT,
--     slug TEXT,
--     rank INT,
--     displayTV INT,
--     manualSetTV INT,
--     tvCoinSymbol TEXT,
--     is_active INT,
--     first_historical_data date,
--     # "2022-04-22T05:45:00.000Z"
--     last_historical_data date,
--     # "2022-04-22T05:45:00.000Z"
--     platform_id BIGSERIAL,
--     platform_name TEXT,
--     platform_symbol TEXT,
--     platform_slug TEXT,
--     platform_token_address TEXT
-- );
-- CREATE TABLE IF NOT EXISTS blockchain_overview.chains (
--     id bigint default,
--     chain text,
--     cmc_id BIGINT,
--     gecko_id text,
--     llama_id bigint,
--     token_symbol text
-- );
-- CREATE TABLE IF NOT EXISTS blockchain_overview.tokens (
--     id bigint default,
--     cmc_id bigint,
--     gecko_id text,
--     symbol text,
--     slug text,
--     name text,
--     platform_cmc_id bigint,
--     platform_gecko_id text,
--     platform_name TEXT,
--     platform_symbol TEXT,
--     platform_slug TEXT,
--     platform_token_address TEXT,
--     first_historical_data timestamp,
--     # "2022-04-22T05:45:00.000Z"
-- )
