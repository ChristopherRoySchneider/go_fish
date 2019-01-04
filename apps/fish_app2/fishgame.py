import json
import random

def draw(player, deck, num_cards):
    num_cards = min(num_cards, len(deck))
    if len(deck)<1:
        print("no cards available to draw")
    print("drawing",num_cards,"from deck")
    drawn_cards = []
    for card_num in range(num_cards):
        # print("drawing card",card_num+1,"of",num_cards)
        # print(player)
        drawn_cards.append(deck.pop())
        # print(player)
    player.hand += drawn_cards
    player.hand.sort()
    return drawn_cards


class Player:
    def __init__(self, name, hand=None, books=None):
        self.name = name
        self.hand = hand if hand is not None else []
        self.books = books if books is not None else []
    def rank_counts(self):
        rank_counts = {}
        for card in self.hand:
            if card[0] not in rank_counts.keys():
                rank_counts[card[0]] = 1
            else:
                rank_counts[card[0]] += 1
        return rank_counts
    def make_books(self):
        print("checking for books")
        # print(self.rank_counts())
        for rank in self.rank_counts():
            # print(rank)
            # print(self.rank_counts()[rank])
            if self.rank_counts()[rank] >= 4:

                print("$$$$$$$$$$$$ I found a book!!!!!!!!!!")
                self.books.append(rank)
                
                print("player", self.name, "books ", self.books)

                self.hand = [c for c in self.hand if c[0] != rank]
                print("player", self.name, "hand after book ", self.hand)
                return True
            else:
                pass
        return False
        

    def __repr__(self):
        return str("Player Class: " + str(self.__dict__))


class Game:

    def __init__(self, players, name=1, num_players = 2, deck = None, new_game = True, rank_length = 5, player_index = 0, books = 0, game_over = False):
        self.name = name
        self.deck = deck if deck is not None else []
        self.num_players = num_players
        self.new_game = new_game
        self.rank_length = rank_length
        self.game_over = game_over
        self.ranks = "A23456789TJQK"
        self.suits = "cdhs"

        if new_game:
            
            self.deck = [] 

            for num in range(self.rank_length):
                for suit in self.suits:
                    self.deck.append([self.ranks[num], suit])

            random.shuffle(self.deck)
            print("deck",self.deck)
        else:
            self.deck = deck

        players_to_cards = {
            2: 7,
            3: 6,
            4: 5,
        }

        self.starting_num_cards = players_to_cards[self.num_players]

        self.players = players

        if new_game:
            for player in self.players:
                player.hand = [] 
                player.books = []
                draw(player, self.deck, self.starting_num_cards)
            self.player_index = random.randint(0,self.num_players-1)
            self.books = 0
        else:
            self.player_index = player_index 
            self.books = books
        

        print([p.__dict__ for p in self.players])

        print("player index", self.player_index)

        self.new_game = False
        
    def take_turn(self, req_player, req_rank):
        print("************* start turn **********")
        print("player index", self.player_index,
          "player name: ", self.players[self.player_index].name)
        self.repeat_turn = False

        if len(self.players[self.player_index].hand) > 0:
            #if you have cards you can request from another player
            print(self.players[self.player_index].hand)
            print(req_player, req_rank)

            for player in self.players:
                if player.name == req_player:
                    self.taken_cards = [card for card in player.hand if card[0] == req_rank]
                    player.hand = [card for card in player.hand if card[0] != req_rank]
            print("you took", self.taken_cards)

            self.players[self.player_index].hand += self.taken_cards

            if self.taken_cards == []:
                print("you must go fish")
                self.fished = draw(self.players[self.player_index], self.deck, 1)

                
                print("you fished", self.fished)
                if self.fished == []:
                    pass
                elif self.fished[0][0] == req_rank:
                    self.repeat_turn = True


            else:
                self.repeat_turn = True
            self.players[self.player_index].hand.sort()
            print("hand now", self.players[self.player_index].hand)

            

        else:

            #if you do not have cards you must draw
            print("no cards in hand - drawing from deck")
            drawn = draw(self.players[self.player_index],self.deck, self.starting_num_cards)
            
            if len(drawn) > 0:
                self.repeat_turn = True
            else:
                self.repeat_turn = False

        # check for books

        if self.players[self.player_index].make_books():
            self.books += 1
        print("total books in game", self.books)
        print("player", self.players[self.player_index].name, "books ", self.players[self.player_index].books)


        print("deck", self.deck)
        print("repeat turn", self.repeat_turn)
        if not self.repeat_turn:
            self.player_index = (self.player_index + 1) % self.num_players

       
        print("player", self.players[self.player_index].name, "rank counts", self.players[self.player_index].rank_counts())
        print([p.__dict__ for p in self.players])
        
        if self.books >= self.rank_length:
            print('Game Over')
            self.game_over = True
            winner = ''
            winner_books = []
            for p in self.players:
                if len(p.books) > len(winner_books):
                    winner_books = p.books
                    winner = p.name
            print(winner, "won with", len(winner_books),"books:",winner_books)

        
            
            
            