# from media.py import 3 classes
from media import Media, Track, Movie
# from linked_list.py import LinkedList (double linked list)
from linked_list import LinkedList
# handle json file
import json

class Player:
    """
    A media player class that manages a playlist of media.

    This class utilizes a doubly linked list (LinkedList) to store and manage media in a playlist.
    It provides methods for adding, removing, playing, and navigating through media.

    Attributes
    ----------
    playlist : LinkedList
        A doubly linked list that stores the media in the playlist.
    currentMediaNode : Node or None
        The current media being played, represented as a node in the linked list.
    """

    def __init__(self) -> None:
        """
        Initializes the Player with an empty playlist and None as currentMediaNode.
        """
        self.playlist = LinkedList()
        self.currentMediaNode = None

    def addMedia(self, media) -> None:
        """
        Adds a media to the end of the playlist.
        Set the currentMediaNode to the first node in the playlist, 
        if currentMediaNode is None. 

        Parameters
        ----------
        media : Media | Track | Movie 
            The media to add to the playlist.
        """
        # use LinkedList.append() method to append the media object to the right side of the linked list
        self.playlist.append(media)

        # move the current media node to the first node if the node is None
        if self.currentMediaNode is None:
            self.currentMediaNode = self.playlist.dummyHead.next

    def removeMedia(self, index) -> bool:
        """
        Removes a media from the playlist based on its index.
        You can assume the only invalid input is invalid index.
        Set the currentMediaNode to its next, if currentMediaNode is removed,
        and remeber using _isNodeUnbound(self.currentMediaNode) to check if a link is broken.

        Parameters
        ----------
        index : int
            The index of the media to remove.

        Returns
        -------
        bool
            True if the media was successfully removed, False otherwise.
        """
        # first check the input argument index is out of bound or not
        if index < 0 or index >= self.playlist.getSize() or self.playlist.getSize() == 0:
            return False
        
        # get the current node
        curr = self.playlist.dummyHead.next
        for i in range(index):
            curr = curr.next

        # remove the media at that index
        # deleteAtIndex return bool: true is scucessfully delete the element
        # false is not successful
        if not self.playlist.deleteAtIndex(index):
            return False

        # if the current pointing node is unbounded, move to its next node
        # first move to right side first, then left side
        if self.currentMediaNode == curr or self.playlist._isNodeUnbound(self.currentMediaNode):
            # move to right side node if it is not tail
            if curr.next != self.playlist.dummyTail:
                self.currentMediaNode = curr.next
            # move to left side node if it is not head
            else:
                if curr.prev != self.playlist.dummyHead:
                    self.currentMediaNode = curr.prev
                else:
                    # playlist become empty
                    self.currentMediaNode = None
        
        return True

    def next(self) -> bool:
        """
        Moves currentMediaNode to the next media in the playlist.
        This method should not make self.currentMediaNode be self.playlist.dummyNode.

        Returns
        -------
        bool
            True if the player successfully moved to the next media, False otherwise.
        """
        # cuz self.currentMediaNode is a node object, it has .next and .prev
        # if the next node (at right side) is a dummy tail, return false
        if self.currentMediaNode.next == self.playlist.dummyTail:
            return False
        
        self.currentMediaNode = self.currentMediaNode.next

        return True

    def prev(self) -> bool:
        """
        Moves currentMediaNode to the previous media in the playlist.
        This method should not make self.currentMediaNode be self.playlist.dummyNode.

        Returns
        -------
        bool
            True if the player successfully moved to the previous media, False otherwise.
        """
        if self.currentMediaNode.prev == self.playlist.dummyHead:
            return False
        
        self.currentMediaNode = self.currentMediaNode.prev

        return True

    def resetCurrentMediaNode(self) -> bool:
        """
        Resets the current media to the first media in the playlist,
        if the playlist contains at least one media. 

        Returns
        -------
        bool
            True if the current media was successfully reset, False otherwise.
        """
        # check if the playlist size is less than 1, meaning no media in it
        if self.playlist.getSize() < 1:
            return False

        # reset the current Media Node to the first node, which is next to dummy head
        self.currentMediaNode = self.playlist.dummyHead.next
        
        return True

    def play(self) -> None:
        """
        Plays the current media in the playlist. 
        Call the play method of the media instance.
        Remeber currentMediaNode is a node not a media, but its data is the actual
        media. If the currentMediaNode is None or its data is None, 
        print "The current media is empty.". 
        """
        # if the current pointing node is None or the data inside the node is None
        # print out the warning message
        if self.currentMediaNode is None or self.currentMediaNode.data is None:
            print('The current media is empty.')
            return
        
        # if it is not None, use .data to get to the Media object and use its play() method
        self.currentMediaNode.data.play()
        
    def playForward(self) -> None:
        """
        Plays all the media in the playlist from front to the end,
        by iterating the linked list.  
        Remeber each media information should take one line. (follow the same
        format in linked list)
        If the playlist is empty, print "Playlist is empty.". 
        """
        # if the playlist is empty, print the error message
        if self.playlist.getSize() < 1:
            print('Playlist is empty.')
            return

        # play all the media in the playlist by using the node.data.play()
        # moving forward
        # lets say size = 3, meaning the last media's index = 2
        # thus we set the first node the dummy head
        curr = self.playlist.dummyHead
        while curr.next != self.playlist.dummyTail:
            curr = curr.next
            curr.data.play()
        
    def playBackward(self) -> None:
        """
        Plays all the media in the playlist from the back to front,
        by iterating the linked list.  
        Remeber each media information should take one line. (follow the same
        format in linked list)
        If the playlist is empty, print this string "Playlist is empty.". 
        """
        if self.playlist.getSize() < 1:
            print('Playlist is empty')
            return

        # play all the media in the playlist by using the node.data.play()
        # moving backward
        curr = self.playlist.dummyTail
        while curr.prev != self.playlist.dummyHead:
            curr = curr.prev
            curr.data.play()

    def loadFromJson(self, fileName) -> None:
        """
        Loads media from a JSON file and adds them to the playlist.
        The order should be the same as the provided json file. 
        You could assume the filename is always valid
        Notice, for each given json object, 
        you should create instance of the correct instance type, (movie,track,media).
        You need to observe the provided json and figure how to do it.
        You could assume if a json object is not track or movie,
        it has to be a media.
        Pay attention the name of the key in each json object. 
        Set the currentMediaNode to the first media in the playlist, 
        if there is at least one media in the playlist.
        Remeber to use the dictionary get method. 

        Parameters
        ----------
        filename : str
            The name of the JSON file to load media from.
        """
        # load the json file
        with open(fileName, 'r') as f:
            data = json.load(f)

        # loop through the json file and add it to the linked list using append() method
        for item in data:

            # if such dictionary represent a movie
            if item.get('wrapperType') == 'track' and item.get('kind') == 'feature-movie':
                movie = Movie(item.get('trackName'),                                    # movie title 
                              item.get('artistName'),                                   # movie artist
                              item.get('releaseDate'),                                  # movie release date
                              item.get('previewUrl'),                                   # movie url  
                              item.get('contentAdvisoryRating'),                        # movie rating
                              item.get('trackTimeMillis'))                              # movie duration
                self.playlist.append(movie)

            # if such dictionary represent track
            elif item.get('wrapperType') == 'track':
                track = Track(item.get('trackName'),                                    # track title 
                              item.get('artistName'),                                   # track artist 
                              item.get('releaseDate'),                                  # track release date
                              item.get('previewUrl') or item.get('trackViewUrl'),       # track url 
                              item.get('collectionName'),                               # track album 
                              item.get('genres') or item.get('primaryGenreName'),       # track genre
                              item.get('trackTimeMillis'))                              # track duration
                self.playlist.append(track)
            
            # others would be media
            else:
                media = Media(item.get('collectionName'),                               # media title
                              item.get('artistName'),                                   # media artist
                              item.get('releaseDate'),                                  # media release date
                              item.get('previewUrl'))                                   # media url
                self.playlist.append(media)

        # set current node to the first media if there is more than 1 node
        if self.playlist.getSize() >= 1:
            self.currentMediaNode = self.playlist.dummyHead.next

if __name__ == '__main__':
    player = Player()
    player.loadFromJson('base_data.json')
    player.playForward()