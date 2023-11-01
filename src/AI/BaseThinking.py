from src.Game.Entities.Cards.TableCards import TableCards
from src.Game.Entities.Cards.Card import Card


class BaseThinking:
	def __init__(self, table_cards: TableCards):
		self.has_chosen = False
		self.move_type = ""  # "take" or "throw"
		self.table_cards = table_cards
		self.cards_in_hand: [Card] = []
		self.chosen_hand_card_index = None  # the index of the card chosen to be played (0,1 or 2)
	
	def choose_the_move(self):
		pass
