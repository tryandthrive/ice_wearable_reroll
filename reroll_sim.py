import random

# re-roll for lvl5 wearables only
# I assume that each wearable is played solo
# I assume that average leaderboard multiplier is 1x
# (I am overshooting a lot here, my avg is 0.8x (+839 chips daily). I think 1x covers the cheaters too)

# re-roll would give you random bonus between 35-45% (yes you can downgrade)



# Assumed variables:
avg_leaderboard_multiplier = 1

# this means that 95% wearables that have 35% bonus would try to reroll and so on
reroll_probabilities = {35: 0.95,
                        36: 0.9,
                        37: 0.7,
                        38: 0.4,
                        39: 0.2,
                        40: 0.1,
                        41: 0.05,
                        42: 0.01,
                        43: 0.005,
                        44: 0.001}

circulating_supply = 10000  # real circulating supply is 2007 for lvl5 items 35-44% bonus, I will make it 10000 for simplification
supply_of_each_rank = round(circulating_supply / 10)  # assuming it is evenly distributed (it would be in a long run)
reroll_costs = (10000, 20000, 30000, 40000, 50000)  # in ICE for each subsequent re-roll

# all level 5 wearables
# all_wearables = (supply_of_each_rank * [bonus] for bonus in reroll_probabilities.keys())
# all_wearables = (bonus for lst in all_wearables for bonus in lst)

# wearables that would be re-rolled (3316 wearables with current variables)
wearables_reroll = [round(supply_of_each_rank * probability) * [bonus] for bonus, probability in reroll_probabilities.items()]
wearables_reroll = [bonus for lst in wearables_reroll for bonus in lst]



def calc_daily_emission(bonus):
    ice_per_day = 330
    bonus_multiplier = 1 + (bonus / 100)
    return round(ice_per_day * bonus_multiplier * avg_leaderboard_multiplier)


def calc_total_daily_emission(wearables):
    """
    I set the wearable circulating supply to 10000 in the beginning (approx. 5x of real supply) to simplify calculations,
    so I am dividing by 5 here to get back to current real emission.
    """
    return sum([calc_daily_emission(bonus) for bonus in wearables]) / 5


def upgrade(wearables):
    for i, bonus in enumerate(wearables):
        wearables[i] = random.randint(35, 45)


def simulate():
    # print(f'{len(wearables_reroll)=}')
    print(f'Average leaderboard multiplier = {avg_leaderboard_multiplier}')

    initial_daily_emission = calc_total_daily_emission(wearables_reroll)
    print(f'Pre-reroll daily emission: {round(initial_daily_emission)}')

    upgrade(wearables_reroll)

    round1_daily_emission = calc_total_daily_emission(wearables_reroll)
    round1_daily_emission_diff = round1_daily_emission - initial_daily_emission
    round1_ice_burn = len(wearables_reroll) * reroll_costs[0] / 5  # dividing by 5 here too, yeah I know messy..

    print(f'Round 1 daily emission: {round(round1_daily_emission)}')
    print(f'Round 1 daily emission difference: {round(round1_daily_emission_diff)}')
    # print(f'Round 1 daily emission increase: {round(round1_daily_emission_diff / initial_daily_emission * 100, 2)}%')
    print(f'Round 1 re-roll cost: {reroll_costs[0]}')
    print(f'Round 1 ICE burn: {round(round1_ice_burn)}')
    print(f'Net emission will increase after {round(round1_ice_burn / round1_daily_emission_diff)} days '
          f'({round(round1_ice_burn / round1_daily_emission_diff / 365, 2)} years)')


simulate()
