from enum import Enum

'''
This is the start of the HW.
If there is any conflict between the doc string and the HW document,
please follow the instruction in the HW document.
Good Luck and have fun !
'''

class Notation(Enum):
    """Enumeration for representing different types of notations in the game.

    Attributes:
        EMPTY (int): Represents an empty cell on the board. (default value is 0)
        PLAYER1 (int): Represents a cell occupied by Player 1. (default value is 1)
        PLAYER2 (int): Represents a cell occupied by Player 2. (default value 2)
    """
    EMPTY = '0'
    PLAYER1 = 'R'
    PLAYER2 = 'Y'

class Player:
    """Represents a player in the game.

    Attributes:
        __playerName (str): The name of the player.
        __playerNotation (Notation): The notation (symbol) used by the player on the board.
        __curScore (int): The current score of the player.

    Args:
        playerName (str): The name of the player.
        playerNotation (Notation): The notation (symbol) used by the player.
        curScore (int): The initial score of the player.
    """

    def __init__(self, playerName, playerNotation, curScore) -> None:
        self.__playerName = playerName
        self.__playerNotation = playerNotation
        self.__curScore = curScore

    def display(self) -> None:
        """Displays the player's details including name, current score, and notation."""
        return self.__playerName, self.__curScore, self.__playerNotation.value

    def addScoreByOne(self) -> None:
        """Increments the player's score by one."""
        self.__curScore += 1

    def getScore(self) -> int:
        """Returns the current score of the player."""
        return self.__curScore

    def getName(self) -> str:
        """Returns the name of the player."""
        return self.__playerName

    def getNotation(self) -> Notation:
        """Returns the notation used by the player."""
        return self.__playerNotation

