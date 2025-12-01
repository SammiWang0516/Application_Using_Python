# typing module is part of Python's type hinting system (PEP 484)
# allows annotate the code so IDEs, linters and static analyzers can check types before runtime
# Any: this can be any type
from typing import Any

class Node:
    """
    A node in a doubly linked list.

    Attributes
    ----------
    data : Any
        The data stored in the node.
    next : Node or None
        The next node in the linked list.
    prev : Node or None
        The previous node in the linked list.

    Parameters
    ----------
    data : Any, optional
        The data to be stored in the node (default is None).
    """
    
    def __init__(self, data: Any = None) -> None:
        self.data: Any = data
        # 'Node | None' is a type hint, meaning the next attribute will either a Node or None
        self.next: 'Node | None' = None
        self.prev: 'Node | None' = None

class LinkedList:
    # dummy head and dummy tail are conveinent in double linked list
    # None ← [dummy head] ↔ [A] ↔ [B] ↔ [C] ↔ [dummy tail] → None
    """
    A doubly linked list with dummy head and tail nodes to simplify node insertion and deletion.
    We require using dummyHead and dummyTail, since it will make certain implementation easier.
    Notice, the linked list is zero indexed.  

    Attributes
    ----------
    dummyHead : Node
        A dummy head node of the linked list.
    dummyTail : Node
        A dummy tail node of the linked list.
    size : int
        The number of elements in the linked list.

    Methods
    -------
    get(index)
        Retrieves the data at the specified index in the linked list.

    appendLeft(data)
        Adds a node with the given data at the beginning of the linked list.

    append(data)
        Adds a node with the given data at the end of the linked list.

    popLeft()
        Removes and returns the data from the beginning of the linked list.

    pop()
        Removes and returns the data from the end of the linked list.

    addAtIndex(index, data)
        Adds a node with the given data at the specified index in the linked list.

    deleteAtIndex(index)
        Deletes the node at the specified index from the linked list.

    printFromFront()
        Prints all elements of the linked list from front to back.

    printFromBack()
        Prints all elements of the linked list from back to front.

    _isNodeUnbound(node)
        Checks if the given node's linkage in the list is broken. 
        More specifically, check if the node is removed.

    getFront()
        Returns the data from the front (head) of the linked list.

    getBack()
        Returns the data from the back (tail) of the linked list.

    getSize()
        Returns the number of elements in the linked list.
    """

    def __init__(self) -> None:
        """
        Initializes a LinkedList instance with dummy head and tail nodes and sets size to zero.
        Notice data attribute of the dummyHead and dummyTail is None
        """
        self.dummyHead = Node(None)
        self.dummyTail = Node(None)
        self.dummyHead.next = self.dummyTail
        self.dummyTail.prev = self.dummyHead
        self.size = 0
    
    def get(self ,index: int) -> Any | None:
        """
        Retrieve the data at the specified index in the linked list.
        If the index is invalid, ie out of range, return None.


        Parameters
        ----------
        index : int
            The index of the node whose data is to be retrieved.

        Returns
        -------
        any or None
            The data at the specified index or None if index is invalid.
        """
        if index < 0 or index >= self.size:
            return None
        
        # current node is dummy head's next node
        curr = self.dummyHead.next

        for i in range(index):
            curr = curr.next
        
        return curr.data


    def appendLeft(self, data) -> None:
        """
        Create a new node, and assign the data to the new node.
        Add the node with the given data at the beginning of the linked list.
        Reset the positional relation(the next and prev attribute) of three
        related nodes.
        Increment the size by one.

        Parameters
        ----------
        data : any
            The data to be stored in the new node.

        Returns
        -------
        None
        """
        new_node = Node(data)

        # put the new node at the beginning of the linked list
        # first, its next would be dummyHead's next node
        # second, its prev would be dummyHead
        new_node.next = self.dummyHead.next
        new_node.prev = self.dummyHead

        # then deal with neighbors
        # dummyHead's next node would be new node
        # dummyHead's next node previous would be new node
        self.dummyHead.next.prev = new_node
        self.dummyHead.next = new_node

        # add size += 1
        self.size += 1

    def append(self, data) -> None:
        """
        Add a node with the given data at the end of the linked list.
        Reset the positional relation(the next and prev attribute) of three
        related nodes.
        Increment the size by one.

        Parameters
        ----------
        data : any
            The data to be stored in the new node.

        Returns
        -------
        None
        """
        new_node = Node(data)

        # first define the position of the new node
        # new_node's next node would be dummyTail
        # new_node's previous node would be dummyTail's previous node
        new_node.next = self.dummyTail
        new_node.prev = self.dummyTail.prev

        # then define the position of neighbors
        self.dummyTail.prev.next = new_node
        self.dummyTail.prev = new_node

        # size += 1
        self.size += 1

    def popLeft(self) -> Any | None:
        """
        Remove and return the data from the beginning of the linked list.
        Decrease the size by one.
        Reset the positional relation(the next and prev attribute) of three
        related nodes.

        Returns
        -------
        any
            The data of the removed node, or None if the list is empty.

        None 
            If the linked list is empty.
        """
        # return None if dummyHead's next node is dummyTail
        if self.dummyHead.next == self.dummyTail:
            return None
        
        # if there is actually some nodes in between
        # fix its neighbors behavior
        curr = self.dummyHead.next
        self.dummyHead.next = curr.next
        curr.next.prev = self.dummyHead

        # size -= 1
        self.size -= 1

        return curr.data

    def pop(self) -> Any | None:
        """
        Remove and return the data from the end of the linked list.
        Decrease the size by one.
        Reset the positional relation(the next and prev attribute) of three
        related nodes.

        Returns
        -------
        any
            The data of the removed node, or None if the list is empty.
        None 
            If the linked list is empty.
        """
        if self.dummyHead.next == self.dummyTail:
            return None
        
        # if there are some nodes in between
        # fix the neighbor's behavior
        curr = self.dummyTail.prev
        self.dummyTail.prev = curr.prev
        curr.prev.next = self.dummyTail

        # size -= 1
        self.size -= 1

        return curr.data

    def addAtIndex(self, index: int, data: int) -> bool:
        """
        Add a node with the given data at the specified index in the linked list.
        You could assume the only illegal input is an out of range index. 
        Notice, you need to reset the connection at both side. 

        Parameters
        ----------
        index : int
            The index at which the new node should be inserted.
        data : any
            The data to be stored in the new node.

        Returns
        -------
        bool
            True if the addition was successful, False otherwise.
        """
        # if the index is out of range
        if index < 0 or index > self.size:
            return False
        
        # create new node and iterate through the linked list while counting
        # starting from the dummy head's next node
        new_node = Node(data)
        curr = self.dummyHead.next
        for i in range(index):
            curr = curr.next

        # now current node becomes the node i would like to add
        # new node's next node would be current node
        # new node's previous node would be current node's previous node
        new_node.next = curr
        new_node.prev = curr.prev

        # then define the neighbors behavior
        curr.prev.next = new_node
        curr.prev = new_node

        # size += 1
        self.size += 1

        return True

    def deleteAtIndex(self, index: int) -> bool:
        """
        Delete a node with the given data at the specified index in the linked list.
        You could assume the only illegal input is an out of range index. 
        Notice, you need to reset the connection at both side. 

        Parameters
        ----------
        index : int
            The index at which the new node should be inserted.

        Returns
        -------
        bool
            True if the addition was successful, False otherwise.
        """
        # if the index is out of range
        if index < 0 or index >= self.size:
            return False

        # starting node would be dummy head's next node
        # iterate through linked list
        curr = self.dummyHead.next
        for i in range(index):
            curr = curr.next

        # now current node become the node that needs to be removed
        # change its neighbors behavior
        previous = curr.prev
        next = curr.next
        previous.next = next
        next.prev = previous

        # remove the neighbors of current node (which has been removed)
        curr.next = curr.prev = None

        # size -= 1
        self.size -= 1

        return True

    def printFromFront(self) -> None:
        """
        Print all elements of the linked list from front to back,
        each element should be in a separate line. 
        If the linked list is empty, print exactly this string "Link list is empty."
        You should not include the value of dummy head or tail.

        Expected Output:
        firstElement  
        secondElement 
        ...
        """
        if self.size == 0:
            print('Link list is empty.')
            return
        
        curr = self.dummyHead.next

        while curr != self.dummyTail:
            print(curr.data)
            curr = curr.next

    def printFromBack(self) -> None:
        """
        Prints all elements of the linked list from back to front.
        If the linked list is empty, print exactly this string "Link list is empty."
        Follow the same format of printFromFront()
        """
        if self.size == 0:
            print('Link list is empty.')
            return

        curr = self.dummyTail.prev

        while curr != self.dummyHead:
            print(curr.data)
            curr = curr.prev

    def _isNodeUnbound(self,node) -> bool:
        """
        A private method. 
        Check if the given node's linkage in the list is broken.
        This means the node does not appear in the traversal from head to tail.
        In the other words, check if the connection relation between the node 
        and the node before it is neutral. 
        Notice this method assumes all the methods related to delete a node are 
        implemented correctly. 

        Parameters
        ----------
        node : Node
            The node to check for broken linkage.

        Returns
        -------
        bool
            True if the node's linkage is broken, False otherwise.

        Example
        --------
        check if the next attribute of the node's previous node is 
        the node.
        """
        # basic check
        if node is None or node is self.dummyHead or node is self.dummyTail:
            return True

        # check previous node and assume it is unbounded
        previous_check_ok = False
        if node.prev is not None and node.prev.next == node:
            previous_check_ok = True
        
        # check next node and assume it is unbounded
        next_check_ok = False
        if node.next is not None and node.next.prev == node:
            next_check_ok = True

        return not (previous_check_ok and next_check_ok)
    
    def getFront(self) -> Any | None:
        """
        Returns the data from the first non dummy node in the linked list.

        Returns
        -------
        data or None
            The data of the first node in the list, or None if the list is empty.
        """
        if self.dummyHead.next == self.dummyTail:
            return None
        return self.dummyHead.next.data

    def getBack(self) -> Any | None:
        """
        Returns the data from the last non dummy node in the linked list.

        Returns
        -------
        data or None
            The data of the last node in the list, or None if the list is empty.
        """
        if self.dummyTail.prev == self.dummyHead:
            return None
        return self.dummyTail.prev.data
    
    def getSize(self) -> int:
        """
        Return the number of elements in the stack or queue.

        This method provides the current size of the linked list, 
        indicating how many elements are stored in it.

        Returns
        -------
        int
            The number of elements in linked list.
        """
        return self.size
        
"""
############################## Homework linked_list ##############################

% Student Name: Sammi Wang

% Student Unique Name: dsammi

% Lab Section 00X: 003

% I worked with the following classmates: None

%%% Please fill in the first 4 lines of this file with the appropriate information.
"""

if __name__ == "__main__":
    test = LinkedList()
    test.addAtIndex(0, 0)
    test.addAtIndex(1, 1)
    print(test.getSize())
    test.printFromFront()
    test.printFromBack()