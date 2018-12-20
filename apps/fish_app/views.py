from django.shortcuts import render, HttpResponse, redirect
from  .cards import Card, Hand, Deck
from apps.login_app.models import User
from django.contrib import messages
import json
import random


class Player:
    def __init__(self, name ="", hand = [], books = []):
        self.name = name
        self.hand = hand
        self.books = books




def index(request):
    user = User.objects.get(id = request.session['user_id'])
    context = {
        
        'user':user,
    }
    return render(request,'fish_app/index.html', context)
###
def initialize(request):
    
    
    deck = []

    ranks = "A2345"
    suits = "cdhs"
    request.session['ranks'] = ranks

    # ranks = "A23456789TJQK"
    # suits = "cdhs"

    for rank in ranks:
        for suit in suits:
            deck.append([rank,suit])

    random.shuffle(deck)
    print(deck)
    request.session['deck'] = deck
    
    num_players = 2 #fixlater
    
    request.session['num_players'] = num_players
    
    players_to_cards = {
        2:7,
        3:6,
        4:5,
    }

    num_cards = players_to_cards[num_players]
    
    players = []
    print("cleared players", players)
    player_ids =  ["z","x"] #fixlater
    
    for player_index in range(num_players):
        name =  player_ids[player_index]
        
        p1 = Player(name)
        p1.hand = []
        players.append(p1)
        for card_num in range(num_cards):
            players[player_index].hand.append(deck.pop())
            
    print([player.__dict__ for player in players])

    random.shuffle(players)


    books = 0
    request.session['books']= books
    player_index = 0
    print("player index",player_index)
    request.session['player_index']= player_index

    players_json = json.dumps([player.__dict__ for player in players])
    request.session['players']= players_json
    request.session['turn_ask']= True
    request.session['turn_fish']= False
    request.session['num_cards'] = num_cards

    return redirect('/gofish/maingame')

def maingame(request):
    user = User.objects.get(id = request.session['user_id'])
    context = {
        
        'user':user,
    }
    
    return render(request,'fish_app/main_game.html', context)

def taketurn(request):
    print("*** POST *** \n",request.POST)
    print(request.POST['ask_player'])
    print(request.POST['ask_rank'])
    num_players = request.session['num_players']
    players = []
    players_from_session = json.loads(request.session['players'])
    print(players_from_session)
    for session_player in players_from_session:
        players.append(Player(session_player['name'],session_player['hand'],session_player['books']))
    print(players)
    ranks = request.session['ranks'] 
    player_index = request.session['player_index']
    books = request.session['books']
    deck = request.session['deck']
    num_cards = request.session['num_cards']



    
    print("************* start turn **********")
    print("player index",player_index, "player name: ", players[player_index].name)
    repeat_turn = False
    if len(players[player_index].hand)>0:
        players[player_index].hand.sort()
        print(players[player_index].hand)
        req_player = request.POST['ask_player']
        req_rank = request.POST['ask_rank']
        print(req_player, req_rank)
        for player in players:
            if player.name == req_player:
                # print("working on",player.name)
                taken_cards = []
                # print("num cards",len(player.hand))
                for card in player.hand:
                    
                    # print("rank",card[0])
                    if card[0] == req_rank:
                        # print("taking yo card")
                        taken_cards.append(card)
                    
                    
                for card in taken_cards:
                    player.hand.remove(card)
        print("you took",taken_cards)
        players[player_index].hand += taken_cards


        
        if taken_cards ==[]:
            print ("you must go fish")
            if len(deck)>0:
                draw = deck.pop()
                print("you drew",draw)
                if draw[0] == req_rank:
                    repeat_turn = True

                players[player_index].hand.append(draw)
            else:
                print("no cards available to draw")
        else: 
            repeat_turn = True
        players[player_index].hand.sort()
        print("hand now",players[player_index].hand)

        #check for books
        
        for player in players:
            rank_counts = {}
            for card in player.hand:
                if card[0] not in rank_counts.keys():
                    rank_counts[card[0]] = 1
                else:
                    rank_counts[card[0]] += 1
            print("player",player.name, "rank counts",rank_counts)
            for rank in rank_counts:
                if rank_counts[rank]==4:
                    player.books.append(rank)
                    books +=1
                    print("total books", books)


                    
                    print("player",player.name, "books ",player.books)

                    player.hand = [c for c in player.hand if c[0] != rank]
                    print("player",player.name, "hand after book ",player.hand)
        print("total books", books)
        

    else:
        num_draws = min(num_cards, len(deck))
        print("drawing from deck")
        for card_num in range(num_draws):
            players[player_index].hand.append(deck.pop())
        print("player index",player_index, "player name: ", players[player_index].name,"player hand: ", players[player_index].hand)
        if num_draws>0:
            repeat_turn = True
        else:
            repeat_turn = False


    print("deck",deck)
    print("repeat turn",repeat_turn)
    if not repeat_turn:
        player_index = (player_index +1) % num_players
    
    request.session['ranks'] = ranks
    request.session['deck'] = deck
    
    request.session['books']= books
    request.session['player_index']= player_index
    players_json = json.dumps([player.__dict__ for player in players])
    request.session['players']= players_json
    request.session['turn_ask']= True
    request.session['turn_fish']= False
    if request.session['books']<len(ranks):
        return redirect('/gofish/maingame')
    else:

        return redirect('/gofish/gameover')


def gameover(request):
    user = User.objects.get(id = request.session['user_id'])
    context = {
        
        'user':user,
    }
    
    return HttpResponse("game over")