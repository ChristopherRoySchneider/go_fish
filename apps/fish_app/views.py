from django.shortcuts import render, HttpResponse, redirect
from .cards import Card, Hand, Deck
from apps.login_app.models import User
from django.contrib import messages
import json
import random


class Player:
    def __init__(self, name="", hand=[], books=[]):
        self.name = name
        self.hand = hand
        self.books = books


card_image_map = {'Tc': 'fish_app/images/cards/10_clubs.png', 'Td': 'fish_app/images/cards/10_diamonds.png', 'Th': 'fish_app/images/cards/10_hearts.png', 'Ts': 'fish_app/images/cards/10_spades.png', '2c': 'fish_app/images/cards/2_clubs.png', '2d': 'fish_app/images/cards/2_diamonds.png', '2h': 'fish_app/images/cards/2_hearts.png', '2s': 'fish_app/images/cards/2_spades.png', '3c': 'fish_app/images/cards/3_clubs.png', '3d': 'fish_app/images/cards/3_diamonds.png', '3h': 'fish_app/images/cards/3_hearts.png', '3s': 'fish_app/images/cards/3_spades.png', '4c': 'fish_app/images/cards/4_clubs.png', '4d': 'fish_app/images/cards/4_diamonds.png', '4h': 'fish_app/images/cards/4_hearts.png', '4s': 'fish_app/images/cards/4_spades.png', '5c': 'fish_app/images/cards/5_clubs.png', '5d': 'fish_app/images/cards/5_diamonds.png', '5h': 'fish_app/images/cards/5_hearts.png', '5s': 'fish_app/images/cards/5_spades.png', '6c': 'fish_app/images/cards/6_clubs.png', '6d': 'fish_app/images/cards/6_diamonds.png', '6h': 'fish_app/images/cards/6_hearts.png', '6s': 'fish_app/images/cards/6_spades.png', '7c': 'fish_app/images/cards/7_clubs.png', '7d': 'fish_app/images/cards/7_diamonds.png', '7h': 'fish_app/images/cards/7_hearts.png',
                  '7s': 'fish_app/images/cards/7_spades.png', '8c': 'fish_app/images/cards/8_clubs.png', '8d': 'fish_app/images/cards/8_diamonds.png', '8h': 'fish_app/images/cards/8_hearts.png', '8s': 'fish_app/images/cards/8_spades.png', '9c': 'fish_app/images/cards/9_clubs.png', '9d': 'fish_app/images/cards/9_diamonds.png', '9h': 'fish_app/images/cards/9_hearts.png', '9s': 'fish_app/images/cards/9_spades.png', 'Ac': 'fish_app/images/cards/ace_clubs.png', 'Ad': 'fish_app/images/cards/ace_diamonds.png', 'Ah': 'fish_app/images/cards/ace_hearts.png', 'As': 'fish_app/images/cards/ace_spades.png', 'Jc': 'fish_app/images/cards/jack_clubs.png', 'Jd': 'fish_app/images/cards/jack_diamonds.png', 'Jh': 'fish_app/images/cards/jack_hearts.png', 'Js': 'fish_app/images/cards/jack_spades.png', 'Kc': 'fish_app/images/cards/king_clubs.png', 'Kd': 'fish_app/images/cards/king_diamonds.png', 'Kh': 'fish_app/images/cards/king_hearts.png', 'Ks': 'fish_app/images/cards/king_spades.png', 'Qc': 'fish_app/images/cards/queen_clubs.png', 'Qd': 'fish_app/images/cards/queen_diamonds.png', 'Qh': 'fish_app/images/cards/queen_hearts.png', 'Qs': 'fish_app/images/cards/queen_spades.png'}


def index(request):
    user = User.objects.get(id = request.session['user_id'])
    all_other_users = User.objects.exclude(id=user.id)
    context = {
        'user':user,
        'all_other_users': all_other_users
    }
    return render(request,'fish_app/index.html', context)
###


def initialize(request):

    deck = []
    print(request.POST)
    ranks = "A2345"
    # ranks = "A23456789TJQK"
    suits = "cdhs"
    request.session['ranks'] = ranks

    
    

    for rank in ranks:
        for suit in suits:
            deck.append([rank, suit])

    random.shuffle(deck)
    print(deck)
    request.session['deck'] = deck

    num_players = int(request.POST['num_players'])

    request.session['num_players'] = num_players

    players_to_cards = {
        2: 7,
        3: 6,
        4: 5,
    }

    num_cards = players_to_cards[num_players]

    players = []
    
    player_ids = []  
    if 'player_1' in request.POST.keys():
        player_ids.append(request.POST['player_1'])
    if 'player_2' in request.POST.keys():
        player_ids.append(request.POST['player_2'])
    if 'player_3' in request.POST.keys():
        player_ids.append(request.POST['player_3'])
    if 'player_4' in request.POST.keys():
        player_ids.append(request.POST['player_4'])


    for player_index in range(num_players):
        name = player_ids[player_index]

        p1 = Player(name)
        p1.hand = []
        players.append(p1)
        for card_num in range(num_cards):
            players[player_index].hand.append(deck.pop())
        players[player_index].hand.sort()

    

    random.shuffle(players)
    print([player.__dict__ for player in players])

    books = 0
    request.session['books'] = books
    player_index = 0
    print("player index", player_index)
    request.session['player_index'] = player_index
    request.session['player_name'] = players[player_index].name
    request.session['other_player_names'] = [player.name for player in players if player.name !=players[player_index].name]

    players_json = json.loads(json.dumps([player.__dict__ for player in players]))
    request.session['players'] = players_json
    
    request.session['num_cards'] = num_cards

    request.session['hand_images'] = []
    for card in players[player_index].hand:
        request.session['hand_images'].append(card_image_map[card[0]+card[1]])
    
    request.session['taken_cards_images'] = []
    request.session['fished_cards_images'] = []
    
    request.session['book_images'] = []

    #fixlater make a class
    rank_counts = {}
    for card in  players[player_index].hand:
        if card[0] not in rank_counts.keys():
            rank_counts[card[0]] = 1
        else:
            rank_counts[card[0]] += 1
    print("player", players[player_index].name, "rank counts", rank_counts)
    request.session['rank_counts'] = rank_counts

    
    
    return redirect('/gofish/maingame')
    


