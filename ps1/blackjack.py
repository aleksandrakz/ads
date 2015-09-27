
import random
import numpy as np
import os, re, subprocess, shlex, time

# load card sprite - 936x384 - source: jfitz.com
CARD_SIZE = (72, 96)
CARD_CENTER = (36, 48)

CARD_BACK_SIZE = (72, 96)
CARD_BACK_CENTER = (36, 48)

# initialize some useful global variables
score = 0
global stats

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}


# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank
    def __str__(self):
        return self.suit + self.rank
    def get_suit(self):
        return self.suit
    def get_rank(self):
        return self.rank
    
# define hand class
       
class Hand:
    def __init__(self):
        self.cards = []

    def __str__(self):
        #ans = "Hand contains "
        for i in range(len(self.cards)):
            ans += str(self.cards[i]) + " "
        return ans
        # return a string representation of a hand

    def add_card(self, card):
        self.cards.append(card)
        # add a card object to a hand

    def get_value(self):
        value = 0
        aces = False
        for c in self.cards:
            rank = c.get_rank()
            v = VALUES[rank]
            if rank == 'A': aces = True
            value += v
        if aces and value < 12: value += 10
        return value
        # count aces as 1, if the hand has an ace, then add 10 to hand value if it doesn't bust
        # compute the value of the hand, see Blackjack video
   
    def draw(self, canvas, pos):
        # draw a hand on the canvas, use the draw method for cards
        for c in self.cards:
            pos[0] += 100  ## shift to the right for next card
 
# define deck class 
class Deck:
    def __init__(self):
        self.deck = []
        for s in SUITS:
            for r in RANKS:
                self.deck.append(Card(s, r))
        # create a Deck object

    def shuffle(self):
        random.shuffle(self.deck)
        # shuffle the deck 

    def deal_card(self):
        return self.deck.pop()
        # deal a card object from the deck
    
    def __str__(self):
        ans = "The deck: "
        for c in self.deck:
            ans += str(c) + " "
        return ans
        # return a string representing the deck


#start a new game by dealing cards and then play until turn() returns false 
def deal(method = "sim"):
        global outcome, in_play, theDeck, playerhand, househand, score
        theDeck = Deck()
        theDeck.shuffle()
        playerhand = Hand()
        househand = Hand()
        playerhand.add_card(theDeck.deal_card())
        playerhand.add_card(theDeck.deal_card())
        househand.add_card(theDeck.deal_card())
        next=True
        while (next == True):
            next= turn(method)

#plays one turn by choosing whether or not the player hits
#if turn is called with method="sim", the choice to hit or stand is made randomly
#otherwise, turn() calls the hitme() function with the hand values to determine this
#if the player stands or hits and loses, turn returns False, to signify the game is 
#over. Otherwise it returns True      
def turn(method ="sim"):
    val = playerhand.get_value()
    if method == "sim":
        choice = random.choice(["hit", "stand"]) #raw_input( "Hit or Stand? ")
        if choice == "hit":
            return hit(val, househand.get_value())
        elif choice == "stand":
             stand(val, househand.get_value())
             return False
    else:
        choice = hitme(val, househand.get_value())
        if choice == True:
             return hit(val, househand.get_value())
        elif choice == False:
             stand(val, househand.get_value())
             return False


#hit() draws another card for the player. If they are over 21, they lose and hit 
#returns false. Otherwise, it returns True. hit() also updates the matrix to say
#whether the player lived or died on this round.
def hit(pHand, hHand):
        global score, stats
        playerhand.add_card(theDeck.deal_card())
        val = playerhand.get_value()
        
        if val > 21: 
            stats[pHand][hHand][3] +=1 
            return False
        else:
            stats[pHand][hHand][2] +=1 
            stats[pHand][hHand][3] +=1 
            return True
           
#stand compares the points of the player and dealer and tells who won
#it updates the matrix to say if the player won or lost after standing 
#it also updates the score if the player won      
def stand(pHand, hHand):
    global score, stats
    if playerhand.get_value() > 21:
        return None
    val = househand.get_value()
    while(val < 17):
        househand.add_card(theDeck.deal_card())
        val = househand.get_value()  
    if (val > 21):
        if pHand > 21:
            stats[pHand][hHand][1] +=1 
        else: 
            score += 1
            stats[pHand][hHand][0] +=1 
            stats[pHand][hHand][1] +=1 
    else:
        if (val == playerhand.get_value()):
            stats[pHand][hHand][1] +=1 
        elif (val > playerhand.get_value()):
            stats[pHand][hHand][1] +=1 
        else:
            score += 1
            stats[pHand][hHand][0] +=1 
            stats[pHand][hHand][1] +=1 
    
#sim plays trials number of games in sim mode, meaning that it the decision about whether
#to hit or stand will be made randomly
#it also generates and saves the transcript file
def sim(trials):
    global stats, score
    score =0
    try: 
        stats = np.load('transcript')
    except: 
         stats = [[[0, 0, 0, 0] for x in range(12)] for x in range(22)] 
    for i in range(0,trials):
        deal()
    np.save('transcript', stats)

    with open("transcript", "w") as transcript:
        for playerhand in range (21):
            for dealerfacecard in range (11):
                result = ' '.join(map(str, stats[playerhand][dealerfacecard]))
                transcript.write(result)
                transcript.write('\n')
                #stats.write(stats[playerhand][dealerfacecard][1], stats[playerhand][dealerfacecard][2], stats[playerhand][dealerfacecard][3], stats[playerhand][dealerfacecard][4])

   
#hitme takes the player and dealer hands and decides whether or not the player should hit
#this is determined by seeing whether the probability of winning if you stand is higher
#than the probability of living (staying under 21) if you hit
def hitme(playerhand, dealerfacecard):
    global stats, score
    try: 
        stats[playerhand][dealerfacecard]
    except:
        stats = np.load('transcript.npy')
    if stats[playerhand][dealerfacecard][1]==0 or stats[playerhand][dealerfacecard][3]==0:
        return True
    ratiowin = float(stats[playerhand][dealerfacecard][0])/ float(stats[playerhand][dealerfacecard][1])
    ratiolive = float(stats[playerhand][dealerfacecard][2])/ float(stats[playerhand][dealerfacecard][3])

    if ratiowin > (ratiolive):
        return False
    else:
        return True

#play plays trials number of games in play mode, meaning that the the decision to stand
#or hit will be made by the hitme() function
def play(trials):
    global stats, score
    score =0
    stats = np.load('transcript.npy')
    for i in range(0,trials):
        deal(method="play")
    print float(score)/float(trials)*100

def main():
    trials = 100
    sim(trials)
    play(trials)

if __name__ == "__main__":
   main()

