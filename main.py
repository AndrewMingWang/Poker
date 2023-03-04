from plot import plotPreflopCalls
from parse import parseLogForPreflopCalls, parseLogForShoves

# all_calls = parseLogForPreflopCalls("data/02_28_2023.csv")
# plotPreflopCalls(all_calls, "Andrew", "preflop_calls_Andrew.png")
all_shoves = parseLogForShoves("data/02_28_2023.csv")

print(all_shoves)