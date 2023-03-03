from plot import plotPreflopCalls
from parse import parseLogForPreflopCalls

all_calls = parseLogForPreflopCalls("data/02_28_2023.csv")
plotPreflopCalls(all_calls, "Andrew", "preflop_calls_Andrew.png")