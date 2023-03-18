import plot
import parse
import stats
from aliases import people

# all_calls = parse.parseFolderForPreflopCalls("data_All", perspective="Andrew")
# plotPreflopCalls(all_calls, "Andrew", "preflop_calls_avg_Andrew.png", aggregator="avg", save=True)

# all_shoves = parse.parseLogForShoves("data_All/03_15_2023.csv")
# print(all_shoves)

all_stacks, all_buy_ins = parse.ParseLogForStacksAndBuyIns("data_All/03_15_2023.csv")
all_returns = stats.CalculatePercentageReturns(all_stacks)
all_profits = stats.CalculateProfits(all_stacks, all_buy_ins)
all_stddev, all_upside, all_downside = stats.CalculateVariations(all_returns)
print(" " * 10, "stddev  ", "upside  ", "downside")
for player in people:
    if player != "Matthew":
        print(player + " " * (10 - len(player)), all_stddev[player], all_upside[player], all_downside[player])
plot.plotStacks(all_profits)
plot.plotReturns(all_returns)
