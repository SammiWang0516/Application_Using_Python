'''
In [1]: change(48, [1, 5, 10, 25, 50])
Out[1]: 6
In [2]: change(48, [1, 7, 24, 42])
Out[2]: 2
In [3]: change(35, [1, 3, 16, 30, 50])
Out[3]: 3
In [4]: change(6, [4, 5, 9])
Out[4]: math.inf
'''
import math

def change(amount, coins):
    # coin count for output: list to store each posibility
    count_list = []
    max_coin = []
    count = 0

    def recursion(amount, coins, count):
        # base case
        if amount == 0 or not coins:
            return amount, count
        # if else condition
        # if current coin size is greater than the amount: pop that size and move to smaller one
        # if current coin size is smaller than the amount: amount - coin size
        if coins[-1] > amount:
            coins.pop()
            return recursion(amount, coins, count)
        elif coins[-1] <= amount:
            count += 1
            amount -= coins[-1]
            return recursion(amount, coins, count)

    for i in range(len(coins)):
        amount_left, coin_count = recursion(amount, coins[:len(coins) - i], count)
        if amount_left == 0:
            count_list.append(coin_count)

    if not count_list:
        return math.inf
    else:
        return min(count_list)

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

def giveChange(amount, coins):

    coin_combo = []
    coin_count = []

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

        coin_combo.append(temp)
        coin_count.append(count)

    min_count = min(coin_count)

    for combo in coin_combo:
        if len(combo) == min_count:
            return [min_count, combo]
    
amount = 48
coins = [1, 5, 10, 25, 50]
print(giveChange(amount, coins))
# output = [6, [25, 10, 10, 1, 1, 1]]
amount = 48
coins = [1, 7, 24, 42]
print(giveChange(amount, coins))
# output = [2, [24, 24]]