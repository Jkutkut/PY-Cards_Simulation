import random
from Classes.card import Card, PokerCard, SpanishCard

class Deck:
    def __init__(self, cardType) -> None:
        if not issubclass(cardType, Card):
            raise Exception("The cardType must be a Card class.")
        if cardType.__class__ == Card:
            raise Exception("The cardType must not be the prototype, rather a children class of it.")
        
        self._cT = cardType
        self._stack = []
        self.restartStack()
        
    
    # ########## GETTERS ##########

    def getStack(self) -> list:
        '''Returns a list with the current cards avalible on the stack.'''
        return self._stack

    def getCardClass(self):
        '''Class choosen for the deck'''
        return self._cT

    def getSuits(self) -> iter:
        '''Iterator with all the suits indices valid for the card type choosen'''
        return range(len(self.getCardClass().SUIT))
    
    def getRanks(self) -> iter:
        '''Iterator with all the rank indices valid for the card type choosen'''
        return range(self.getCardClass().RANK["MIN"], self.getCardClass().RANK["MAX"] + 1)

    def __str__(self) -> str:
        s = []
        indexing = "  "
        delimeter = ",\n"
        for c in self.getStack():
            s.append(f"{indexing}{c.__str__()}")
        return f"[\n{delimeter.join(s)}\n]"
        
    
    # ########## SETTERS ##########

    def takeCard(self):
        '''Removes and returns a card from the stack. If empty, None is returned.'''
        if len(self.getStack() == 0):
            return None
        return self.getStack().pop()


    def restartStack(self):
        '''Generates a new ordered stack of cards.'''
        self._stack = []
        for s in self.getSuits():
            for r in self.getRanks():
                self.getStack().append(self.getCardClass()(r, s))
    
    def restartShuffleStack(self):
        '''Generates a new random stack of cards.'''
        self.restartStack()
        self.shuffle()
    
    def shuffleStack(self):
        '''Shuffles the current stack of cards'''
        random.shuffle(self.getStack())
