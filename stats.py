from aliases import people
import math

def CalculatePercentageReturns(all_stacks):
    all_returns = {}
    for player in people:
        all_returns[player] = []

    for i in range(1, len(all_stacks["Andrew"])):
        for player in people:
            x = all_stacks[player]

            curr, prev = x[i], x[i-1]
            if prev == 0:
                all_returns[player].append(0)
            else:
                all_returns[player].append((curr - prev) / float(prev))

    return all_returns

def CalculateProfits(all_stacks, all_buy_ins):
    all_profits = {}
    for player in people:
        all_profits[player] = []

    for i in range(0, len(all_stacks["Andrew"])):
        for player in people:
            all_profits[player].append(all_stacks[player][i] - all_buy_ins[player][i] * 500)

    return all_profits

def CalculateVariations(all_returns):
    all_stddev = {}
    all_downside = {}
    all_upside = {}
    for player in people:
        all_stddev[player] = 0
        all_downside[player] = 0
        all_upside[player] = 0

    for player in people:
        x = all_returns[player]
        x_up = []
        x_down = []
        for ret in x:
            if ret > 0:
                x_up.append(ret)
            if ret < 0:
                x_down.append(ret)

        all_stddev[player] = getStdDev(x)
        all_upside[player] = getStdDev(x_up)
        all_downside[player] = getStdDev(x_down)

    return all_stddev, all_upside, all_downside

def getStdDev(x):
    stddev = 0
    n = float(len(x))
    if n == 0:
        return 0
    mean = sum(x) / n
    for ret in x:
        stddev += (ret - mean) ** 2
    return round(math.sqrt(stddev / n), 6)