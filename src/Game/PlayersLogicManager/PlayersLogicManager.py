from random import choice
from src.Game.Entities.Players.Player import Player
from src.Game.Entities.Cards import TableCards


class PlayersManager:
	def __init__(self,  table_cards: TableCards, player1: Player, player2: Player):
		self.table_cards = table_cards
		self.player1 = player1
		self.player2 = player2
		self.turn = choice(("1", "2"))  # the player to play first is chosen at random
	
	def manage_player1_input(self) -> None:
		pass
	
	def manage_player2_input(self) -> None:
		pass
	
	def update(self, dt):
		pass
