from src.Game.Entities.Cards.Card import Card


class Player:
    def __init__(self, name):
        self.total_score: int = 0
        self.match_score: int = 0
        self.name: str = name
        self.state = "waiting"
        self.cards_in_hand: [Card] = []
        self.cards_taken: [Card] = []
        self.selected_card = None

    def count_score(self):
        pass

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
        pass
