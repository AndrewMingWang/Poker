import csv
import os
from aliases import people, aliasToPerson

'''
FIGURE OUT HOW TO HANDLE BIG BLINDS
'''

# Returns stacks and buy-ins per person for the given log CSV file
# ex:
# stacks: {
#   "Andrew": [0, 500, 490, 300]
#   "Dorothy": [0, 500, 510, 700]
# }
# buy-ins: {
#   "Andrew": [0, 1, 1, 1]
#   "Dorothy": [0, 1, 1, 1]
# }
def ParseLogForStacksAndBuyIns(filename: str):
    all_stacks = {}
    all_buy_ins = {}
    buy_outs = {}
    for player in people:
        all_stacks[player] = [0]
        all_buy_ins[player] = [0]

    # Iterate through messages from first to last hand
    messages = getMessages(filename)
    last_round = 0
    for msg in messages:
        # In a stack message:
        if isStack(msg):
            curr_stacks = {}
            for player in people:
                curr_stacks[player] = 0

            # Get (player, stack amount) tuples
            stack_msgs = msg.split("|")
            for stack_msg in stack_msgs:
                player, amount = getPlayerStackTuple(stack_msg)
                curr_stacks[player] = amount
            for player in people:
                if player in buy_outs and curr_stacks[player] == 0:
                    curr_stacks[player] = buy_outs[player]

            # Count blinds
            for player in people:
                if all_stacks[player][-1] == 0 and curr_stacks[player] > 0:
                    all_buy_ins[player].append(all_buy_ins[player][-1] + 1)
                else:
                    all_buy_ins[player].append(all_buy_ins[player][-1])

            # Count stacks
            for player in people:
                all_stacks[player].append(curr_stacks[player])
        # In an ending hand message:
        if isHandEnding(msg):
            last_round = extractHandNumberFromHandEnding(msg)
        if isBuyout(msg) or "stand up" in msg:
            player = aliasToPerson(msg.split('\"')[1].split(" ")[0])
            amount = int(float(msg.split(" ")[-1][:-1]) * 100)
            if amount > 0:
                buy_outs[player] = amount

    def getPlayerAmountsTuple(msg):
        if isCall(msg) or isRaise(msg) or isBet(msg) or "posts" in msg:
            amount = int(float(extractAmount(msg)) * 100)
            player = extractPlayer(msg)
            return player, amount
        else:
            return "Andrew", 0

    def getUncalledBetTuple(msg):
        player = aliasToPerson(msg.split(" ")[-3][1:])
        amount = int(float(msg.split(" ")[3]) * 100)
        return player, amount

    # Manually calculate stacks for last hand
    for i in range(len(messages)):
        msg = messages[i]
        if isNewHand(msg):
            if extractHandNumberFromHandStarting(msg) == last_round:
                deltas = {}
                for player in people:
                    deltas[player] = 0
                action_remaining = True
                while i < len(messages) and action_remaining:
                    msg = messages[i]
                    if isFlop(msg):
                        break
                    elif "Uncalled bet" in msg:
                        action_remaining = False
                        player, amount = getUncalledBetTuple(msg)
                        deltas[player] += amount
                    else:
                        player, amount = getPlayerAmountsTuple(msg)
                        deltas[player] -= amount
                    i += 1
                while i < len(messages) and action_remaining:
                    msg = messages[i]
                    if isTurn(msg):
                        break
                    elif "Uncalled bet" in msg:
                        action_remaining = False
                        player, amount = getUncalledBetTuple(msg)
                        deltas[player] += amount
                    else:
                        player, amount = getPlayerAmountsTuple(msg)
                        deltas[player] -= amount
                    i += 1
                while i < len(messages) and action_remaining:
                    msg = messages[i]
                    if isRiver(msg):
                        break
                    elif "Uncalled bet" in msg:
                        action_remaining = False
                        player, amount = getUncalledBetTuple(msg)
                        deltas[player] += amount
                    else:
                        player, amount = getPlayerAmountsTuple(msg)
                        deltas[player] -= amount
                    i += 1
                while i < len(messages):
                    msg = messages[i]
                    if "collected" in msg:
                        player = extractPlayer(msg)
                        amount = int(float(msg.split(" ")[4]) * 100)
                        deltas[player] += amount
                    i += 1
                for player in people:
                    all_buy_ins[player].append(all_buy_ins[player][-1])
                    all_stacks[player].append(all_stacks[player][-1] + deltas[player])

    # for player in people:
    #    print(player, len(all_buy_ins[player]), all_buy_ins[player])
    #    print(player, len(all_stacks[player]), all_stacks[player])
    return all_stacks, all_buy_ins

