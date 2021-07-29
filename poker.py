from Classes.card.card import Card
import random
from Classes.colorOutput import *
from Classes.card.pokerCard import PokerCard
from Classes.playerHand import PlayerHand
from Classes.deck import Deck

class Poker:
    HANDS = {
        "Five of a kind":  100000000000,
        "Royal Flush":     10000000000,
        "Straight Flush":  1000000000,
        "Four of a kind":  100000000,
        "Full house":      10000000,
        "Flush":           1000000,
        "Straight":        100000,
        "Three of a kind": 10000,
        "Two pair":        1000,
        "Pair":            100,
        "High card":       0
    }

    def __init__(self) -> None:
        pass

    @classmethod
    def analyze(cls, hand) -> str:
        if not isinstance(hand, PlayerHand):
            raise Exception("The hand given is not valid")
        
        # Sort array using insertion sort
        sortedHand = hand.getHand().copy() # Clone the array
        for i in range(1, 5):
            val = sortedHand[i]
            j = i-1
            while j >=0 and val.compare(sortedHand[j]) > 0:
                    sortedHand[j+1] = sortedHand[j]
                    j -= 1
            sortedHand[j+1] = val
        
        # Take away the jokers
        jokers = 0
        ind = 0
        while sortedHand[ind].__getRankPoint__() == PokerCard.RANK["MAX"] + 1:
            if sortedHand[ind].getRank() == PokerCard.RANK["JOKER"]:
                jokers += 1
                sortedHand.pop(ind)
            else:
                ind += 1
        print(f"Checking\n{hand.__str__()} with {jokers} jokers")
        
        
        # Check the array for pairs
        i = 1; pairs = []
        while i < len(sortedHand): 
            if sortedHand[i - 1].getRank() == sortedHand[i].getRank(): # if pair found
                l = 2
                while i + 1 < len(sortedHand) and sortedHand[i].getRank() == sortedHand[i + 1].getRank():
                    l += 1; i += 1 # While the next is also the same rank, keep updating the amount
                pairs.append({"rank": sortedHand[i].__getRankPoint__(), "amount": l})
            i += 1


        hand = None # Type of hand at the moment (str)
        points = 0 # Total points
        extraP = 0 # Extra points

        if len(pairs) == 0 and jokers != 0: # If pair not found but jokers in hand
            # make a new pair with all the jokers
            pairs.append({"rank": sortedHand[0].__getRankPoint__(), "amount": 1})

        if len(pairs) == 1: # if pair or 3, 4 or 5 of a kind
            l = pairs[0]["amount"] + jokers
            extraP = pairs[0]["rank"]
            
            if l == 2:
                hand = "Pair"
            elif l == 3:
                hand = "Three of a kind"
            elif l == 4:
                hand = "Four of a kind"
            elif l == 5:
                hand = "Five of a kind"

            points = Poker.HANDS[hand]
            
        elif len(pairs) == 2: # 2 pair or full house
            extraP = pairs[0]["rank"] + pairs[1]["rank"]

            if pairs[0]["amount"] < pairs[1]["amount"]: # Full house inverted => invert array
                tmp = pairs[0]
                pairs[0] = pairs[1]
                pairs[1] = tmp
            
            if pairs[0]["amount"] + jokers == 2:
                hand = "Two pair"
            else:
                hand = "Full house"
            
            points = Poker.HANDS[hand]

        # ========== Check (royal, straight or --) flush, straight or high card ==========

        straight = False # 2 3 4 5 6 
        royal = False    # A K Q J 10
        flush = True    # Same suit

        print([i.__str__() for i in sortedHand])

        # Check if straight (and royal)
        # ind = 0
        # if sortedHand[0].getRank() == 1: # if first is Ace
        #     pass


        # if straight and False: # If straight, check if royal
        #     royal = True
        
        # Check if flush
        currentSuit = sortedHand[0].getSuit()
        for i in range(1, len(sortedHand)):
            if sortedHand[i].getSuit() != currentSuit:
                flush = False
                break
        
        if flush:
            if straight:
                if royal: # If royal flush
                    points = Poker.HANDS["Royal Flush"]
                else: # If straight flush
                    points = Poker.HANDS["Straight Flush"]
            else: # if flush
                points += Poker.HANDS["Flush"] # Added cause it can also have a pair
                print("Flush")
        
        if not any([royal, straight, flush]) and points == 0: # if high card
            points = sortedHand[0].__getRankPoint__()
        
        points += extraP

        print(f"Points: {points}")
        
        print("\n")
        return points