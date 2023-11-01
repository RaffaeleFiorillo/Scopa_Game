class BaseThinking:
	def __init__(self):
		self.has_chosen = False
		self.move_type = "waiting"  # "taking" or "throwing"
		self.table_cards = []
		self.hand_cards = []
		self.chosen_hand_card_index = None  # the index of the card chosen to be played (0,1 or 2)
	
	def choose_the_move(self):
		pass
