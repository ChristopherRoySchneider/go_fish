from django.shortcuts import render, HttpResponse, redirect
from .cards import Card, Hand, Deck
from apps.login_app.models import User
from django.contrib import messages
import json
import random
from . import models
from .fishgame import Player, Game, draw


def make_game_from_db(game_id):
    game_in_db = models.Game.objects.get(id = game_id)
    print(game_in_db.__dict__)

    players_new = [None]* len(game_in_db.players.all()) 
    for p in game_in_db.players.all():
        players_new[p.position] = Player(p.user.username, json.loads(p.hand), json.loads(p.books))
    
    print("player list created from DB",players_new)

    game = Game(players = players_new, name = game_in_db.id, num_players = len(game_in_db.players.all()),
        deck = json.loads(game_in_db.deck), new_game = False, player_index=game_in_db.player_index, books=game_in_db.books )

    print("game created from DB:", game.__dict__)
    return game

def save_game_to_db(game_id, game):
    print("saving game to db")
    
    game_in_db = models.Game.objects.get(id = game_id)
    game_in_db.deck = json.dumps(game.deck)
    game_in_db.player_index = game.player_index 
    game_in_db.books = game.books
    game_in_db.game_over = game.game_over
    game_in_db.save()
    for p in game_in_db.players.all():
        p.hand = json.dumps(game.players[p.position].hand)
        p.books = json.dumps(game.players[p.position].books)
        p.save()
    
    print("done saving")




card_image_map = {'Tc': 'fish_app2/images/cards/10_clubs.png', 'Td': 'fish_app2/images/cards/10_diamonds.png', 'Th': 'fish_app2/images/cards/10_hearts.png', 'Ts': 'fish_app2/images/cards/10_spades.png', '2c': 'fish_app2/images/cards/2_clubs.png', '2d': 'fish_app2/images/cards/2_diamonds.png', '2h': 'fish_app2/images/cards/2_hearts.png', '2s': 'fish_app2/images/cards/2_spades.png', '3c': 'fish_app2/images/cards/3_clubs.png', '3d': 'fish_app2/images/cards/3_diamonds.png', '3h': 'fish_app2/images/cards/3_hearts.png', '3s': 'fish_app2/images/cards/3_spades.png', '4c': 'fish_app2/images/cards/4_clubs.png', '4d': 'fish_app2/images/cards/4_diamonds.png', '4h': 'fish_app2/images/cards/4_hearts.png', '4s': 'fish_app2/images/cards/4_spades.png', '5c': 'fish_app2/images/cards/5_clubs.png', '5d': 'fish_app2/images/cards/5_diamonds.png', '5h': 'fish_app2/images/cards/5_hearts.png', '5s': 'fish_app2/images/cards/5_spades.png', '6c': 'fish_app2/images/cards/6_clubs.png', '6d': 'fish_app2/images/cards/6_diamonds.png', '6h': 'fish_app2/images/cards/6_hearts.png', '6s': 'fish_app2/images/cards/6_spades.png', '7c': 'fish_app2/images/cards/7_clubs.png', '7d': 'fish_app2/images/cards/7_diamonds.png', '7h': 'fish_app2/images/cards/7_hearts.png',
                  '7s': 'fish_app2/images/cards/7_spades.png', '8c': 'fish_app2/images/cards/8_clubs.png', '8d': 'fish_app2/images/cards/8_diamonds.png', '8h': 'fish_app2/images/cards/8_hearts.png', '8s': 'fish_app2/images/cards/8_spades.png', '9c': 'fish_app2/images/cards/9_clubs.png', '9d': 'fish_app2/images/cards/9_diamonds.png', '9h': 'fish_app2/images/cards/9_hearts.png', '9s': 'fish_app2/images/cards/9_spades.png', 'Ac': 'fish_app2/images/cards/ace_clubs.png', 'Ad': 'fish_app2/images/cards/ace_diamonds.png', 'Ah': 'fish_app2/images/cards/ace_hearts.png', 'As': 'fish_app2/images/cards/ace_spades.png', 'Jc': 'fish_app2/images/cards/jack_clubs.png', 'Jd': 'fish_app2/images/cards/jack_diamonds.png', 'Jh': 'fish_app2/images/cards/jack_hearts.png', 'Js': 'fish_app2/images/cards/jack_spades.png', 'Kc': 'fish_app2/images/cards/king_clubs.png', 'Kd': 'fish_app2/images/cards/king_diamonds.png', 'Kh': 'fish_app2/images/cards/king_hearts.png', 'Ks': 'fish_app2/images/cards/king_spades.png', 'Qc': 'fish_app2/images/cards/queen_clubs.png', 'Qd': 'fish_app2/images/cards/queen_diamonds.png', 'Qh': 'fish_app2/images/cards/queen_hearts.png', 'Qs': 'fish_app2/images/cards/queen_spades.png'}


