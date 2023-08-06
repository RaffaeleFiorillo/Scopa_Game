from src.Game.Entities.Players.Player import Player
from pygame import draw


class Human(Player):
    def __init__(self, nome):
        super().__init__(nome)

    def activate_card(self, mouse_position):
        card_was_activated = False
        for card in self.cards_in_hand:
            if card.mouse_is_inside(mouse_position):
                card.active = not card.active  # reverts the state of the card to its opposite
                card_was_activated = True
            else:
                card.active = False
        return card_was_activated

    def highlight_hovered_card(self, mouse_position):
        for card in self.cards_in_hand:
            card.hoovered = card.mouse_is_inside(mouse_position)

    def draw(self, screen):
        if not self.cards_taken:
            draw.rect(screen, (120, 74, 50), (930, 476, 135, 227))
        for i, card in enumerate(self.cards_in_hand):
            card.draw(screen)
