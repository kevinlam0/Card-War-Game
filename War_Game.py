from random import shuffle

# -- Arrays of suits and ranks to generate cards for the Deck --
SUIT = 'H D S C'.split()
RANKS = '2 3 4 5 6 7 8 9 10 J Q K A'.split()

# -- Making each card of every suit -- 
# mycards = []
# for r in RANKS:
#     for s in SUITE:
#         mycards.append((s,r))


class Deck:
    """
    This class is the entire deck before distributed to the two players
    Has attribute of allcards which is a list of cards (tuples of suit and rank)
    Has methods for splitting the cards in half and shuffling the cards in the Deck 
    """
    def __init__(self):
        # For each each suit and for each rank, pair them up as a tuple to imitate a card
        # allcards is a list of all the cards 
        self.allcards = [(s,r) for s in SUIT for r in RANKS]
        
    # -- Splitting the deck in half at index 0-25 and 26-52 -- 
    def split_in_half(self):
        return (self.allcards[0:26], self.allcards[26:])

    # -- From Random library to shuffle the cards in the deck --
    def shuffle(self):
        shuffle(self.allcards)


class Hand:
    '''
    This is the Hand class that each player has containing cards 
    Has attribute of cards 
    Each player has a Hand that they can add or remove cards from 
    '''
    def __init__(self, cards):
        self.cards = cards

    #  -- Returns the amount of cards in the Hand --
    def __str__(self) -> str:
        return "Contains {} cards".format(len(self.cards))
    
    # -- Adding to the hand by extending the list with another list of cards from the table for that round 
    def add(self, card):
        self.cards.extend(card)
    
    # -- Remove the top card and returning what it is -- 
    def remove_card(self):
        return self.cards.pop()

class Player:
    """
    This is the Player class, which has attributes of a name and a hand
    Has methods of playing a card by using Hand's remove method, removing the correct amount of cards when there is war, and check to see if Player still has cards in their hand
    """
    def __init__(self, name, hand) -> None:
        self.name = name
        self.hand = hand 

    # -- Play the card and returning what the card is -- 
    def play_card(self):
        drawn_card = self.hand.remove_card()
        return drawn_card
    
    # -- Removes 2 cards that will stay faced down when there is war -- 
    def remove_war_cards(self):
        war_cards = []
        for i in range(2):
            war_cards.append(self.hand.remove_card())
        return war_cards
    
    # -- Returns boolean of still having cards or not -- 
    def still_has_cards(self):
        if len(self.hand.cards) > 0:
            return True
        return False
    


######################
#### GAME PLAY #######
######################
print("Welcome to War, let's begin...")


# -- Create a new deck and split it in half after being shuffled -- 
game_deck = Deck()
game_deck.shuffle()
half1, half2 = game_deck.split_in_half()


# -- Create 2 players --
name_of_player = input("What is your name? ")
user = Player(name_of_player, Hand(half1))
comp = Player("Computer", Hand(half2))

total_rounds = 0
war_count = 0

# -- Game Logic -- 
while user.still_has_cards() and comp.still_has_cards():
    total_rounds += 1
    shuffle(user.hand.cards)
    shuffle(comp.hand.cards)

    # -- Printing portion -- 
    print("This is round {}".format(total_rounds)) 
    print(user.name + " has " + str(len(user.hand.cards)) + " cards")
    print(comp.name + " has " + str(len(comp.hand.cards)) + " cards")
    print('\n')

    # -- The players play their top card 
    pcard = user.play_card()
    print(pcard)
    ccard = comp.play_card()
    print(ccard)

    # -- The cards on the table that player will take if they win the round -- 
    table_stack = [pcard, ccard]
    

    # -- If the card played is the same ranking, there is war if and only if both players have enough cards for war -- 
    if pcard[1] == ccard[1] and len(user.hand.cards) >= 3 and len(comp.hand.cards) >= 3:
        war_count += 1
        print("There is war")

        # Add two cards from each hand to the table stack 
        table_stack.extend(user.remove_war_cards())
        table_stack.extend(comp.remove_war_cards())

        # Card that will be compared during war 
        cwar_cards = comp.play_card()
        pwar_cards = user.play_card()

        # Add those cards to the table stack 
        table_stack.append(cwar_cards)
        table_stack.append(pwar_cards)

        # -- If index of the player's card's rank is higher, the player wins and takes the cards on the table. --
        # Refer to the RANKS list to see the rankings
        if RANKS.index(pwar_cards[1]) > RANKS.index(cwar_cards[1]):
            user.hand.add(table_stack)
        
        # If the computer's cards have a higher rank or if they both have the same rank, the computer wins
        else:
            comp.hand.add(table_stack)
    
    # -- If player has higher ranking, player wins the round -- 
    elif RANKS.index(pcard[1]) > RANKS.index(ccard[1]):
        print(user.name +" wins")
        user.hand.add(table_stack)
    
    # -- Computer wins the round -- 
    else:
        print("Computer wins")
        comp.hand.add(table_stack)

# -- After the game stops, whoever has cards left wins -- 
print('\n')
print("The game took " + str(total_rounds) + " rounds!")
print("There were " + str(war_count) + " wars that happened!")
if user.still_has_cards():
    print("Congratulations! " +user.name + " won")
else:
    print("Sorry buddy, the " +comp.name + " won. " + user.name + ", you are a loser.")

print('\n')




