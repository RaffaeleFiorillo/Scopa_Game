from src.AI.BaseThinking import BaseThinking
from src.Game.Matches.scopa_functions import pick_best_move


class DirectBestMove(BaseThinking):
	def __init__(self):
		super().__init__()
	
	def choose_the_move(self):
		pick_best_move(self.cards_in_hand, self.table_cards)
		self.has_chosen = True
		self.move_type = "waiting"  # should be "take" or "throw"
