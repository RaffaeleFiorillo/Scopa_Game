from pygame.transform import scale
from pygame.image import load
from src.Globals.Variables.Cards import CARD_SCALES


class PlayerAnimation:
	card_in_hand_image = None
	cards_in_hand = []
	len_cards_in_hand = 3
	body_color = (4, 5, 132)
	left_elbow_coo = (602, 235)
	right_elbow_coo = (464, 235)
	
	def __init__(self):
		self.has_ended = True  # must change to false
		self.card_in_hand_image = scale(load("assets/retro/1.png").convert_alpha(), CARD_SCALES["player-ai"])
		self.time_lapse = 0  # amount of time passed since the beginning of the animation
	
	def reset(self):
		self.time_lapse = 0
		self.has_ended = False
	
	def update(self, dt, cards):
		self.cards_in_hand = cards
		self.len_cards_in_hand = len(self.cards_in_hand)
	
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
