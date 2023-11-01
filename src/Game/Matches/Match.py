import pygame
from src.Game.Entities import Deck, TableCards
from src.Game.Entities.Players.Player import Player
from src.Game.PlayersLogicManager.Human_VS_AI_LogicManager import PlayersManager
# from src.Animations.animation_collection import play_animation
from src.Globals.Configurations.Game import FPS


class Match:
	def __init__(self, screen, clock):
		self.background = pygame.image.load("assets\\background.jpg").convert_alpha()
		self.clock = clock
		self.dt = 0
		self.screen = screen
		self.deck = Deck()
		self.table_cards = TableCards()
		
		# noinspection PyTypeChecker
		self.player1: Player = None
		# noinspection PyTypeChecker
		self.player2: Player = None
		# noinspection PyTypeChecker
		self.players_manager: PlayersManager = None
		# play_animation(self.screen, "choosing_player")
		
	# ------------------------------------------------ AUXILIARY -------------------------------------------------------
	def give_cards(self):
		# 1- animation of player 1 getting his cards into his hands
		self.player1.cards_in_hand = self.deck.draw_cards("player")
		# 2- animation of player 2 getting his cards into his hands
		self.player2.cards_in_hand = self.deck.draw_cards("player")
		
	#  --------------------------------------------- MAIN FUNCTIONS ----------------------------------------------------
	def start(self):
		# 1- animation of the cards going to the table: move from deck to table (face down) and the get facing up
		self.table_cards.cards = self.deck.draw_cards("table")  # put the cards on the table
		self.game_loop()  # starting the actual game
	
	def game_loop(self):
		match_is_on, rounds_left = True, 6
		while match_is_on:
			# controls what to do at the start of each round, and happens when the players have no cards left to play
			if not (len(self.player1.cards_in_hand) and len(self.player2.cards_in_hand)) and rounds_left > 1:
				self.give_cards()
				rounds_left -= 1
				match_is_on = rounds_left >= 0  # if there are no more cards in the deck the match is over
			
			# handling the input of the human player and its effects on the game
			self.players_manager.manage_player1_input()
			# Manages the AI actions based on whether it's its turn to move
			self.players_manager.manage_player2_input()
			
			# applying changes
			self.dt = self.clock.tick(FPS) / 1000
			self.update()
			self.refresh()
			
		self.end_of_match()
		
	def update(self):
		self.players_manager.update(self.dt)
	
	# refreshes the screen to display recent updates in the game
	def refresh(self):
		self.screen.blit(self.background, (0, 0))
		self.player2.draw(self.screen)
		self.player1.draw(self.screen)
		self.table_cards.draw(self.screen)
		pygame.display.update()
		
	def end_of_match(self):
		print("Game Over")
		pygame.time.wait(20000)
		self.deck.show_deck()
