import csv
import os
from aliases import people, aliasToPerson

'''
FIGURE OUT HOW TO HANDLE BIG BLINDS
'''

# Returns stacks per person for the given log CSV file
# ex: {
#   "Andrew": [500, 490, 300]
#   "Dorothy": [500, 510, 700]
# }
def ParseLogForStacks(filename: str):
    all_stacks = {}
    buy_ins = {}
    for player in people:
        all_stacks[player] = []
        buy_ins[player] = 0

    with open(filename, newline='') as f:
        reader = csv.reader(f)
        # Get messages in log from first to last hand
        messages = []
        for row in reader:
            messages.append(row[0])
        messages.reverse()

        # Iterate through messages from first to last hand
        count = 0
        prev_round_in = {}
        for player in people:
            prev_round_in[player] = False
        last_round = 0
        for msg in messages:
            # In a stack message:
            if isStack(msg):
                # Initialize everyones stack to 0 (track people who need to buy in again)
                stackamounts = {}
                for player in people:
                    stackamounts[player] = 0

                # Get (player, stack amount) tuples
                rawMsgs = msg.split("|")
                for playerStackRawMsg in rawMsgs:
                    player, amount = getPlayerStackTuple(playerStackRawMsg)
                    stackamounts[player] = amount

                for player in people:
                    if not prev_round_in[player] and stackamounts[player] > 0:
                        buy_ins[player] += 1

                for player in people:
                    if stackamounts[player] == 0:
                        prev_round_in[player] = False
                    else:
                        prev_round_in[player] = True

                for player in people:
                    all_stacks[player].append(stackamounts[player] - 500 * buy_ins[player])
            # In an ending hand message:
            if isHandEnding(msg):
                last_round = extractHandNumberFromHandEnding(msg)

        def getPlayerAmountsTuple(msg):
            if isCall(msg) or isRaise(msg) or isBet(msg) or "posts" in msg:
                amount = extractAmount(msg)
                player = extractPlayer(msg)
                return player, int(float(amount) * 100)
            else:
                return "Andrew", 0

        # Manually calculate stacks for last hand
        for i in range(len(messages)):
            msg = messages[i]
            if isNewHand(msg):
                if extractHandNumberFromHandStarting(msg) == last_round:
                    deltas = {}
                    action = True
                    for player in people:
                        deltas[player] = 0
                    while i < len(messages) and action:
                        msg = messages[i]
                        if isFlop(msg):
                            print("FLOP")
                            break
                        if "Uncalled bet" in msg:
                            player = aliasToPerson(msg.split(" ")[-3][1:])
                            amount = int(float(msg.split(" ")[3]) * 100)
                            action = False
                            deltas[player] += amount
                        player, amount = getPlayerAmountsTuple(msg)
                        deltas[player] -= amount
                        i += 1
                    print(deltas)
                    while i < len(messages) and action:
                        msg = messages[i]
                        if isTurn(msg):
                            print("TURN")
                            break
                        if "Uncalled bet" in msg:
                            player = aliasToPerson(msg.split(" ")[-3][1:])
                            amount = int(float(msg.split(" ")[3]) * 100)
                            action = False
                            deltas[player] += amount
                        player, amount = getPlayerAmountsTuple(msg)
                        deltas[player] -= amount
                        i += 1
                    print(deltas)
                    while i < len(messages) and action:
                        msg = messages[i]
                        if isRiver(msg):
                            print("RIVER")
                            break
                        if "Uncalled bet" in msg:
                            player = aliasToPerson(msg.split(" ")[-3][1:])
                            amount = int(float(msg.split(" ")[3]) * 100)
                            action = False
                            deltas[player] += amount
                        player, amount = getPlayerAmountsTuple(msg)
                        deltas[player] -= amount
                        i += 1
                    print(deltas)
                    while i < len(messages):
                        msg = messages[i]
                        if "collected" in msg:
                            player = extractPlayer(msg)
                            amount = int(float(msg.split(" ")[4]) * 100)
                            deltas[player] += amount
                        i += 1
                    print(deltas)


    return all_stacks

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
#   "Andrew": [0.04, "AhKh", 0.1, "AhAs"],
#   "Dorothy": [1.00, "2s7h"]
# }
def parseFolderForPreflopCalls(folder: str, perspective: "Andrew"):
    all_calls = {}
    for file in os.listdir(folder):
        all_calls = parseLogForPreflopCalls(folder + "/" + file, all_calls, perspective=perspective)
    return all_calls

# Returns a list of preflop calls per person for the given log CSV file
# ex: {
#   "Andrew": [0.04, "AhKh", 0.1, "AhAs"],
#   "Dorothy": [1.00, "2s7h"]
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

# True if the msg is a "Player stacks: #2 "..."" message
def isStack(msg):
    if "Player stacks: #" in msg:
        return True

# True if the msg is a "Player calls 5.56 and go all in" message
def isShove(msg):
    if "go all in" in msg:
        return True

# True if the msg is a "Player shows a 2♣, 5♣" message
def isShow(msg):
    if "shows a" in msg:
        return True

# True if the msg is a "Your hand is 5♣, A♥" message
def isMyHand(msg):
    if "Your hand is" in msg:
        return True

# True if the msg is a "Flop:" message
def isFlop(msg):
    if "Flop:" in msg:
        return True

# True if the msg is a "Turn:" message
def isTurn(msg):
    if "Turn:" in msg:
        return True

# True if the msg is a "River:" message
def isRiver(msg):
    if "River:" in msg:
        return True

# True if the msg is a "player calls 0.04" message
def isCall(msg):
    if " calls " in msg:
        return True

# True if the msg is a "player raises to 0.04" message
def isRaise(msg):
    if " raises " in msg:
        return True

# True if the msg is a "player bets 0.04" message
def isBet(msg):
    if " bets " in msg and "Uncalled" not in msg:
        return True

# True if the msg is a "-- ending hand #118--" message
def isHandEnding(msg):
    if "ending hand" in msg:
        return True

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

# ParseLogForPreflopCalls('data/02_28_2023.csv')
# ParseLogForStacks("data_All/03_15_2023.csv")
