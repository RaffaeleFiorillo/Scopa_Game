from src.AI.BaseThinking import BaseThinking


class MiniMax(BaseThinking):
	def __init__(self):
		super().__init__()
	
	def choose_the_move(self):
		move, best_move = self.minmax(self.cards_in_hand, self.table_cards, depth=6, is_maximizing_player=True)
		self.has_chosen = True
		self.move_type = "waiting"  # should be "take" or "throw"
	
	def evaluate_state(self, player_hand, table_cards):
		# Implement the evaluation logic to assign values to different states
		# This can include card values, potential card-taking, etc.
		pass
	
	def generate_moves(self, player_hand, table_cards):
		# Generate a list of possible moves based on player's hand and table cards
		pass
	
	def apply_move(self, move_type, card_played, cards_taken, player_hand, table_cards):
		# Apply the selected move to update player's hand and table cards
		pass
	
	def minmax(self, player_hand, table_cards, depth, is_maximizing_player):
		if depth == 0 or len(self.cards_in_hand) == 0:
			return self.evaluate_state(player_hand, table_cards), None
		
		if is_maximizing_player:
			best_value = float('-inf')
			best_move = None
			for move in self.generate_moves(player_hand, table_cards):
				new_player_hand, new_table_cards = self.apply_move(*move, player_hand, table_cards)
				value, _ = self.minmax(new_player_hand, new_table_cards, depth - 1, False)
				if value > best_value:
					best_value = value
					best_move = move
			return best_value, best_move
		else:
			return get_best_possible_moves(table_cards)
			
			
"""
# Max part of the minimax
best_value = float('inf')
			best_move = None
			for move in self.generate_moves(player_hand, table_cards):
				new_player_hand, new_table_cards = self.apply_move(*move, player_hand, table_cards)
				value, _ = self.minmax(new_player_hand, new_table_cards, depth - 1, True)
				if value < best_value:
					best_value = value
					best_move = move
			return best_value, best_move
"""
	