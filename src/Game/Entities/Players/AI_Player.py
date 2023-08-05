from src.Game.Entities.Players.Player import Player
from pygame.image import load
from pygame.transform import scale
from src.global_variables import CARD_SCALES


class AI(Player):
    def __init__(self):
        super().__init__("R.F.J.8")
        image = load("assets/retro/1.png").convert_alpha()
        self.card_in_hand_image = scale(image, CARD_SCALES["hand-ai"])

    def draw(self, screen):
        if len(self.cards_in_hand) == 3:
            screen.blit(self.card_in_hand_image, (480, 150))
            screen.blit(self.card_in_hand_image, (510, 150))
            screen.blit(self.card_in_hand_image, (540, 150))
        elif len(self.cards_in_hand) == 2:
            screen.blit(self.card_in_hand_image, (495, 150))
            screen.blit(self.card_in_hand_image, (530, 150))
        elif len(self.cards_in_hand) == 1:
            screen.blit(self.card_in_hand_image, (512, 150))
