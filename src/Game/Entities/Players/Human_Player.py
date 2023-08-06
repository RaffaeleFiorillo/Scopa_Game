from src.Game.Entities.Players.Player import Player
from pygame import draw


class Human(Player):
    def __init__(self, nome):
        super().__init__(nome)

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
            else:
                card.active = False

    def highlight_hovered_card(self, mouse_position):
        for card in self.cards_in_hand:
            card.hoovered = card.mouse_is_inside(mouse_position)

    def draw(self, screen):
        if not self.cards_taken:
            draw.rect(screen, (120, 74, 50), (930, 476, 135, 227))
        for i, card in enumerate(self.cards_in_hand):
            card.draw(screen)