def maingame(request):
    user = User.objects.get(id=request.session['user_id'])
    context = {

        'user': user,
    }

    return render(request, 'fish_app/main_game.html', context)


def taketurn(request):
    print("*** POST *** \n", request.POST)
    print(request.POST['ask_player'])
    print(request.POST['ask_rank'])
    num_players = request.session['num_players']
    players = []
    players_from_session = request.session['players']
    print(players_from_session)
    for session_player in players_from_session:
        players.append(
            Player(session_player['name'], session_player['hand'], session_player['books']))
    print(players)
    ranks = request.session['ranks']
    player_index = request.session['player_index']
    books = request.session['books']
    deck = request.session['deck']
    num_cards = request.session['num_cards']

    print("************* start turn **********")
    print("player index", player_index,
          "player name: ", players[player_index].name)
    repeat_turn = False
    if len(players[player_index].hand) > 0:
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
        print("you took", taken_cards)
        players[player_index].hand += taken_cards

        if taken_cards == []:
            print("you must go fish")
            if len(deck) > 0:
                draw = deck.pop()
                print("you drew", draw)
                if draw[0] == req_rank:
                    repeat_turn = True

                players[player_index].hand.append(draw)
            else:
                print("no cards available to draw")
        else:
            repeat_turn = True
        players[player_index].hand.sort()
        print("hand now", players[player_index].hand)

        

    else:
        num_draws = min(num_cards, len(deck))
        print("drawing from deck")
        for card_num in range(num_draws):
            players[player_index].hand.append(deck.pop())
        print("player index", player_index, "player name: ",
              players[player_index].name, "player hand: ", players[player_index].hand)
        if num_draws > 0:
            repeat_turn = True
        else:
            repeat_turn = False

    # check for books
    #fixlater make rank counts a function
    rank_counts = {}
    for card in  players[player_index].hand:
        if card[0] not in rank_counts.keys():
            rank_counts[card[0]] = 1
        else:
            rank_counts[card[0]] += 1
    print("player", players[player_index].name, "rank counts", rank_counts)
    request.session['rank_counts'] = rank_counts

    
    for rank in rank_counts:
        if rank_counts[rank] >= 4:
            print("$$$$$$$$$$$$ I found a book!!!!!!!!!!")
            players[player_index].books.append(rank)
            books += 1
            print("total books", books)

            print("player", players[player_index].name, "books ", players[player_index].books)

            players[player_index].hand = [c for c in players[player_index].hand if c[0] != rank]
            print("player", players[player_index].name, "hand after book ", players[player_index].hand)
    print("total books", books)


    print("deck", deck)
    print("repeat turn", repeat_turn)
    if not repeat_turn:
        player_index = (player_index + 1) % num_players

    rank_counts = {}
    for card in  players[player_index].hand:
        if card[0] not in rank_counts.keys():
            rank_counts[card[0]] = 1
        else:
            rank_counts[card[0]] += 1
    print("player", players[player_index].name, "rank counts", rank_counts)
    request.session['rank_counts'] = rank_counts

    request.session['ranks'] = ranks
    request.session['deck'] = deck

    request.session['books'] = books
    request.session['player_index'] = player_index
    request.session['player_name'] = players[player_index].name
    request.session['other_player_names'] = [player.name for player in players if player.name !=players[player_index].name]
    players_json = json.loads(json.dumps([player.__dict__ for player in players]))
    request.session['players'] = players_json
    request.session['turn_ask'] = True
    request.session['turn_fish'] = False
    
    request.session['hand_images'] = []
    for card in players[player_index].hand:
        request.session['hand_images'].append(card_image_map[card[0]+card[1]])
    

    request.session['taken_cards_images'] = []
    try:
        for card in taken_cards:
            request.session['taken_cards_images'].append(card_image_map[card[0]+card[1]])
    except:
        pass
        
    request.session['fished_cards_images'] = []
           
    try:
        request.session['fished_cards_images'].append(card_image_map[draw[0]+draw[1]])
    except:
        pass
    
    request.session['book_images'] = []
    for book in players[player_index].books: 
        request.session['book_images'].append(card_image_map[book+'s'])
        print(card_image_map[book+'s'])

    print(request.session['book_images'])

    if request.session['books'] < len(ranks):
        if repeat_turn:
            return redirect('/gofish/maingame')
        else:
            return redirect('/gofish/handover')
    else:

        return redirect('/gofish/gameover')

def handover(request):
    

    return render(request, 'fish_app/handover.html')
def passcontrol(request):
    request.session['taken_cards_images'] = []
    request.session['fished_cards_images'] = []
    
    request.session['book_images'] = []

    return render(request, 'fish_app/passcontrol.html')

def gameover(request):
    maxbooks = 0
    for player in request.session['players']:
        print("gameover player",player)
        if len(player['books'])>maxbooks:
            maxbooks = len(player['books'])
            request.session['winner'] = player['name']
    
    return render(request, 'fish_app/gameover.html')