# Returns number of calls per person for the given log CSV file
# ex: {
#   "Andrew": 10,
#   "Dorothy": 2
# }
def parseLogForShoves(filename: str):
    all_shoves = {}
    for person in people:
        all_shoves[person] = 0
    with open(filename, newline='') as f:
        reader = csv.reader(f)
        # Get messages in log from first to last hand
        messages = []
        for row in reader:
            messages.append(row[0])
        messages.reverse()

        # Iterate through messages from first to last hand
        for msg in messages:
            # In a shove msg
            if isShove(msg):
                player = extractPlayer(msg)
                all_shoves[player] += 1

    return {k: v for k, v in sorted(all_shoves.items(), key=lambda item: item[1])}

# Returns a list of preflop calls per person for the given folder of log CSV files
# ex: {
#   "Andrew": [(0.04, "AhKh"), (0.1, "AhAs")],
#   "Dorothy": [(1.00, "2s7h")]
# }
def parseFolderForPreflopCalls(folder: str, perspective: "Andrew"):
    all_calls = {}
    for file in os.listdir(folder):
        all_calls = parseLogForPreflopCalls(folder + "/" + file, all_calls, perspective=perspective)
    return all_calls

# Returns a list of preflop calls per person for the given log CSV file
# ex: {
#   "Andrew": [(0.04, "AhKh"), (0.1, "AhAs")],
#   "Dorothy": [(1.00, "2s7h")]
# }
def parseLogForPreflopCalls(filename: str, all_calls=None, perspective="Andrew"):
    if all_calls is None:
        all_calls = {}
    for person in people:
        if person not in all_calls:
            all_calls[person] = []
    with open(filename, newline='') as f:
        reader = csv.reader(f)
        # Get messages in log from first to last hand
        messages = []
        for row in reader:
            messages.append(row[0])
        messages.reverse()

        # Initialize tracking variables
        calls = newCallsDict()
        hands = newHandsDict()
        isPreflop = False

        # Iterate through messages from first to last hand
        for msg in messages:
            # In a new hand msg
            if isNewHand(msg):
                # Record results for the previous hand
                for person in people:
                    if hands[person] != '' and calls[person] > 0.0:
                        all_calls[person].append((calls[person], hands[person]))
                # Reset tracking variables
                calls = newCallsDict()
                hands = newHandsDict()
                isPreflop = True
            # In a preflop call or raise msg
            elif isPreflop and (isCall(msg) or isRaise(msg)):
                player = extractPlayer(msg)
                amount = extractAmount(msg)
                calls[player] = max(calls[player], float(amount))
            # In a flop msg
            elif isFlop(msg):
                isPreflop = False
            # In a showing my hand msg
            elif isMyHand(msg):
                hand = extractMyHand(msg)
                hands[perspective] = hand
            # In a showing player hand msg
            elif isShow(msg):
                hand = extractShowHand(msg)
                player = extractPlayer(msg)
                hands[player] = hand

        # Record results for the last hand
        for person in people:
            if hands[person] != '' and calls[person] > 0.0:
                all_calls[person].append((calls[person], hands[person]))

    return all_calls

# True if the msg is a "The player ""Jade @ xhsZ8jgTjv"" quits the game with a stack of 6.82." message
def isBuyout(msg): return "quits the game with a stack of" in msg

# True if the msg is a "Player stacks: #2 "..."" message
def isStack(msg): return "Player stacks: #" in msg

# True if the msg is a "Player calls 5.56 and go all in" message
def isShove(msg): return "go all in" in msg

# True if the msg is a "Player shows a 2♣, 5♣" message
def isShow(msg): return "shows a" in msg

# True if the msg is a "Your hand is 5♣, A♥" message
def isMyHand(msg): return "Your hand is" in msg

# True if the msg is a "Flop:" message
def isFlop(msg): return "Flop:" in msg

# True if the msg is a "Turn:" message
def isTurn(msg): return "Turn:" in msg

# True if the msg is a "River:" message
def isRiver(msg): return "River:" in msg

# True if the msg is a "player calls 0.04" message
def isCall(msg): return " calls " in msg

# True if the msg is a "player raises to 0.04" message
def isRaise(msg): return " raises " in msg

# True if the msg is a "player bets 0.04" message
def isBet(msg): return " bets " in msg

