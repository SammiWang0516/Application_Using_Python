# make change
# Your first task is to write a function called change(amount, coins), where the 
# amount is a non-negative integer indicating the amount of change to be made 
# and coins are a list of coin values. The function should return a non-negative 
# integer indicating the minimum number of coins required to make up the given
# amount. If there is no possible solution, return math.inf
import math

def change(amount, coins):

    # make a list that contains inf index for amount
    result = [math.inf for i in range(amount+1)]
    result[0] = 0

    for i in range(1, amount+1):
        for coin in coins:
            if coin <= i:
                result[i] = min(result[i], 1 + result[i - coin])

    return result[amount]

def giveChange(amount, coins):

    # coin_count[i] = min coins to make amount i
    coin_count = [math.inf] * (amount + 1)
    coin_count[0] = 0

    # last_coin[i] = which coin was used last to make amount i
    last_coin = [None] * (amount + 1)

    # build dp
    for i in range(1, amount + 1):
        for coin in coins:
            if coin <= i and coin_count[i - coin] + 1 < coin_count[i]:
                coin_count[i] = 1 + coin_count[i - coin]
                last_coin[i] = coin

    # reconstruct the coins used
    if coin_count[amount] == math.inf:
        return [math.inf, []]   # no solution

    result = []
    current = amount

    while current > 0:
        result.append(last_coin[current])
        current -= last_coin[current]

    return [coin_count[amount], result] 