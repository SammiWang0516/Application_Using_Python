class TwentyQuestions:
    def __init__(self):
        """
        Initialize the TwentyQuestions class with predefined small and medium trees.
        Sets the current tree to the small tree by default.
        """

        # small tree has only one question node, that is bigger than breadbox or not
        # if it is bigger than breadbox, then the program consider it as an elephant
        # if it is not, then the program consider it as a mouse
        self.smallTree = (
            "Is it bigger than a breadbox?",
            ("an elephant", None, None),
            ("a mouse", None, None),
        )

        # one more question node after user select yes
        # if users select it is bigger than a breadbox, then they will be asked another
        # further question, whether it is gray or not
        # if it is, it is an elephant. if it is not, a tiger it is
        # if it is not bigger than a breadbox, a mouse it is
        self.mediumTree = (
            "Is it bigger than a breadbox?",
            ("Is it gray?", ("an elephant", None, None), ("a tiger", None, None)),
            ("a mouse", None, None),
        )

        # default tree contains only one question
        self.currentTree = self.smallTree  # Default tree

    def inputChecker(self, userIn: str) -> bool:
        """
        aka(yes(userIn))
        Check if the user's input is an affirmative response.

        Parameters
        ----------
        userIn : str
            The input string from the user.

        Returns
        -------
        bool
            True if the input is an affirmative response ('y', 'yes', 'yup', 'sure'), else False.
        """

        affirmative_response = ["y", "yes", "yup", "sure"]

        # remove white space and make the user's response all lowercase
        # and check whether the response falls in our default response
        if userIn.strip().lower() in affirmative_response:
            return True
        else:
            return False

    def checkIfLeaf(self, curNode) -> bool:
        """
        Determine if the given node is a leaf node.

        Parameters
        ----------
        curNode : tuple
            The current node in the decision tree.

        Returns
        -------
        bool
            True if the node is a leaf (both children are None), else False.
        """

        # the node (tuple) is always a tuple consists of 3 tuples
        # the first tuple would always be a question
        # second node would be a yes branch that contains further questions
        # third node would be a no branch that contains further questions
        # Thus, to check whether such node is a leaf node, check the second tuple
        # and third tuple and see they are None or not
        return True if curNode[1] is None and curNode[2] is None else False

    def simplePlay(self, curNode) -> bool:
        """
        Conduct a simple playthrough of the game using the current node.

        Parameters
        ----------
        curNode : tuple
            The current node in the decision tree.

        Returns
        -------
        bool
            True if the player successfully guesses the item, else False.
        """

        # return True if the program successfully guesses the item, else is False
        # traverse down the tree and stop when it reach the None (leaf node)
        # if such branch is yes branch, return True. Else returns False

        # check such node is a leaf node or not, lets go with it is
        if curNode[1] is None and curNode[2] is None:
            userInput = input(f"is it {curNode[0]}? ")

            # if it is a yes or positive input
            if self.inputChecker(userInput):
                print("I got it!")
                return True
            else:
                print("Drats! I was wrong.")
                return False

        # if such node is not a leaf node, meaning we can still traverse down
        else:
            userInput = input(curNode[0] + " ")
            if self.inputChecker(userInput):
                return self.simplePlay(curNode[1])      # recursively traverse yes branch
            else:
                return self.simplePlay(curNode[2])      # recursively traverse no branch

    def createNode(self, userQuestion: str, userAnswer: str, isCorrectForQues: bool, curNode: tuple) -> tuple:
        """
        Create a new node in the decision tree.

        Parameters
        ----------
        userQuestion : str
            The question to differentiate the new answer from the current node.
        userAnswer : str
            The answer provided by the user.
        isCorrectForQues : bool
            True if the userAnswer is the correct response to the userQuestion.
        curNode : tuple
            The current node in the decision tree at which the game has arrived. 
            This node typically represents the point in the game 
            where the player's guess was incorrect, 
            and a new question-answer pair needs to be 
            added to refine the tree. 


        Returns
        -------
        tuple
            The new node created with the user's question and answer 
            and curNode
        """

        # check the isCorrectForQues first so that we can know such node's pattern
        # if isCorrectForQues is true, meaning the answer shall fall in the yes branch
        if isCorrectForQues:
            return (userQuestion, (userAnswer, None, None), curNode)
        else:
            return (userQuestion, curNode, (userAnswer, None, None))

    def playLeaf(self, curNode) -> tuple:
        """
        Handle gameplay when a leaf node is reached in the decision tree. This method is called when 
        the game's traversal reaches a leaf node, indicating a guess at the player's thought. 
        If the guess is incorrect, the method will
        1. prompts the player for the correct answer 
        2. prompts the player for a distinguishing question
        3. ask user what is the answer for the new input item to this distinguishing question(refer the io result of play in the homework doc)
           notice the node should follow (tree question, (node for answer yes), (node for answer no))
        4. creating a new node in the tree for future gameplay. It should call self.createNode(...)

        Parameters
        ----------
        curNode : tuple
            The current leaf node in the decision tree. A leaf node is represented as a tuple with the guessed 
            object as the first element and two `None` elements, signifying that it has no further branches.

        Returns
        -------
        tuple
            The updated node based on user input. If the player's response indicates that the initial guess was 
            incorrect, this method returns a new node that includes the correct answer and a new question 
            differentiating it from the guessed object. If the guess was correct, it simply returns the unchanged 
            `curNode`.
        
        Notes
        -----
        The method interacts with the player to refine the decision tree. It's a crucial part of the learning 
        aspect of the game, enabling the tree to expand with more nuanced questions and answers based on 
        player feedback.
        """

        # the background of implementing such function is that the user reach the leaf node
        # but still the program is not able to find the answer
        # such function return a tuple
        # if the guess is correct, return curNode. But if it is not, return a new node
        userInput = input(f"Is it {curNode[0]}? ")
        # response is positive and such node is a leaf node, return curNode
        if self.inputChecker(userInput):
            print("I got it!")
            return curNode
        
        # if it is not the correct answer, return a new tuple
        # user answer first
        userAnswer = input("Drats! What was it? ")

        # distinguish question
        distinguishQuestion = input(f"What's a question that distinguishes between {userAnswer} and {curNode[0]}? ")

        # userCorrect
        userCorrectResponse = input(f"And what's the answer for {userAnswer}? ")

        isCorrectForQues = self.inputChecker(userCorrectResponse)

        return self.createNode(distinguishQuestion, userAnswer, isCorrectForQues, curNode)


    def play(self, curNode) -> tuple:
        """
        Conduct gameplay starting from the given node.

        Parameters
        ----------
        curNode : tuple
            The current node in the decision tree.

        Returns
        -------
        tuple
            The updated tree after playing from the given node.
        """

        # unlike simplePlay, this play function actually learn the user input
        # and output the new tree (include the new node learned from user)

        # start from checking whether such node is a leaf node or not
        # if it is, run playLeaf function 
        if self.checkIfLeaf(curNode):
            return self.playLeaf(curNode)

        userInput = input(curNode[0] + " ")

        if self.inputChecker(userInput):
            updateYes = self.play(curNode[1])
            return (curNode[0], updateYes, curNode[2])
        else:
            updateNo = self.play(curNode[2])
            return (curNode[0], curNode[1], updateNo)

    def playRound(self) -> None:
        """
        Execute a single round of the game, starting from the current state of the currentTree attribute. This method 
        calls the 'play' method to navigate through the tree. It then updates the 'currentTree' 
        attribute with the potentially modified tree resulting from this round of gameplay.

  
        Returns
        -----
        None
        """
        # store the tree after playing one round to self.currentTree
        self.currentTree = self.play(self.currentTree)


    def saveTree(self, node, treeFile) -> None:
        """
        Recursively save the decision tree to a file.

        Parameters
        ----------
        node : tuple
            The current node in the decision tree.
        treeFile : _io.TextIOWrapper
            The file object where the tree is to be saved.
        """

        # case 1: leaf node
        if self.checkIfLeaf(node):
            print("Leaf", file = treeFile)
            print(node[0], file = treeFile)
            return
        
        # case 2: internal node
        print("Internal node", file = treeFile)
        print(node[0], file = treeFile)

        # recursively save yes branch (sample comes first)
        self.saveTree(node[1], treeFile)

        # recursively save no branch (sample comes second)
        self.saveTree(node[2], treeFile)

    def saveGame(self, treeFileName) -> None:
        """
        Save the current state of the game's decision tree to a specified file. This method opens the file 
        with the given filename and writes the structure of the current decision tree to it. The tree is saved 
        in a txt format.

        The method uses the 'saveTree' function to perform the recursive traversal and writing of the tree 
        structure. Each node of the tree is written to the file with its type ('Leaf' or 'Internal node') 
        followed by its content (question or object name). 

        Important: the format of the txt file should be exactly the same as the ones in our doc to pass the autograder. 
        
        Parameters
        ----------
        treeFileName : str
            The name of the file where the current state of the decision tree will be saved. The file will be 
            created or overwritten if it already exists.

        """

        # open the file for writing
        treeFile = open(treeFileName, "w")

        # write the current tree into the file with the designated file name
        self.saveTree(self.currentTree, treeFile)

        # must close the file
        treeFile.close()


    def loadTree(self, treeFile) -> tuple:
        """
        Recursively read a binary decision tree from a file and reconstruct it.

        Parameters
        ----------
        treeFile : _io.TextIOWrapper
            An open file object to read the tree from.

        Returns
        -------
        tuple
            The reconstructed binary tree.
        """

        # read the tree in the treeFile and write it in the self.currentNode
        # treeFile is a file handle, not the file
        # we readline (line by line)
        line = treeFile.readline().strip()

        if line == "Leaf":
            answer = treeFile.readline().strip()
            return (answer, None, None)

        elif line == "Internal node":
            question = treeFile.readline().strip()
            yes_subtree = self.loadTree(treeFile)
            no_subtree = self.loadTree(treeFile)
            return (question, yes_subtree, no_subtree)

    def loadGame(self, treeFileName) -> None:
        """
        Load the game state from a specified file and update the current decision tree. This method opens the 
        file with the given filename and reconstructs the decision tree based on its contents. 

        The method employs the 'loadTree' function to perform recursive reading of the tree structure from the 
        file. Each node's type ('Leaf' or 'Internal node') and content (question or object name) are read and 
        used to reconstruct the tree in memory. This restored tree becomes the new 'self.currentTree' of the game.

        Parameters
        ----------
        treeFileName : str
            The name of the file from which the game state will be loaded. The file should exist and contain a 
            previously saved decision tree.

        """

        # oepn the file for reading
        treeFile = open(treeFileName, "r")

        # write the tree inside the file to currentNode
        self.currentTree = self.loadTree(treeFile)

        # must close the file
        treeFile.close()


    def printTree(self):
        self._printTree(tree = self.currentTree)

    def _printTree(self, tree, prefix = '', bend = '', answer = ''):
        """Recursively print a 20 Questions tree in a human-friendly form.
        TREE is the tree (or subtree) to be printed.
        PREFIX holds characters to be prepended to each printed line.
        BEND is a character string used to print the "corner" of a tree branch.
        ANSWER is a string giving "Yes" or "No" for the current branch."""
        text, left, right = tree
        if left is None  and  right is None:
            print(f'{prefix}{bend}{answer}It is {text}')
        else:
            print(f'{prefix}{bend}{answer}{text}')
            if bend == '+-':
                prefix = prefix + '| '
            elif bend == '`-':
                prefix = prefix + '  '
            self._printTree(left, prefix, '+-', "Yes: ")
            self._printTree(right, prefix, '`-', "No:  ")
