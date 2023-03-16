import plot
import parse

#all_calls = parse.parseFolderForPreflopCalls("data_All", perspective="Andrew")
#plotPreflopCalls(all_calls, "Andrew", "preflop_calls_avg_Andrew.png", aggregator="avg", save=True)

#all_shoves = parse.parseLogForShoves("data_All/03_15_2023.csv")
#print(all_shoves)

all_stacks = parse.ParseLogForStacks("data_All/03_15_2023.csv")
plot.plotStacks(all_stacks)
