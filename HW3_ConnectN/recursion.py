import math

def change(amount, coins):
    '''
    1. Using a recursion helper function inside change function.
    2. Inside the recursion function, the base cases are amount equals 0 
        or coins list has no more element or amount is negative value
    3. with each recursion output, i have 2 ways to count the change
        either using current coin size, or i skip current coin size and use the smaller one
    4. then I output the minimum of coin count.

    Parameters:
        amount (int): the amount of money that needs changes
        coins (list of int): the sizes of coin
        count (int): the change counts

    Returns:
        math.inf: if the change cannot equal to amount of money
        int: change count for the amount
    '''

    # count the coins
    count = 0
    # sort the coin type
    coins = sorted(coins)

    def recursion(amount, coins, count):

        # base case: if amount is 0, that means the change count equals to amount
        if amount == 0:
            return count
        # base case: amount is negative value or no element in coins mean that such count is invalid
        if amount < 0 or not coins:
            return math.inf
        
        # use the current coin size to make change.
        use_it = recursion(amount - coins[-1], coins, count + 1)

        # skip the current coin size and ignore the last element
        skip_it = recursion(amount, coins[:-1], count)

        return min(use_it, skip_it)
    
    return recursion(amount, coins, count)

def giveChange(amount, coins):
    '''
    take argument amount and check the minimum combination of coin counts
    and return the combination

    Parameters:
        amount (int): the amount of money that needs changes
        coins (list of int): the sizes of coin

    Returns:
        min_count (int): minimum change count
        combo: the coin size combination of minimum change count
    '''

    coin_combo = []
    coin_count = []
    # sort the coin type
    coins = sorted(coins)

    for i in range(len(coins)):

        temp = []
        count = 0
        coin = coins[:len(coins)-i]
        j = 0
        amount_copy = amount

        while j < len(coin):
            if coin[-1-j] > amount_copy:
                j += 1
            else:
                count += 1
                temp.append(coin[-1-j])
                amount_copy -= coin[-1-j]

        if amount_copy == 0:
            coin_combo.append(temp)
            coin_count.append(count)

    if coin_count:
        min_count = min(coin_count)

    for combo in coin_combo:
        if sum(combo) == amount and len(combo) == min_count:
            return [min_count, combo]

    return [math.inf, []]

if __name__ == '__main__':

    # test for change function

    amount = 48
    coins = [1, 5, 10, 25, 50]
    print(change(amount, coins))
    # output = 6

    amount = 48
    coins = [1, 7, 24, 42]
    print(change(amount, coins))
    # output = 2

    amount = 35
    coins = [1, 3, 16, 30, 50]
    print(change(amount, coins))
    # output = 3

    amount = 6
    coins = [4, 5, 9]
    print(change(amount, coins))
    # output = math.inf

    amount = 38
    coins = [35, 11, 43, 16]
    print(change(amount, coins))
    # output = 3
    
    # test for change function

    amount = 48
    coins = [1, 5, 10, 25, 50]
    print(giveChange(amount, coins))
    # output = [6, [25, 10, 10, 1, 1, 1]]

    amount = 48
    coins = [1, 7, 24, 42]
    print(giveChange(amount, coins))
    # output = [2, [24, 24]]

    amount = 19
    coins = [10, 37, 47, 22, 25, 11]
    print(giveChange(amount, coins))
    # output = [inf, []]

    amount = 32
    coins = [14, 16, 29]
    print(giveChange(amount, coins))
    # output = [2, [16, 16]]