"""
############################## Homework 20questions ##############################

% Student Name: Sammi Wang

% Student Unique Name: dsammi

% Lab Section 00X: 003

% I worked with the following classmates: Alone

%%% Please fill in the first 4 lines of this file with the appropriate information.
"""

def main():
    """
    First I instantiate one object of the game and print the welcome message

    then, I prompt the user to load the file or not
    if the user select yes, then we load the file and refresh the current tree node
    if not, then we just start from the small tree that we wrote in the attribute
    
    Later, I used a while loop to keep on playing the game until the user said
    no to the game.

    if the game is ended, I asked the user whether to save the current tree for later
    if the user select yes, then we can save the tree into the file name that the
    user typed.

    then go back to the very first line after rerun (since I already have the file
    the user save, we can then load the file)
    """
    # Write the "main" function for 20 Questions here.  Although
    # main() is traditionally placed at the top of a file, it is the
    # last function you will write.

    # first welcome wording
    game = TwentyQuestions()
    print("Welcome to 20 Questions!")

    # load a tree from a file
    existingTreeFile = input("Would you like to load a tree from a file? ")

    # if the user choose yes, then prompt him / her the file name
    # positive response
    if game.inputChecker(existingTreeFile):
        treeFileName = input("What's the name of the file? ")
        game.loadGame(treeFileName)
    else:
        game.currentTree = game.smallTree
    
    # keep playing until user says no
    while True:
        game.playRound()

        again = input("Would you like to play again? ")
        if not game.inputChecker(again):
            break
    
    # ask if the user want to save the tree
    saveChoice = input("Would you like to save this tree for later? ")
    if game.inputChecker(saveChoice):
        fileName = input("Please enter a file name: ")
        game.saveGame(fileName)
        print("Thank you! The file has been saved.")
    
    print("Bye!")

    game.printTree()

if __name__ == '__main__':
    main()