class Board:
    """Represents the game board.

    Attributes:
        __rowNum (int): Number of rows in the board.
        __colNum (int): Number of columns in the board.
        __grid (list): 2D list representing the game board.

    Args:
        rowNum (int): Number of rows in the board.
        colNum (int): Number of columns in the board.
    """

    def __init__(self, rowNum, colNum) -> None:
        self.__rowNum = rowNum                                                              # private attribute rowNum (row count)
        self.__colNum = colNum                                                              # private attribute colNum (col count)
        self.__grid = [[Notation.EMPTY for _ in range(colNum)] for _ in range(rowNum)]      # create a 2D list contains 0 (index)

    def initGrid(self) -> None:
        """Initializes the game board with empty cells."""
        self.__grid = [[Notation.EMPTY for _ in range(self.__colNum)] for _ in range(self.__rowNum)]

    def getColNum(self) -> int:
        """Returns the number of columns in the board."""
        return self.__colNum

    def placeMark(self, colNum, mark) -> bool:
        """Attempts to place a mark on the board at the specified column.

        Args:
            colNum (int): The column number where the mark is to be placed. # this colNum is the 0-based index
            mark (Notation): The mark to be placed on the board.

        Returns:
            bool: True if the mark was successfully placed, False otherwise.
        """
        col_mark_vacant = False                                             # check if that column is vacant or not (by default full)
        empty_row = None                                                    # the row that is empty (default is None)

        if colNum < 0 or colNum >= self.__colNum:                           # check whether colNum is within self.colNum
            print("the column number shall be within the board")
            return False

        if mark == Notation.EMPTY:                                          # check whether the marker is EMPTY
            print("invalid marker")
            return False
        
        for i in range(self.__rowNum - 1, -1, -1):                          # iterate through the rows (count from bottom to top)
            if self.__grid[i][colNum] == Notation.EMPTY:
                col_mark_vacant = True
                empty_row = i
                break

        if not col_mark_vacant:                                             # the column is full
            print("column is full")
            return False
        
        self.__grid[empty_row][colNum] = mark                               # if there is empty space and colNum is not out of bound
                                                                            # fill the space with mark (object of Notation)
        return True

    def checkFull(self) -> bool:
        """Checks if the board is completely filled.

        Returns:
            bool: True if the board is full, False otherwise.
        """
        for i in range(self.__rowNum - 1, -1, -1):                          # count from bottom to top each row
            for j in range(self.__colNum):                                  # count from left to right each column
                if self.__grid[i][j] == Notation.EMPTY:                     # if there is one space that is empty
                    return False                                            # not full
        return True                                                         # otherwise it is completely full

    def display(self) -> None:
        """Displays the current state of the board."""
        boardStr = ""

        for i in range(self.__rowNum):
            for j in range(self.__colNum):
                if self.__grid[i][j] == Notation.EMPTY:
                    boardStr += 'O '
                elif self.__grid[i][j] == Notation.PLAYER1:
                    boardStr += 'R '
                else:
                    boardStr += 'Y '
            boardStr += '\n'

        print(boardStr)

    # Private methods for internal use
    def __checkWinHorizontal(self, target) -> Notation | None:
        for row in range(self.__rowNum):
            count_player1 = 0                                   # count the player1
            count_player2 = 0                                   # count for player2
            for col in range(self.__colNum):
                if self.__grid[row][col] == Notation.PLAYER1:
                    count_player1 += 1
                    if count_player2 != 0:
                        count_player2 = 0
                else:
                    count_player1 = 0

                if count_player1 == target:
                    return Notation.PLAYER1

                if self.__grid[row][col] == Notation.PLAYER2:
                    count_player2 += 1
                    if count_player1 != 0:
                        count_player1 = 0       
                else:
                    count_player2 = 0  

                if count_player2 == target:
                    return Notation.PLAYER2     

        return None      

    def __checkWinVertical(self, target) -> Notation | None:
        for col in range(self.__colNum):
            count_player1 = 0                                   # count the player1
            count_player2 = 0                                   # count for player2
            for row in range(self.__rowNum):
                if self.__grid[row][col] == Notation.PLAYER1:
                    count_player1 += 1
                    if count_player2 != 0:
                        count_player2 = 0
                else:
                    count_player1 = 0
                
                if count_player1 == target:
                    return Notation.PLAYER1

                if self.__grid[row][col] == Notation.PLAYER2:
                    count_player2 += 1
                    if count_player1 != 0:
                        count_player1 = 0       
                else:
                    count_player2 = 0  

                if count_player2 == target:
                    return Notation.PLAYER2 
        
        return None

    def __checkWinOneDiag(self, target, rowNum, colNum) -> Notation | None:
        current_mark = self.__grid[rowNum][colNum]          # the last move

        if current_mark == Notation.EMPTY:
            return None

        # diagonal check
        dr = -1                                             # top right direction and
        dc = 1                                              # bottom left direction

        count = 1                                           # current piece
        # top right direction
        # ↗ direction (dr = -1, dc = +1)
        r, c = rowNum + dr, colNum + dc
        while 0 <= r < self.__rowNum and 0 <= c < self.__colNum and self.__grid[r][c] == current_mark:
            count += 1
            r += dr
            c += dc
        
        # bottom left direction
        # ↙ direction (dr = +1, dc = -1)
        r, c = rowNum - dr, colNum - dc
        while 0 <= r < self.__rowNum and 0 <= c < self.__colNum and self.__grid[r][c] == current_mark:
            count += 1
            r -= dr
            c -= dc
        
        if count >= target:
            return current_mark

        return None


    def __checkWinAntiOneDiag(self, target, rowNum, colNum) -> Notation | None:
        current_mark = self.__grid[rowNum][colNum]          # the last move

        if current_mark == Notation.EMPTY:
            return None

        # diagonal check
        dr = -1                                             # top right direction and
        dc = -1                                             # bottom left direction

        count = 1                                           # current piece
        # top left direction
        # ↖ direction (dr = -1, dc = -1)
        r, c = rowNum + dr, colNum + dc
        while 0 <= r < self.__rowNum and 0 <= c < self.__colNum and self.__grid[r][c] == current_mark:
            count += 1
            r += dr
            c += dc
        
        # bottom right direction
        # ↘ direction (dr = +1, dc = +1)
        r, c = rowNum - dr, colNum - dc
        while 0 <= r < self.__rowNum and 0 <= c < self.__colNum and self.__grid[r][c] == current_mark:
            count += 1
            r -= dr
            c -= dc
        
        if count >= target:
            return current_mark
        
        return None

    def __checkWinDiagonal(self, target) -> Notation | None:
        for row in range(self.__rowNum):
            for col in range(self.__colNum):
                winner = self.__checkWinOneDiag(target, row, col)
                if winner is not None:
                    return winner

                winner = self.__checkWinAntiOneDiag(target, row, col)
                if winner is not None:
                    return winner

        return None

    def checkWin(self, target) -> Notation | None:
        """Checks if there is a winning condition on the board.

        Args:
            target (int): The number of consecutive marks needed for a win.

        Returns:
            Notation or None: The notation of the winning player, or None if there is no winner.
        """
        win_hor = self.__checkWinHorizontal(target)
        if win_hor is not None:
            return win_hor

        win_ver = self.__checkWinVertical(target)
        if win_ver is not None:
            return win_ver

        win_dia = self.__checkWinDiagonal(target)
        if win_dia is not None:
            return win_dia
        
        return None

