import random
random.seed(17)

# BaconCast_00_06: movies released since 2000 to 2006 [movies=52195, actors=348497]
# Bacon_06: movies released in 2006 [movies=8780, actors=84236]
# ActionCast: action movies
# PopularCast: popular movies

class BaconNumberCalculator:
    """
    A class to calculate the Kevin Bacon number in a network of actors.

    Parameters
    ----------
    fileName : str
        The name of the file containing the movie data.

    Attributes
    ----------
    adjList : dict of dict/dict of list/ dict of tuple/etc...

    Methods
    -------
    generateAdjList(fileName)
        Constructs the adjacency list from the given file.
    
    calcBaconNumber(startActor, endActor)
        Calculates the Bacon number between two actors.
    
    calcAvgNumber(startActor, threshold)
        Calculates the average Bacon number for a given actor.
    """

    def __init__(self, fileName) -> None:
        """
        Constructs all the necessary attributes for the BaconNumberCalculator object.

        Parameters
        ----------
        fileName : str
            The name of the file containing the movie data.
        """
        self.adjList = {}
        self.generateAdjList(fileName)

    def generateAdjList(self, fileName) -> None:
        """
        Reads a file and builds an adjacency list representing actor connections.

        Parameters
        ----------
        fileName : str
            The name of the file to read the movie data from.
            You need to think about which encoding you should use,
	        To load the file.

        
        Attributes
        ----------
        adjList : dict of dict/dict of list/ dict of tuple/etc...
        The key of the adjList should be the original(unmodified) actor name
        in the inputted file. You should not and do not need to modify it.
        For example:
        Bacon, Kevin
        Kidman, Nicole


        Note
        ----------
        Adjacency list representing the actor connections.
        For example: 
        adjList = {actor1 : {{actor2: movie1} ,{actor3: movie1}} }
        or 
        adjList = {actor1 : [[actor2,movie1],[actor3, movie1]]}
        or
        ...

        Hint
        ------
	    1. As the size of our graph increases, which of the adjacency   
 	    lists mentioned above is more efficient for graph building? 
        2. Do we need all of the movie information/name in which two 
        actors performed together stored in the adjList? 
        Or just one pair is sufficient? 
        ie  {actor1 : {actor2: movie1} }
        not  {actor1 : {actor2: [movie1,movie2]} }
        Think about how many pathes we need to find between the inputted actor,
        just one or many. 
         

        Returns
        -------
        None
        """
        # Method implementation...
        # read the file with fileName
        file = open(fileName, "r", encoding = "latin-1")

        # read through every line and divide the long line into strings divided by "/"
        # movie is the first string while others are actors in the movie
        for line in file:
            line = line.strip()
            parts = line.split("/")

            movie = parts[0]
            actors = parts[1:]

            # make sure each actor exists in the adjacency list
            for actor in actors:
                if actor not in self.adjList:
                    self.adjList[actor] = {}
            
            # add edges
            for i in range(len(actors)):
                for j in range(i+1, len(actors)):
                    left_actor = actors[i]
                    right_actor = actors[j]

                    # add edge both directions (undirected)
                    if left_actor not in self.adjList[right_actor]:
                        self.adjList[right_actor][left_actor] = movie
                    if right_actor not in self.adjList[left_actor]:
                        self.adjList[left_actor][right_actor] = movie
        
        file.close()

    def calcBaconNumber(self, startActor, endActor) -> list[int | list[str]]:
        """
        Calculates the Bacon number (shortest path) between two actors.

        Parameters
        ----------
        startActor : str
            The name of the starting actor.
        endActor : str
            The name of the ending actor.

        Returns
        -------
        List[int, List[str]]
            A List containing the Bacon number and the path of connections.
            The second List should be in the following form.
            [startActor, moive1, actor1, moive2,actor1, movie3,endActor]

        Note
        -------
        1.A local variable visited:set() is needed, which aviod visiting the same
        actor more than once. 

        2.List should not be used to simulate the behavior of a queue.
        related reading:https://docs.python.org/3/tutorial/datastructures.html
        solution to is question is in the next line of the reason in the website

        3. It should return [-1, []], if one of the inputted actor is not
        in our graph.

        4.It should return [0, [start actor]], if the start actor is the end actor

        Hint
        -------
        What infomation you should store in the queue?
        Should it be the whole current path, or a single actor, or a tuple with 
        length of two?

        If the whole path, think about how many new list object you might create
        during the process. Notice, create a new list is not very time efficient.

        If a single actor, think about how to reconstruct the path from startActor
        to endActor. Will you need a dictionary to do so? 

        If a tuple, think about what information need to be in the tuple, and 
        how to reconstruct the path. Will you need a dictionary to do so? 

        BFS is a search algorithm that extends step by step, so if a point is traversed, 
        there is one and only one path to the point due to the visited set. 
        Each time, you enqueue an actor, 
        record the actor and movie before it in a dictionary.

        """

        # Method implementation...
        from collections import deque

        # if the inputted actor is not in our graph
        if startActor not in self.adjList.keys() or endActor not in self.adjList.keys():
            return [-1, []]

        # if the start actor is the end actor
        if startActor == endActor:
            return [0, [startActor]]

        # traverse using BFS
        # first we define a set that store every visited actor name
        visited_actor = set()

        # establish a queue to traverse BFS
        d = deque()

        # history to get the shortest traverse history from startActor to endActor
        # parent[childActor] = parentActor
        # parentMovie[childActor] = movieUsedToReachThem
        parent = {}
        parentMovie = {}

        # first start from the startActor, append the first startActor
        # add such actor to visited_actor set
        # parent[startActor] = None
        # parentMovie[startActor] = None
        d.append(startActor)
        visited_actor.add(startActor)
        parent[startActor] = None
        parentMovie[startActor] = None

        # bool variable stands for finding the endActor
        found = False

        # if the queue has element, keep going on poping
        while d and not found:

            current_actor = d.popleft()

            for neighbor_actor in self.adjList[current_actor]:

                if neighbor_actor not in visited_actor:
                    # movie is from the current actor's neighbor actor
                    movie = self.adjList[current_actor][neighbor_actor]
                    # neighbor actor's parent actor is current actor
                    parent[neighbor_actor] = current_actor
                    # neighbor actor's parent movie is the movie that connects the current actor and him/her
                    parentMovie[neighbor_actor] = movie
                    # add the neighbor actors into queue (for further traverse)
                    d.append(neighbor_actor)
                    # add the visited actor
                    visited_actor.add(neighbor_actor)

                    # if the neighbor actor is end actor, we find him and can stop the loop
                    if neighbor_actor == endActor:
                        found = True
                        break
        
        # if endActor is not reachable from startActor, return [-1, []]
        if endActor not in parent:
            return [-1, []]

        # reconstruct the logic
        # build path backward
        path = []
        current = endActor

        while current is not None:

            # add such actor in the path
            path.append(current)

            movie = parentMovie[current]
            if movie is not None:
                path.append(movie)
            
            current = parent[current]
        
        # since above codes record path from child to parent, we reverse the path
        # so the path is now from startActor to endActor
        path.reverse()

        return [(len(path) - 1) // 2, path]


    def calcAvgNumber(self, startActor, threshold) -> float:
        """
        Calculates the average Bacon number for a given actor until convergence.

        The method iteratively selects a random actor and computes the Bacon number 
        from the startActor to this random actor. It updates and calculates the 
        average Bacon number. This process continues until the difference between 
        successive averages is less than the specified threshold, indicating convergence.

        pseudocode 
        ----------
        Initialize previousAvg to 0, curDiff to a large number (acting as infinity)
        Create a list of all possible actors from the adjacency list.
        Enter a while loop that continues as long as curDiff is greater than the threshold.
        a. Increment round count.
        b. Choose a random actor from the list of possible actors.
        c. Calculate the Bacon number (bNum) from startActor to the chosen actor.
        d. If bNum is valid (not -1 and not 0):
            addjust totalBNum and calculate the difference (curDiff) between the current and previous averages.
            Update previousAvg to the current average.
        e. If bNum is invalid, exclude it and adjust round count, undo the effect of this unsuccessful round.
        Return the previousAvg once the loop exits.

        Parameters
        ----------
        startActor : str
            The actor for whom the average Bacon number is to be calculated.
        threshold : float
            The convergence threshold for the average calculation.

        Returns
        -------
        float
            The converged average Bacon number for the startActor.
        
        # Method implementation...
        """
        if startActor not in self.adjList:
            return -1

        # last average
        previousAvg = 0
        # difference between averages
        curDiff = float("inf")
        # sum of all valid bacon numbers
        totalBNum = 0
        # how many valid samples we used
        roundCount = 0

        all_actor = list(self.adjList.keys())

        # estimate the average bacon number using random actors until the number stabilizes
        while curDiff > threshold:

            roundCount += 1

            random_actor = random.choice(all_actor)

            bNum, _ = self.calcBaconNumber(startActor, random_actor)

            if bNum == -1 or bNum == 0:
                # skip the round
                roundCount -= 1
                continue
            
            totalBNum += bNum

            currentAvg = totalBNum / roundCount

            curDiff = abs(currentAvg - previousAvg)

            previousAvg = currentAvg

        return previousAvg
"""
############################## Homework kevin_bacon ##############################

% Student Name: Sammi Wang

% Student Unique Name: dsammi

% Lab Section 00X: 003

% I worked with the following classmates: Alone

%%% Please fill in the first 4 lines of this file with the appropriate information.
"""

def main():
    
    calculator = BaconNumberCalculator("PopularCast.txt")

    print(calculator.calcBaconNumber('Raimondi, Constantino', 'Anderson, Jeff (XI)'))

    print(calculator.calcAvgNumber("Cohan, Lauren", 0.02))

if __name__ == "__main__":
    main()