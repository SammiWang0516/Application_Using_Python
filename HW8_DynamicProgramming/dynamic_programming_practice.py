# make change
# Your first task is to write a function called change(amount, coins), where the 
# amount is a non-negative integer indicating the amount of change to be made 
# and coins are a list of coin values. The function should return a non-negative 
# integer indicating the minimum number of coins required to make up the given
# amount. If there is no possible solution, return math.inf
import math

def change(amount, coins):

    def recursion(amount, coins, count):

        # base case: if amount is 0, meaning the change count equals to amount
        if amount == 0:
            return count
        # base case: amount is negative value or no element in coins, meaning such count is invalid
        if amount < 0 or not coins:
            return math.inf
        
        # use the current coin size to make change
        use_it = recursion(amount - coins[-1], coins, count+1)
        # pass the current coin size
        skip_it = recursion(amount, coins[:-1], count)

        return min(use_it, skip_it)

    count = 0

    sort_coins = sorted(coins)

    change_count = recursion(amount, sort_coins, count)

    return change_count

amount = 48
coins = [1, 5, 10, 25, 50]
print(change(amount, coins))

amount = 48
coins = [1, 7, 24, 42]
print(change(amount, coins))

amount = 35
coins = [1, 3, 16, 30, 50]
print(change(amount, coins))

amount = 6
coins = [4, 5, 9]
print(change(amount, coins))

def changeDPTopDown(amount, coins):

    # use a memo to memorize the combination of i (index of coin) and amount left
    # for this combination, it will always has an exact best result (min result of coin change)
    # for example, [1, 3, 4] and amount = 6
    # (0, 6) = 2 | take [1, 3, 4] into acount, 6 is the remaining amount and 2 is the min coin change
    memo = {}

    coins = sorted(coins)

    def recursion(i, amount):

        # base case: if the amount is 0, meaning we reach the coin change that can meet the amount
        if amount == 0:
            return 0

        # base case: if the amount is less than 0 or reach all coins
        if amount < 0 or i == len(coins):
            return math.inf

        # memorization
        if (i, amount) in memo:
            return memo[(i, amount)]
        
        # use it or skip it
        skip_it = recursion(i + 1, amount)
        use_it = 1 + recursion(i, amount - coins[i])

        memo[(i, amount)] = min(skip_it, use_it)

        return memo[(i, amount)]

    return recursion(0, amount)

amount = 48
coins = [1, 5, 10, 25, 50]
print(changeDPTopDown(amount, coins))

amount = 48
coins = [1, 7, 24, 42]
print(changeDPTopDown(amount, coins))

amount = 35
coins = [1, 3, 16, 30, 50]
print(changeDPTopDown(amount, coins))

amount = 6
coins = [4, 5, 9]
print(changeDPTopDown(amount, coins))


def changeDPBottomUp(amount, coins):

    # make a list that contains inf index for amount
    result = [math.inf for i in range(amount+1)]
    result[0] = 0

    for i in range(1, amount+1):
        for coin in coins:
            if coin <= i:
                result[i] = min(result[i], 1 + result[i - coin])

    return result[amount]

amount = 6
coins = [1, 2, 3]
print(changeDPBottomUp(amount, coins))

def givingChangeDPBottomUp(amount, coins):

    import math

def givingChangeDPBottomUp(amount, coins):

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

amount = 6
coins = [1, 2, 3]
print(givingChangeDPBottomUp(amount, coins))     