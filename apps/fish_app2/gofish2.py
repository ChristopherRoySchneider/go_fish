
import random
import itertools


class Player:
    def __init__(self, name="", hand=[]):
        self.name = name
        self.hand = []
        self.books = []


deck = []

ranks = "A2345"
suits = "cdhs"

# ranks = "A23456789TJQK"
# suits = "cdhs"

for rank in ranks:
    for suit in suits:
        deck.append([rank, suit])

random.shuffle(deck)

print(deck)

num_players = int(input("number of players: "))

players_to_cards = {
    2: 7,
    3: 6,
    4: 5,
}

num_cards = players_to_cards[num_players]
players = []


for player_num in range(num_players):
    name = input(f"name for player {player_num+1}: ")
    players.append(Player(name))
    for card_num in range(num_cards):
        players[player_num].hand.append(deck.pop())

print([player.__dict__ for player in players])

random.shuffle(players)


books = 0
player_index = 0

while books < len(ranks):
    print("************* start turn **********")
    print("player index", player_index,
          "player name: ", players[player_index].name)
    repeat_turn = False
    if len(players[player_index].hand) > 0:

        players[player_index].hand.sort()
        print(players[player_index].hand)

        req_player, req_rank = input(
            "enter player name and rank to request: ").split()
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

        # check for books

        for player in players:
            rank_counts = {}
            for card in player.hand:
                if card[0] not in rank_counts.keys():
                    rank_counts[card[0]] = 1
                else:
                    rank_counts[card[0]] += 1
            print("player", player.name, "rank counts", rank_counts)
            for rank in rank_counts:
                if rank_counts[rank] == 4:
                    player.books.append(rank)
                    books += 1
                    print("total books", books)

                    print("player", player.name, "books ", player.books)

                    player.hand = [c for c in player.hand if c[0] != rank]
                    print("player", player.name,
                          "hand after book ", player.hand)
        print("total books", books)

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

    print("deck", deck)
    print("repeat turn", repeat_turn)
    if not repeat_turn:
        player_index = (player_index + 1) % num_players
