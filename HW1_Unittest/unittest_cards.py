import unittest                                     # for unittesting
import cards                                        # the py file
from typing import Type                             # python type hint

class TestCard(unittest.TestCase):
    
    '''
        suit_names: list
        the four suit names in order 
        0:Diamonds, 1:Clubs, 2: Hearts, 3: Spades
    '''

    def test_construct_Card(self) -> None:
        c1 = cards.Card(0, 2)                       # 2 of Diamonds
        c2 = cards.Card(1, 1)                       # Ace of Clubs

        # check whether c1 suit is equal to 0
        self.assertEqual(c1.suit, 0)            
        # check whether the sult name is equal to Diamonds    
        self.assertEqual(c1.suit_name, "Diamonds")
        # check whether c1 rank is equal to 2
        self.assertEqual(c1.rank, 2)
        # check whether c1 rank name is equal to 2
        self.assertEqual(c1.rank_name, "2")

        # check return data type
        self.assertIsInstance(c1.suit, int)
        self.assertIsInstance(c1.suit_name, str)
        self.assertIsInstance(c1.rank, int)
        self.assertIsInstance(c1.rank_name, str)

        # check whether c2 suit is equal to 1
        self.assertEqual(c2.suit, 1)
        # check whether the suit name is equal to clubs
        self.assertEqual(c2.suit_name, "Clubs")
        # check whether c2 rank is equal to 1
        self.assertEqual(c2.rank, 1)
        # check whether c2 rank name is equal to Ace
        self.assertEqual(c2.rank_name, "Ace")
        
    def test_q1(self) -> tuple[str, str]:
        '''
        1. fill in your test method for question 1:
        Test that if you create a card with rank 12, its rank_name will be "Queen"
        
        2. remove the pass command
        
        3. uncomment the return command and 
        3b. change X, Y to the values from your assert statement
            ### please note: normally unit test methods do not have return statements. 
            But returning will allow for unit testing of your unit test, 
            and allow you to check your answer with the autograder.  This is optional today.
        '''
        card = cards.Card(0, 12)
        self.assertEqual(card.rank_name, 'Queen')
        return(card.rank_name, 'Queen')
    
    def test_q2(self) -> tuple[str, str]:
        '''
        1. fill in your test method for question 1:
        Test that if you create a card instance with suit 1, 
        its suit_name will be "Clubs"
        
        2. remove the pass command
        
        3. uncomment the return command and 
        3b. change X, Y to the values from your assert statement
        ### please note: normally unit test methods do not 
            have return statements. But returning will allow 
            for unit testing of your unit test, and allow you 
            to check your answer with the autograder.  
            This is optional today.
        '''
        card = cards.Card(1, 12)
        self.assertEqual(card.suit_name, 'Clubs')
        return(card.suit_name, 'Clubs')

    def test_q3(self) -> tuple[str, str]:
        '''
        1. fill in your test method for question 3:
        Test that if you invoke the __str__ method of a card instance 
        that is created with suit=3, rank=13, it returns the string 
        "King of Spades"

        
        2. remove the pass command
        
        3. uncomment the return command and 
        3b. change X, Y to the values from your assert statement
        ### please note: normally unit test methods do not have 
            return statements. But returning will allow for unit 
            testing of your unit test, and allow you to check your 
            answer with the autograder.  This is optional today.
        '''
        card = cards.Card(3, 13)
        self.assertEqual(card.__str__(), 'King of Spades')
        return(card.__str__(), 'King of Spades')
    
    def test_q4(self) -> tuple[int, int]:
        '''
        1. fill in your test method for question 4:
        Test that if you create a eck instance, it will have 52 cards 
        in its cards instance variable
        
        2. remove the pass command
        
        3. uncomment the return command and 
        3b. change X, Y to the values from your assert statement
        ### please note: normally unit test methods do not have 
            return statements. But returning will allow for unit 
            testing of your unit test, and allow you to check your 
            answer with the autograder.  This is optional today.
        '''
        deck = cards.Deck()
        self.assertEqual(len(deck.cards), 52)
        return(len(deck.cards), 52)

    def test_q5(self) -> tuple[cards.Card, Type[cards.Card]]:
        '''
        1. fill in your test method for question 5:
        Test that if you invoke the deal_card method on a deck, 
        it will return a card instance.
        
        2. remove the pass command
        
        3. uncomment the return command and 
        3b. change X, Y to the values from your assert statement
        ### please note: normally unit test methods do not have return statements. But returning will allow for unit testing of your unit test, and allow you to check your answer with the autograder.  This is optional today.

        '''
        deck = cards.Deck()
        top_card = deck.deal_card()
        self.assertIsInstance(top_card, cards.Card)
        return(top_card, cards.Card)
    
    def test_q6(self) -> tuple[int, int]:
        '''
        1. fill in your test method for question 6:
        
        Test that if you invoke the deal_card method on a deck, 
        the deck has one fewer cards in it afterwards.
        
        2. remove the pass command
        
        3. uncomment the return command and 
        3b. change X, Y to the values from your assert statement
        ### please note: normally unit test methods do not have return 
            statements. But returning will allow for unit testing of your 
            unit test, and allow you to check your answer with the autograder.  
            This is optional today.
        '''
        deck = cards.Deck()                     # instanciate a Deck class
        original_num = len(deck.cards)
        deck.deal_card()                        # deal one card on top
        after_num = len(deck.cards)
        self.assertEqual(after_num, original_num - 1)
        return(after_num, original_num - 1)

    def test_q7(self) -> tuple[int, int]:
        '''
        1. fill in your test method for question 7:
        Test that if you invoke the replace_card method, 
        the deck has one more card in it afterwards. 
        (Please note that you want to use deal_card function 
        first to remove a card from the deck and then add the 
        same card back in)

        
        2. remove the pass command
        
        3. uncomment the return command and 
        3b. change X, Y to the values from your assert statement
        ### please note: normally unit test methods do not have 
        # return statements. But returning will allow for unit 
        # testing of your unit test, and allow you to check your 
        # answer with the autograder.  This is optional today.
        '''
        deck = cards.Deck()
        top_card = deck.deal_card()
        original_num = len(deck.cards)          
        deck.replace_card(top_card)             # to the top card back
        after_num = len(deck.cards)
        self.assertEqual(after_num, original_num + 1)
        return(after_num, original_num + 1)
    
    def test_q8(self) -> tuple[int, int]:
        '''
        1. fill in your test method for question 8:
        Test that if you invoke the replace_card method 
        with a card that is already in the deck, the deck 
        size is not affected.(The function must silently 
        ignore it if you try to add a card that’s already in the deck)

        
        2. remove the pass command
        
        3. uncomment the return command and 
        3b. change X, Y to the values from your assert statement
        ### please note: normally unit test methods do not have 
        # return statements. But returning will allow for unit 
        # testing of your unit test, and allow you to check your 
        # answer with the autograder.  This is optional today.
        '''
        deck = cards.Deck()
        top_card = deck.deal_card()
        deck.replace_card(top_card)             # put the top card back
        original_num = len(deck.cards)
        deck.replace_card(top_card)             # put the same card again
        after_num = len(deck.cards)
        self.assertEqual(after_num, original_num)
        return(after_num, original_num)

if __name__=="__main__":
    unittest.main()