from overviewetl.domain.stakingrewards import StakingRewardsStaking

from . import gen_multi_item_exporter


def stakingrewards_staking_item_exporter(output, pg_url):
    return gen_multi_item_exporter(
        output,
        pg_url,
        "stakingrewards_staking",
        "stakingrewards_stakings",
        StakingRewardsStaking.fields,
    )
