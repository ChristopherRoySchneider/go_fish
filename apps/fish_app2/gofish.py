from cards import Card, Deck, Hand
import random
import itertools



deck=Deck().shuffle()
num_players = int(input("number of players: "))

players_to_cards = {
    2:7,
    3:6,
    4:5,
}
num_cards = players_to_cards[num_players]
players = []
for num in range(num_players):
    players.append(
        {
            'name':  input(f"name for player {num+1}: "),
            'hand': Hand().draw_cards(deck,num_cards)
        }
    )

random.shuffle(players)

for player in players:
    print(player, player['hand'].show_cards())

print("****************************")

books = 0
player_index = 0
while books < 13:
    print("player index",player_index, "player name: ", players[player_index]['name'])
    players[player_index]['hand'].cards.sort()
    print(players[player_index]['hand'].show_cards())
    req_player , req_rank = input("enter player index and rank to request: ").split()
    print(req_player, req_rank)
    req_player = int(req_player)
    if players[req_player]['hand'].has_rank(req_rank):
        print("moving cards from", req_player)
        print(players[req_player]['hand'].show_cards())
        for card in players[req_player]['hand'].cards:
            if card.rank == req_rank:
                print("rank matches")
                players[player_index].cards.append(card)
                players["name"==req_player].cards.remove(card)
    else:
        print(False)
    books +=1
    player_index = (player_index +1) % num_players



