import unittest
import random
import math


class Card:
    def __init__(self, id):
        self.id = id
        self.rank_id = math.floor(self.id/4)
        self.suit_id = self.id % 4

        ranks = {
            0: "A",
            1: "2",
            2: "3",
            3: "4",
            4: "5",
            5: "6",
            6: "7",
            7: "8",
            8: "9",
            9: "T",
            10: "J",
            11: "Q",
            12: "K",
        }

        self.rank = ranks[self.rank_id]

        suits = {
            0: "c",
            1: "d",
            2: "h",
            3: "s",
        }
        self.suit = suits[self.suit_id]

    def __str__(self):
        return self.rank + self.suit
    def __lt__(self, other):
        return (self.rank_id <other.rank_id)


class Deck:
    def __init__(self, card_ids=None):
        if card_ids == None:
            self.cards = [Card(x) for x in range(52)]
        else:
            self.cards = [Card(x) for x in card_ids]

    def show_cards(self):
        return [str(card) for card in self.cards]

    def shuffle(self):
        random.shuffle(self.cards)
        return self

    def draw(self, num_cards=1):
        arr = []
        for i in range(num_cards):
            try:
                arr.append(self.cards.pop())
            except:
                return arr
        return arr


class Hand:
    def __init__(self):
        self.cards = []

    def draw_cards(self, deck, num_cards=1):
        self.cards += (deck.draw(num_cards))
        return self

    def show_cards(self):
        return [str(card) for card in self.cards]

    def has_rank(self, rank):
        for card in self.cards:
            print("checking rank match",card.rank)
            if card.rank == rank:
                return True
            else:
                continue
         
            return False
    def sort(self):
        self.cards.sort()
        return self
