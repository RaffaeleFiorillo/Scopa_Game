from src.Game.Entities.Players.Player import Player
from pygame import draw


class Human(Player):
    def __init__(self, nome):
        super().__init__(nome)

    def activate_cards_in_hand(self, mouse_pos):
        for card in self.cards_in_hand:
            if card.mouse_dentro(mouse_pos):
                card.active = not card.active  # reverts the state of the card to its opposite
                return card.active

    def draw(self, screen):
        if not self.cards_taken:
            draw.rect(screen, (120, 74, 50), (930, 476, 135, 227))
        for i, card in enumerate(self.cards_in_hand):
            card.draw(screen)
