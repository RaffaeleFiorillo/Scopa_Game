from pygame.transform import scale
from pygame.image import load
from src.Globals.Variables.Cards import CARD_SCALES


class PlayerAnimation:
	card_in_hand_image = None
	cards_in_hand = []
	
	def __init__(self):
		self.card_in_hand_image = scale(load("assets/retro/1.png").convert_alpha(), CARD_SCALES["player-ai"])
	
	def reset(self):
		pass
	
	def update(self, dt, cards):
		self.cards_in_hand = cards
	
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
