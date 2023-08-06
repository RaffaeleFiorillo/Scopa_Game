from src.Game.Entities.Players.Player import Player
from pygame import draw


class Human(Player):
    def __init__(self, nome):
        super().__init__(nome)
        self.selected_card = None

    # returns the index of the card where the mouse is hovering. Returns -1 if no card is being hovered over
    def mouse_is_on_card(self, mouse_position):
        for i, card in enumerate(self.cards_in_hand):
            if card.mouse_is_inside(mouse_position):
                return i
        return -1

    # reverts the state of the card to its opposite and deselect all other cards
    def toggle_card(self, card_index):
        for i, card in enumerate(self.cards_in_hand):
            if i == card_index:
                card.active = not card.active
                self.selected_card = card if card.active else None
            else:
                card.active = False

    def highlight_hovered_card(self, mouse_position):
        for card in self.cards_in_hand:
            card.hoovered = card.mouse_is_inside(mouse_position)

    def take_cards(self, cards):
        # points should be updated here
        self.cards_taken += cards  # take the cards from the table
        self.cards_taken.append(self.pop_selected_card())  # take the card used to take those cards

    def pop_selected_card(self):
        for i, card in enumerate(self.cards_in_hand):
            if card.active:
                card.active = False
                self.selected_card = None
                return self.cards_in_hand.pop(i)

    def draw(self, screen):
        if not self.cards_taken:
            draw.rect(screen, (120, 74, 50), (930, 476, 135, 227))
        for i, card in enumerate(self.cards_in_hand):
            card.draw(screen)
