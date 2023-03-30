percentiles = [
    [ 0,  2,  2,  3,  5,  8, 10,  13, 14, 12, 14, 14, 17],
    [ 5,  1,  3,  3,  6, 10, 16,  19, 24, 25, 25, 26, 26],
    [ 8,  9,  1,  5,  6, 10, 19,  26, 28, 29, 29, 30, 31],
    [12, 14, 15,  2,  6, 11, 17,  27, 33, 35, 37, 37, 38],
    [18, 20, 22, 21,  4, 10, 16,  25, 31, 40, 40, 41, 41],
    [32, 35, 36, 34, 31,  7, 17,  24, 29, 38, 47, 47, 49],
    [39, 50, 53, 48, 43, 42,  9,  21, 27, 33, 40, 53, 54],
    [45, 57, 66, 64, 59, 55, 52,  12, 25, 28, 37, 45, 56],
    [51, 60, 71, 80, 74, 68, 61,  57, 16, 27, 29, 38, 49],
    [44, 63, 75, 82, 89, 83, 73,  65, 58, 20, 28, 32, 39],
    [46, 67, 76, 85, 90, 95, 88,  78, 70, 62, 23, 36, 41],
    [49, 67, 77, 86, 92, 96, 98,  93, 81, 72, 76, 23, 46],
    [54, 69, 79, 87, 94, 97, 99, 100, 95, 84, 86, 91, 24]
]

def canonicalCardsToPercentile(s1, s2):
    r, c = canonicalCardsToIndex(s1, s2)
    return percentiles[r][c]

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