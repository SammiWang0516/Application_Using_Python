# you may use pandas only for IO reason
# Using it to do sort will impact your grade
# import pandas as pd

import random

# a function that is able to do the same thing time.time() does, but it can input
# the function. 
# i will consider it as an advanced time modul
import timeit

# for parsing csv file
import csv

# with a method as an argument and wrapper that can take any functions
# this is a decorator factory.
# inside this function, it can not only run the input function but also
# time how long it take to run the function
def timeFunc(method):
    """
    Define the main body of the decorator that decorates a method.
        
    Returns
    -------
    Callable
        A wrapper that defines the behavior of the decorated method
    """
    def wrapper(*args, **kwargs):
        """
        Define the behavior of the decorated method
        Parameters:
            Same as the parameters used in the methods to be decorated
            
        Returns:
            Same as the objects returned by the methods to be decorated
        """
        # start the timer
        start = timeit.default_timer()

        # run the input function and store the return in result variable
        result = method(*args, **kwargs)  

        # record the time consumption of executing the method
        time = timeit.default_timer() - start
        
        # send metadata to standard output
        print(f"Method: {method.__name__}")
        print(f"Result: {result}")
        # instead of run the function 10,000 times, we simply run one time
        # and time the runtime with 10,000
        print(f"Elapsed time of 10000 times: {time*10000} seconds")

        return result

    return wrapper


