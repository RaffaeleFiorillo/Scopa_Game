import random
from src.AI.BaseThinking import BaseThinking
from src.Game.Matches.scopa_functions import taking_is_possible, get_index_combinations


class RandomBehaviour(BaseThinking):
	def __init__(self, table_cards):
		super().__init__(table_cards)
	
	# generates all possible ways a specific card can take
	def generate_all_possible_taking_moves(self):
		all_combinations = get_index_combinations(self.table_cards.cards)
		piked_card_number = self.cards_in_hand[self.chosen_hand_card_index].number
		combinations = []
		for combination in all_combinations:
			if taking_is_possible(piked_card_number, [self.table_cards.cards[c_index].number for c_index in combination]):
				combinations.append(combination)
		return combinations
		
	def choose_the_move(self):
		self.chosen_hand_card_index = random.randint(0, len(self.cards_in_hand) - 1)  # pick the hand-card to use
		all_taking_moves = self.generate_all_possible_taking_moves()
		
		if len(all_taking_moves) == 0:
			self.move_type = "throw"
		else:
			self.move_type = "take"
			indexes_of_cards_to_take = random.choice(all_taking_moves)
			for c_index in indexes_of_cards_to_take:
				self.table_cards.cards[c_index].active = True
		self.has_chosen = True  # must be done last because of the threading system
