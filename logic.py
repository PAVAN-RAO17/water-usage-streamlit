REWARD_RATE = 0.01
MAX_DISCOUNT_PERCENT = 30

def calculate_rewards(actual, expected):
    reward_points = 0

    if actual < expected:
        reward_points = (expected - actual) * REWARD_RATE

        max_allowed = expected * MAX_DISCOUNT_PERCENT / 100
        reward_points = min(reward_points, max_allowed)

    return round(reward_points, 2)