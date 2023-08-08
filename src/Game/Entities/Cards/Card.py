from pygame.image import load
from pygame.transform import scale
from pygame import draw
from src.global_variables import CARD_SCALES, COO_CARDS, card_type


class Card:
	def __init__(self, number, seme):
		self.number = number  # number between 1 and 10 representing the value of the card
		self.seme = seme  # represents the "house" of the card: Denara, Bastoni, Spade, Coppe
		self.img_dir = f"assets/cards/{card_type}/{seme}/{number}.png"  # directory of the image of the card
		self.active = False  # card has been selected
		self.hoovered = False  # card has the cursor on it
		self.image = None  # image of the card
		self.coo = None  # where the card is printed on the screen
		self.size = None  # size of the card. It depends if the card is on the table (small) or in player's hand (big)
		self.order = None

	def load_card(self, tipo, order):
		image = load(self.img_dir).convert_alpha()
		self.image = scale(image, CARD_SCALES[tipo])
		self.coo = COO_CARDS[tipo][order]
		self.size = CARD_SCALES[tipo]
		self.order = order

	def mouse_is_inside(self, coo_mouse: (int, int)):
		cursor_x, cursor_y = coo_mouse[0], coo_mouse[1]
		if self.coo[0] <= cursor_x <= self.coo[0] + self.size[0]:
			if self.coo[1] <= cursor_y <= self.coo[1] + self.size[1]:
				return True
		return False

	def draw(self, screen, border_color=(0, 255, 255)):
		if self.active:
			draw.rect(screen, border_color, (self.coo[0]-12, self.coo[1]-12, self.size[0]+24, self.size[1]+24))
		elif self.hoovered:
			draw.rect(screen, (233, 213, 22), (self.coo[0]-5, self.coo[1]-5, self.size[0]+10, self.size[1]+10))
		screen.blit(self.image, self.coo)
