from src.Game.Entities.Cards.Card import Card
from pygame import draw


class Player:
    def __init__(self, name, taken_cards_y_coo):
        self.total_score: int = 0
        self.match_score: int = 0
        self.name: str = name
        self.state = "waiting"
        self.cards_in_hand: [Card] = []
        self.cards_taken: [Card] = []
        self.cards_taken_y_coo = taken_cards_y_coo
        self.selected_card = None

    def count_score(self):
        pass

    def take_cards_from_deck(self, cards: [Card]):
        self.cards_in_hand = cards

    def take_cards(self, cards):
        # points should be updated here
        self.cards_taken += cards  # take the cards from the table
        self.cards_taken.append(self.pop_selected_card())  # take the card used to take those cards
        self.end_turn()

    def pop_selected_card(self):
        for i, card in enumerate(self.cards_in_hand):
            if card.active:
                card.active = False
                self.selected_card = None
                return self.cards_in_hand.pop(i)
        self.end_turn()
        
    def end_turn(self):
        self.state = "waiting"

    def draw(self, screen):
        if not self.cards_taken:
            draw.rect(screen, (120, 74, 50), (930, self.cards_taken_y_coo, 135, 227))