# True if the msg is a "-- ending hand #118--" message
def isHandEnding(msg): return "ending hand" in msg

# True if the msg is a "Uncalled bet of 4.00 returned to" message
def isUncalledBet(msg): return "Uncalled bet" in msg

# Extracts hand number from "-- ending hand #118--" message
def extractHandNumberFromHandEnding(msg):
    words = msg.split(" ")
    return int(words[-2][1:])

# Extracts hand number from "starting hand #1" message
def extractHandNumberFromHandStarting(msg):
    words = msg.split(" ")
    return int(words[3][1:])

# Gets the hands in a "Player shows a 2♣, 5♣" message
def extractShowHand(msg):
    m = msg.split(',')
    first = m[0][-4:]
    second = m[1][1:-1]

    first = getCanonicalCard(first)
    second = getCanonicalCard(second)
    if canonicalNumToInt(first[0]) < canonicalNumToInt(second[0]):
        return second + first
    return first + second

# Gets the hand in a "Your hand is 5♣, A♥" message
def extractMyHand(msg):
    m = msg.split(',')
    first = m[0][13:]
    second = m[1][1:]

    first = getCanonicalCard(first)
    second = getCanonicalCard(second)
    if canonicalNumToInt(first[0]) < canonicalNumToInt(second[0]):
        return second + first
    return first + second

# Gets the amount in a "player calls/raises/postsblind 0.04" message
def extractAmount(msg):
    if "go all in" in msg:
        return msg.split()[-5]
    return msg.split()[-1]

# Gets the player in a "player calls/raises/postsblind 0.04" message
def extractPlayer(msg):
    for i in range(len(msg)):
        if msg[i] == "@":
            return aliasToPerson(msg[1:i-1])

# True if the msg is a "starting hand #1" message
def isNewHand(msg):
    if "starting hand" in msg:
        return True

# Gets the hand number from a "starting hand #1" message
def extractHandNumber(msg):
    return msg[18:].split()[0]

# Returns a dictionary {"Andrew": 0.0, ...} for all names in "people"
def newCallsDict():
    res = {}
    for person in people:
        res[person] = 0.0
    return res

# Returns a dictionary {"Andrew": "", ...} for all names in "people"
def newHandsDict():
    res = {}
    for person in people:
        res[person] = ""
    return res

# Given a string "7♣" returns it in canonical form
# ex: "7♣"  -> "7c"
# ex: "10♥" -> "Th"
def getCanonicalCard(s):
    num = s[:-3]
    num = "T" if num == "10" or num == "0" else num
    suit = getCanonicalSuit(s)
    assert len(num+suit) == 2
    return num+suit

# Given a string "7♣" returns the suit in canonical form
# ex: "7♣"  -> "c"
# ex: "10♥" -> "h"
def getCanonicalSuit(s):
    if "â™¥" in s:
        return "h"
    elif "â™£" in s:
        return "c"
    elif "â™¦" in s:
        return "d"
    elif "â™ " in s:
        return "s"
    else:
        print("ERROR! Unrecognized suit emoji:", s)
        return ""

# Converts canonical card number to its order equivalent integer
def canonicalNumToInt(n):
    if n == "A":
        return 14
    elif n == "K":
        return 13
    elif n == "Q":
        return 12
    elif n == "J":
        return 11
    elif n == "T":
        return 10
    else:
        return int(n)

# Parse "#10 "Andrew @ yhDVFE17BV" (19.61)" message into (Andrew, 19.61) player, stack amount tuples
def getPlayerStackTuple(msg):
    start, stop = 0, 0
    for i in range(len(msg)):
        if msg[i] == "\"":
            start = i + 1
            break
    for i in range(len(msg)):
        if msg[i] == "@":
            stop = i - 1
            break
    player = aliasToPerson(msg[start:stop])
    for i in range(len(msg)):
        if msg[i] == "(":
            start = i + 1
            break
    for i in range(len(msg)):
        if msg[i] == ")":
            stop = i
            break
    amount = msg[start:stop]
    return player, int(float(amount) * 100)

def getMessages(filename: str):
    with open(filename, newline='') as f:
        reader = csv.reader(f)
        # Get messages in log from first to last hand
        messages = []
        for row in reader:
            messages.append(row[0])
        messages.reverse()
        return messages

# ParseLogForPreflopCalls('data/02_28_2023.csv')
# ParseLogForStacks("data_All/03_15_2023.csv")
