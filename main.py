from plot import plotPreflopCalls
import parse

all_calls = parse.parseFolderForPreflopCalls("data")
plotPreflopCalls(all_calls, "Andrew", "preflop_calls_max_Andrew.png", aggregator="max")

# all_shoves = parseLogForShoves("data/02_28_2023.csv")
# print(all_shoves)