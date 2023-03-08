from plot import plotPreflopCalls
import parse

all_calls = parse.parseFolderForPreflopCalls("data")
plotPreflopCalls(all_calls, "Andrew", "preflop_calls_avg_Andrew.png", aggregator="avg")

# all_shoves = parse.parseLogForShoves("data/03_08_2023.csv")
# print(all_shoves)