class Game:
    """Represents the game logic and flow.

    Args:
        rowNum (int): Number of rows in the game board.
        colNum (int): Number of columns in the game board.
        connectN (int): Number of consecutive marks needed for a win.
        targetScore (int): The score a player needs to reach to win the game.
        playerName1 (str): Name of the first player.
        playerName2 (str): Name of the second player.
    """

    def __init__(self, rowNum, colNum, connectN, targetScore, playerName1, playerName2) -> None:
        self.__board = Board(rowNum, colNum)                            # rowNum & colNum are count
        self.__connectN = connectN                                      # target count of consecutive marks
        self.__targetScore = targetScore                                # target score
        player1 = Player(playerName1, Notation.PLAYER1, 0)
        player2 = Player(playerName2, Notation.PLAYER2, 0)
        self.__playerList = [player1, player2]
        self.__curPlayer = self.__playerList[0]

    def __playBoard(self, curPlayer) -> None:
        """Handles the process of a player making a move on the board.

        Args:
            curPlayer (Player): The current player who is making the move.
        """
        isPlaced = False

        while not isPlaced:
            # keep asking until valid input is given
            colNum = input(f"{self.__curPlayer.getName()}, input a column number: ")

            # 1. must be digits only
            if not colNum.isdigit():
                print("Input a valid column number! (digits only)")
                continue

            # 2. reject leading zero like "01" or "007"
            if len(colNum) > 1 and colNum[0] == "0":
                print("Input a valid column number! (no leading zeros)")
                continue

            # 3. safe to convert
            colNum = int(colNum)

            # 4. try to place the mark; if False → re-prompt
            if self.__board.placeMark(colNum, self.__curPlayer.getNotation()):
                isPlaced = True
            else:
                print("That column is full or invalid. Try another one.")


    def __changeTurn(self) -> None:
        """Switches the turn to the other player."""
        if self.__curPlayer == self.__playerList[0]:                                 # if it is player 1
            self.__curPlayer = self.__playerList[1]                                 # change to player 2
        else:
            self.__curPlayer = self.__playerList[0]                                 # change to player 1

    def playRound(self) -> None:
        curWinnerNotation = None                                                    # no winner (set to None)

        while not curWinnerNotation:                                                # keep trying rounds until a winner
            self.__board.initGrid()                                                 # reset the game board

            self.__curPlayer = self.__playerList[0]                                 # first player in player list

            print('Starting a new round!')

            while True:                                                             # moves within a round
                self.__curPlayer.display()                                          # display current player's info
                self.__board.display()                                              # display current state of the board
                self.__playBoard(self.__curPlayer)                                  # current player play the board

                curWinnerNotation = self.__board.checkWin(self.__connectN)

                if curWinnerNotation:                                               # board is not full and have a winner
                    self.__board.display()                                          # display the game board
                    self.__curPlayer.addScoreByOne()                                # add one score to the current player
                    break
                elif self.__board.checkFull():
                    print('board is full and no winner for this round')
                    break
                else:
                    self.__changeTurn()                                             # change the current player

    def play(self) -> None:
        """Starts and manages the game play until a player wins."""
        while True:
            self.playRound()
            if self.__curPlayer.getScore() == self.__targetScore:
                break

        print('Game Over')
        print('Name, Score, Mark')
        print(self.__playerList[0].display())
        print(self.__playerList[1].display())
"""
############################## Homework ConnectN ##############################

% Student Name: Sammi Wang

% Student Unique Name: dsammi

% Lab Section 00X: 003

% I worked with the following classmates: None

%%% Please fill in the first 4 lines of this file with the appropriate information.
"""

def main():
    """Main function to start the game."""
    game = Game(8, 8, 4, 2, 'P1', 'P2')
    game.play()

if __name__ == "__main__":
    main()
