import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patheffects as PathEffects

# Given strings "7c", "8c" returns its indices (x, y) in the poker hands chart
def canonicalCardsToIndex(s1, s2):
    num1, num2, suit1, suit2 = s1[0], s2[0], s1[1], s2[1]
    if suit1 == suit2:
        return numToIndex(num1), numToIndex(num2)
    else:
        return numToIndex(num2), numToIndex(num1)

# Given index (x, y) returns its hand "AKs" in the poker hands chart
def indexToCanonicalCards(r, c):
    if r == c:
        return indexToNum(r) + indexToNum(c)
    elif r < c:
        return indexToNum(r) + indexToNum(c) + 'o'
    else:
        return indexToNum(c) + indexToNum(r) + 's'

# Converts card number to index in the poker hands chart
def numToIndex(n):
    if n == "A":
        return 0
    elif n == "K":
        return 1
    elif n == "Q":
        return 2
    elif n == "J":
        return 3
    elif n == "T":
        return 4
    else:
        return 14 - int(n)

# Converts index in the poker hands chart to card number
def indexToNum(i):
    if i == 0:
        return "A"
    elif i == 1:
        return "K"
    elif i == 2:
        return "Q"
    elif i == 3:
        return "J"
    elif i == 4:
        return "T"
    else:
        return str(14 - i)

def plotPreflopCalls(all_calls, person="Andrew", filename="preflop_calls_Andrew.png", aggregator="max"):
    if aggregator not in ["max", "avg"]:
        print("ERROR! " + aggregator + " is not a valid aggregator (max, avg).")
        return
    person_calls = all_calls[person]

    # Convert calls data into poker hands table format
    z = np.zeros((13, 13))
    if aggregator == "max":
        for call in person_calls:
            call_amount, call_hand = call
            r, c = canonicalCardsToIndex(call_hand[:2], call_hand[2:])
            # Track the largest preflop call made for this hand
            z[r][c] = max(call_amount * 100, z[r][c])
    elif aggregator == "avg":
        zcounts = np.zeros((13, 13))
        for call in person_calls:
            call_amount, call_hand = call
            r, c = canonicalCardsToIndex(call_hand[:2], call_hand[2:])
            # Track the sum of all preflop calls made for this hand
            z[r][c] += call_amount * 100
            zcounts[r][c] += 1
        for r in range(13):
            for c in range(13):
                if zcounts[r][c] != 0:
                    z[r][c] /= zcounts[r][c]

    # Calculate log version of output
    zlog = np.zeros((13, 13))
    for r in range(13):
        for c in range(13):
            if z[r][c] != 0:
                zlog[r][c] = np.log(z[r][c])

    # Setup figure
    fig, ax = plt.subplots(figsize=(12, 12))
    ax.xaxis.set_visible(False)
    ax.yaxis.set_visible(False)

    # Make color plot background
    ax.imshow(zlog, interpolation='none', aspect='auto',cmap=plt.cm.gray)

    # Make labels
    for (j, i), label in np.ndenumerate(z):
        ax.text(i, j, indexToCanonicalCards(i, j),
            ha='center', va='bottom', color='w', name='consolas')\
            .set_path_effects([PathEffects.withStroke(linewidth=2, foreground='black')])
        ax.text(i, j, "\n" + str(int(label)) if label != 0 else "",
            ha='center', va='center', color='w', weight='heavy', size=11, name='consolas')\
            .set_path_effects([PathEffects.withStroke(linewidth=0 if label == 0 else 2, foreground='black')])

    # Display and save
    plt.savefig("figures/" + filename, pad_inches=0.1, bbox_inches='tight')