def index(request):
    user = User.objects.get(id = request.session['user_id'])
    all_other_users = User.objects.exclude(id=user.id)
    context = {
        'user':user,
        'all_other_users': all_other_users
    }
    return render(request,'fish_app2/index.html', context)
###


def initialize(request):

    print(request.POST)
    if request.POST['new_game']=="True":
        num_players = int(request.POST['num_players'])
        request.session['num_players'] = num_players
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

        for i in range(num_players):
            name = player_ids[i]
            p1 = Player(name)
            players.append(p1)
            
        game = Game(num_players = num_players, players=players)
        models.Game.objects.create(game_over = False, deck = json.dumps(game.deck), player_index = game.player_index, books = 0 )
        game_in_db = models.Game.objects.last()
        request.session['game_id'] = game_in_db.id
        for i in range(len(game.players)):
            user = models.User.objects.get(username = game.players[i].name)
            models.Player.objects.create(position = i, game = game_in_db, user = user, hand = json.dumps(game.players[i].hand), books = json.dumps(game.players[i].books) )

    print([player.__dict__ for player in game.players])
    
    request.session['ranks'] = game.ranks[:game.rank_length]
    request.session['deck'] = game.deck
    request.session['books'] = game.books
    
    print("player index", game.player_index)
    request.session['player_index'] = game.player_index
    request.session['player_name'] = game.players[game.player_index].name
    request.session['other_player_names'] = [player.name for player in game.players if player.name !=players[game.player_index].name]

    players_json = json.loads(json.dumps([player.__dict__ for player in game.players]))
    request.session['players'] = players_json
    
    request.session['num_cards'] = game.starting_num_cards

    request.session['hand_images'] = []
    for card in game.players[game.player_index].hand:
        request.session['hand_images'].append(card_image_map[card[0]+card[1]])
    
    request.session['taken_cards_images'] = []
    request.session['fished_cards_images'] = []
    
    request.session['book_images'] = []

   
    print("player", game.players[game.player_index].name, "rank counts", game.players[game.player_index].rank_counts())
    request.session['rank_counts'] = game.players[game.player_index].rank_counts()

    
    
    return redirect('/gofish/passcontrol')
    


def maingame(request):
    user = User.objects.get(id=request.session['user_id'])
    context = {

        'user': user,
    }

    return render(request, 'fish_app2/main_game.html', context)


def taketurn(request):
    print("*** POST *** \n", request.POST)
    print(request.POST['ask_player'])
    print(request.POST['ask_rank'])
    
    game = make_game_from_db(int(request.session['game_id']))

    print("******************* start game.take_turn************")
    game.take_turn(request.POST['ask_player'],request.POST['ask_rank'])
    print("******************* END game.take_turn************")

    save_game_to_db(int(request.session['game_id']),game)
    
    request.session['rank_counts'] = game.players[game.player_index].rank_counts()

    request.session['ranks'] = game.ranks[:game.rank_length]
    request.session['deck'] = game.deck

    request.session['books'] = game.books
    request.session['player_index'] = game.player_index
    request.session['player_name'] = game.players[game.player_index].name
    request.session['other_player_names'] = [player.name for player in game.players 
        if player.name != game.players[game.player_index].name]
    players_json = json.loads(json.dumps([player.__dict__ for player in game.players]))
    request.session['players'] = players_json
    
    
    request.session['hand_images'] = []
    for card in game.players[game.player_index].hand:
        request.session['hand_images'].append(card_image_map[card[0]+card[1]])
    

    request.session['taken_cards_images'] = []
    try:
        for card in game.taken_cards:
            request.session['taken_cards_images'].append(card_image_map[card[0]+card[1]])
    except:
        pass
        
    request.session['fished_cards_images'] = []
           
    try:
        request.session['fished_cards_images'].append(card_image_map[game.fished[0][0]+game.fished[0][1]])
    except:
        pass
    
    request.session['book_images'] = []
    for book in game.players[game.player_index].books: 
        request.session['book_images'].append(card_image_map[book+'s'])
        print(card_image_map[book+'s'])

    print(request.session['book_images'])

    if not game.game_over:
        if game.repeat_turn:
            return redirect('/gofish/maingame')
        else:
            return redirect('/gofish/handover')
    else:

        return redirect('/gofish/gameover')

def handover(request):
    

    return render(request, 'fish_app2/handover.html')
def passcontrol(request):
    request.session['taken_cards_images'] = []
    request.session['fished_cards_images'] = []
    
    request.session['book_images'] = []

    return render(request, 'fish_app2/passcontrol.html')

def gameover(request):
    maxbooks = 0
    for player in request.session['players']:
        print("gameover player",player)
        if len(player['books'])>maxbooks:
            maxbooks = len(player['books'])
            request.session['winner'] = player['name']
    
    return render(request, 'fish_app2/gameover.html')