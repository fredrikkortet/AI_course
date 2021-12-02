# identify if there is one or more pairs in the hand
import random
prize=0#prize money
rank = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']
suit= ['s', 'h', 'd', 'c']
deck=[]# deck of cards
# winning hand player, (HandCategory index), (rank index)
winning_hand=['name',-1,-1]
# 2 example poker hands
CurrentHand1 = []#card to player 
CurrentHand2 = []#card to player 2
player1={'card':[],'money':0,'wins':0}#hold card and moneyto players
player2={'card':[],'money':0,'wins':0}
player={'player1':player1,'player2':player2}#diffrent players in one variable
playerpot=[0,0]#hold pot for each player
playerhand=[[],[]]#hold hands for each player
mem_pot=[]#memory for the bettings
mem_hands=[]#memory for the hands for each player
# make shuffled deck
def make_card_deck():
    for i in range(4):
        for j in range(13):
            deck.append(rank[j]+""+suit[i])
    random.shuffle(deck)
# Randomly generate two hands of n cards
def generate_2hands(nn_card=3):
    for i in range(nn_card):
        CurrentHand1.insert(0,deck.pop(0))
        CurrentHand2.insert(0,deck.pop(0))
    #set in the cards in player to the players
    player['player1']['card']=CurrentHand1#
    player['player2']['card']=CurrentHand2
# identify hand category using IF-THEN rule
def identifyHand(Hand_):
    for c1 in Hand_:
        for c2 in Hand_:
            for c3 in Hand_:
                if (c1[0]==c2[0]==c3[0]) and (c1[1]<c2[1]<c3[1]):
                    yield dict(name='three of a kind',rank=c1[0],suit1=c1[1],suit2=c2[1],suit3=c3[1])
                elif (c1[0] == c2[0] != c3[0] ) and (c1[1] < c2[1]):
                    yield dict(name='pair',rank=c1[0],suit1=c1[1],suit2=c2[1])
                elif (rank.index(c1[0])<rank.index(c2[0])<rank.index(c3[0])):
                    yield dict(name='highest card',rank=c3[0],suit1=c3[1],suit2='')
#bid for the prize 
def bidding(pot,player_):
    global prize
    if player_=='player1':
        playerpot[0]+=pot
    else:
        playerpot[1]+=pot
    prize += pot
# Print out the result
def analyseHand(Hand_,player_):
    HandCategory = ['highest card','pair','three of a kind']
    functionToUse = identifyHand
    for category in functionToUse(Hand_):
        if winning_hand[1] <HandCategory.index(category['name']):
            winning_hand[0]=player_
            winning_hand[1]=HandCategory.index(category['name'])
            winning_hand[2]=rank.index(category['rank'])
        elif winning_hand[1] == HandCategory.index(category['name']) and winning_hand[2] < rank.index(category['rank']):
            winning_hand[0]=player_
            winning_hand[1]=HandCategory.index(category['name'])
            winning_hand[2]=rank.index(category['rank'])
#take the winner and gice the prize and count the winner
def winner():
    global prize
    player[winning_hand[0]]['money']+=prize
    player[winning_hand[0]]['wins']+=1
    print('Winner:',winning_hand[0] ,'\n prize money:',prize)
#remember the pots and hands
def memory():
    mem_pot.extend(playerpot)
    mem_hands.extend(playerhand)
#random agent take random value
def rand(player_):
    pot=random.randint(0,50)
    bidding(pot,player_)
#fixed agent take same pot 
def fixed(player_):
    pot=10
    bidding(pot,player_)
#reflex agent look in own hand and decide what to do
def reflex(player_):
    for hand in identifyHand(player[player_]['card']):
        if hand['name']=='three of a kind':
            pot=50
        elif hand['name']=='pair':
            pot=30
        else:
            pot = 5
        bidding(pot,player_)

#########################
#      Game flow        #
#########################
for i in range(50):
    make_card_deck()
#########################
# phase 1: Card Dealing #
#########################
# 3 kort till var person
    generate_2hands()
    playerhand[0]=player['player1']['card']
    playerhand[1]=player['player2']['card']

    #print(playerhand)
#########################
# phase 2:   Bidding    #
#########################
# buda på korten du
# beroende på hur 
    #bid 3 times  
    for j in range(3):
        rand('player1')
        reflex('player2')
        #fixed('player2')
#########################
# phase 2:   Showdown   #
#########################
# vem vann med pris pengar
    #analyse hand to see the winner
    analyseHand(player['player1']['card'],'player1')
    analyseHand(player['player2']['card'],'player2')
    winner()
    memory()
    print('player 1 ',player['player1']['wins'],'player 2 ',player['player2']['wins'])
    print('player 2 bet:',playerpot[1])
    print('player 1 bet:',playerpot[0])
    print('player 1:',player['player1']['money'])
    print('player 2:',player['player2']['money'])
    #clean all the value.
    playerhand[0]=[]
    playerhand[1]=[]
    playerpot[0]=0
    playerpot[1]=0
    CurrentHand1=[]
    CurrentHand2=[]
    deck=[]
    prize=0
    winning_hand=['name',-1,-1]
