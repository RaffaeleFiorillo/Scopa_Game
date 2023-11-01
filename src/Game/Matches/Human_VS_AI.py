from src.Game.Matches.Match import Match
from src.Game.Entities import Human, AI
from src.Game.PlayersLogicManager.Human_VS_AI_LogicManager import Human_VS_AI_Manager


class Human_VS_AI_Match(Match):
	def __init__(self, screen, clock, names):
		super(Human_VS_AI_Match, self).__init__(screen, clock)
		self.player1 = Human(names[0])
		self.player2 = AI(self.table_cards)
		self.players_manager = Human_VS_AI_Manager(self.table_cards, self.player1, self.player2)