class MusicLibrary:

    def __init__(self):
        """
        Initialize the MusicLibrary object with default values.
        self.data the collect of music library
        self.rows: the row number 
        self.cols: the col number 
        self.nameIndex: the number represent the index of name in each element of self.data
        self.albumIndex: the number represent the index of album in each element of self.data
        self.trackIndex: the number represent the index of track in each element of self.data
        """
        self.data = []
        self.rows = 0
        self.cols = 0
        self.nameIndex = 0
        self.albumIndex = 1
        self.trackIndex = 2

    def readFile(self, fileName):
        """
        Read music data from a CSV file and store it in the self.data attribute.
        The self.rows and self.cols should be updated accordingly. 
        The self.data should be [[name, albums count, tract count],...]
        You could assume the file is in the same directory with your code.
        Please research about the correct encoding for the given data set, 
        as it is not UTF-8.
        You are allowed to use pandas or csv reader, 
        but self.data should be in the described form above.

        Parameters
        ----------
        fileName : str
            The file name of the CSV file to be read.
        """
        # i used chardet module to detect the csv file and found that the
        # encoded type of the file is ISO-8859-1, also known as Latin-1
        with open(fileName, 'r', encoding = "latin-1") as file:
            reader = csv.reader(file)

            for line in reader:
                artist = line[0]
                no_album = int(line[1])
                no_track = int(line[2])

                self.data.append([artist, no_album, no_track])
        
        # modify self.rows and self.cols
        self.rows = len(self.data)
        self.cols = len(self.data[0])
        
    def printData(self):
        """
        Print the data attribute stored in the library instance in a formatted manner.
        """
        for row in self.data:
            print(row)
        print(len(self.data))

    def shuffleData(self):
        """
        Shuffle the data stored in the library.
        refer to the random package
        """
        # use the shuffle function in random module (in-place)
        random.shuffle(self.data)

    @timeFunc
    def binarySearch(self, key, keyIndex):
        """
        Perform a binary search on the data.

        Parameters
        ----------
        key : int or str
            The key to search for.
        keyIndex : int
            The column index to search in.

        Returns
        -------
        int
            The index of the row where the key is found, or -1 if not found.
        """

        # since now the dataset is either sorted by the artist name or shuffle
        # and now is not sorted, we have to sort it first in order to conduct
        # the binary search
        # but it depends on the keyIndex to know that which column should be the criteria
        # to sort (but it is sorted in the main function, let's skip the sort part)

        # conduct the binary search
        def binary_search(list, low, high, key):

            # base case: low is greater than high, meaning the key is not in the list
            if low > high:
                return -1

            # first find the mid of the list
            mid = (low + high) // 2
            
            # if else condition to check the key is lesser or greater
            if list[mid][keyIndex] == key:
                return mid
            elif list[mid][keyIndex] < key:
                return binary_search(list, mid+1, high, key)
            else:
                return binary_search(list, low, mid-1, key)
        
        return binary_search(self.data, 0, len(self.data)-1, key)
        

    @timeFunc
    def seqSearch(self, key, keyIndex):
        """
        Perform a sequential search on the data.

        Parameters
        ----------
        key : int or str
            The key to search for.
        keyIndex : int
            The column index to search in.

        Returns
        -------
        int
            The index of the row where the key is found, or -1 if not found.
        """

        # linear search does not require to be sorted
        rows = len(self.data)

        for row in range(rows):
            if self.data[row][keyIndex] == key:
                return row
        
        return -1

    @timeFunc
    def bubbleSort(self, keyIndex):
        """
        Sort the data using the bubble sort algorithm based on a specific column index.
        self.data will have to be in sorted order after calling this function.

        Parameters
        ----------
        keyIndex : int
            The column index to sort by.
        """
        # bubble sort: move the largest element to the last position and keep doing
        # this action till the 2 cursors are the same, meaning sorting is done

        left_cursor = 0
        right_cursor = 1
        right_most = len(self.data) - 1

        # right_most cannot less than or equal to 0, so that it can continue to compare values
        while right_most > 0:

            # compare each other and if right < left, swap
            # do nothing if not
            if self.data[right_cursor][keyIndex] < self.data[left_cursor][keyIndex]:
                self.data[left_cursor], self.data[right_cursor] = self.data[right_cursor], self.data[left_cursor]
            
            # move to next comparison
            left_cursor += 1
            right_cursor += 1

            # if the right_cursor exceed the right_most index, then go back to first element
            # and minus right_most by 1, meaning we sort 1 element already
            if right_cursor > right_most:
                left_cursor = 0
                right_cursor = 1
                right_most -= 1

    def merge(self, L, R, keyIndex):
        """
        Merge two sorted sublists into a single sorted list.
        This is the helper function for merge sort.
        You may change the name of this function or even not have it.
        

        Parameters
        ----------
        L, R : list
            The left and right sublists to merge.
        keyIndex : int
            The column index to sort by.

        Returns
        -------
        list
            The merged and sorted list.
        """
        # Implementation details...
        pass

    @timeFunc
    def mergeSort(self, keyIndex):
        """
        Sort the data using the merge sort algorithm.
        This is the main mergeSort function
        self.data will have to be in sorted order after calling this function.

        Parameters
        ----------
        keyIndex : int
            The column index to sort by.
        """
        # i prefer to write all the helper functions inside the sorting function
        # thus, i will write not only the splitting but merging functions inside this
        # list: input list
        def splitting(list):

            n = len(list)

            # base case: if list contains only 1 element left
            if n <= 1:
                return list

            # splitting left and right
            # recursively splitting the left half
            mid = n // 2
            left_list = splitting(list[:mid])
            right_list = splitting(list[mid:])

            # call merge helper function to merge (and do sorting as well)
            return merging(left_list, right_list)
        
        def merging(left_list, right_list):

            # left list cursor
            i = 0
            # right list cursor
            j = 0
            # temp list to store the merging new list
            temp = []

            while i < len(left_list) and j < len(right_list):
                if left_list[i][keyIndex] <= right_list[j][keyIndex]:
                    temp.append(left_list[i])
                    i += 1
                else:
                    temp.append(right_list[j])
                    j += 1
            
            # after above comparison, whichever the sublist left element extend
            # to the very last of the temp list
            temp.extend(left_list[i:])
            temp.extend(right_list[j:])

            return temp

        self.data = splitting(self.data)
            

    def _mergeSort(self, arr, keyIndex):

        # This is the helper function for merge sort.
        # You may change the name of this function or even not have it.
        # This is a helper method for mergeSort
        pass

    @timeFunc
    def quickSort(self, keyIndex):
        """
        Sort the data using the quick sort algorithm.
        This is the main quickSort function
        self.data will have to be in sorted order after calling this function.

        Parameters
        ----------
        keyIndex : int
            The column index to sort by.
        """

        # Implementation details...
        # helper function to keep recursively get the pivot index and call the
        # left side sublist and right side sublist
        def _quickSort(list, left, right):

            if left >= right:
                return

            # get the pivot index
            pivot_index = partition(list, left, right)
            # keep partitioning and swap elements in the left side
            _quickSort(list, left, pivot_index - 1)
            # keep partitioning and swap elements in the right side
            _quickSort(list, pivot_index + 1, right)

        def partition(list, left, right):

            # get the pivot value
            pivot = list[right][keyIndex]

            # make a cursor that represent the pivot index
            # since we have not traversed yet, make it left - 1, representing no
            # element is at its left side
            i = left - 1

            # make a cursor that traverse the list
            j = left

            while j != right:
                if list[j][keyIndex] <= pivot:
                    i += 1
                    list[i], list[j] = list[j], list[i]
                    j += 1
                else:
                    j += 1
            
            list[i+1], list[right] = list[right], list[i+1]
            return i + 1
        
        _quickSort(self.data, 0, len(self.data) - 1)

    def _quickSort(self, arr, keyIndex):
        # This is a helper method for quickSort
        # ...
        pass

    def comment(self):
        '''
        Based on the result you find about the run time of calling different function,
        Write a small paragraph (more than 50 words) about time complexity, and print it. 
        '''
        # print(you comment)
        print("binary search takes O(logn) while sequential search takes O(n). \
            Thus, binary search is much faster than linear search. As for the sorting, \
            bubble sort is the slowest because it takes O(n^2). As for merge sort, \
            it uses divide and conquer technique. Thus, the time complexity of merge \
            sort is O(nlogn). As for quick sort, it is O(nlogn) as well with the worst \
            case O(n^2) if we always pick the last element as pivot and that pivot \
            is always the biggest element in the list")


# create instance and call the following instance method
# using decroator to decroate each instance method
def main():
    random.seed(42)
    myLibrary = MusicLibrary()
    filePath = 'music.csv'
    myLibrary.readFile(filePath)

    idx = 0
    myLibrary.data.sort(key = lambda data: data[idx])
    myLibrary.seqSearch(key="Taylor Swift", keyIndex=idx)
    myLibrary.binarySearch(key="Taylor Swift", keyIndex=idx)

    idx = 2
    myLibrary.shuffleData()
    myLibrary.bubbleSort(keyIndex=idx)
    myLibrary.shuffleData()
    myLibrary.quickSort(keyIndex=idx)
    myLibrary.shuffleData()
    myLibrary.mergeSort(keyIndex=idx)
    myLibrary.printData()

if __name__ == "__main__":
    main()

