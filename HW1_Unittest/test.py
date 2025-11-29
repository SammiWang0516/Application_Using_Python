import cards

card1 = cards.Card(0, 1)
card2 = cards.Card(2, 3)

deck1 = cards.Deck()
print(deck1.deal_card())
print(deck1.deal_card())
deck1.shuffle()
print(deck1.deal_card())

hand_of_card = deck1.deal_hand(13)

cards.print_hand(hand_of_card)

print(card1)
print(card2)