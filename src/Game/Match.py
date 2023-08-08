from src.Game.Entities import Deck, Human, AI, TableCards
from src.Game.scopa_functions import taking_is_possible
# from src.Animations.animation_collection import play_animation
import pygame
from src.Globals.Configurations.Game import FPS


class Match:
	def __init__(self, screen, names, clock):
		self.background = pygame.image.load("assets\\background.jpg").convert_alpha()
		self.deck = Deck()
		self.table_cards = TableCards()
		self.player1 = Human(names[0])
		self.player2 = AI()
		self.clock = clock
		self.screen = screen
		
		# the mode says if the player is "choosing" (the card to play), "taking" (cards on the table) or "waiting"
		# (the other player to make a move)
		self.mode = "choice"
		# incomplete-take, valid-take, invalid-take, throw,
		self.move_type = "incomplete-take"
	
	# play_animation(self.screen, "choosing_player")
	
	def draw(self, screen):
		screen.blit(self.background, (0, 0))
		self.player2.draw(self.screen)
		self.player1.draw(self.screen, self.move_type)
		self.table_cards.draw(self.screen, self.move_type)
	
	def refresh(self):
		self.draw(self.screen)
		pygame.display.update()
	
	def game_loop(self):
		while len(self.deck.cards):  # if there are no more cards in the deck the match is over
			if not (len(self.player1.cards_in_hand) and len(self.player2.cards_in_hand)):
				self.give_cards()
			mouse_pos = pygame.mouse.get_pos()  # avoid multiples execution of the same function
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					exit()
				elif self.mode != "wait":  # the player is only allowed to play on its turn
					if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
						self.manage_mouse_events(mouse_pos)
					elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN and self.player1.selected_card:
						# the player can use a card to take or just throw it on the table
						if self.move_type == "valid-take":  # if possible, the player must use the selected card to take
							self.player1.take_cards(self.table_cards.pop_selected_cards())
						elif self.move_type == "incomplete-take":
							pass  # make some error noise and show the user why
						elif self.move_type == "invalid-take":  # if unable to take, the card is thrown on the table
							pass  # make some error noise and show the user why
						elif self.move_type == "valid-throw":
							self.table_cards.receive_card(self.player1.pop_selected_card())
						elif self.move_type == "invalid-throw":
							pass  # make some error noise and show the user why
			
			self.highlight_hovered_card(mouse_pos)
			self.refresh()
			self.clock.tick(FPS)
		self.end_of_match()
	
	def end_of_match(self):
		print("Game Over")
		self.deck.show_deck()
	
	def give_cards(self):
		self.player1.cards_in_hand = self.deck.draw_cards("player")
		# 2- animation of player 1 getting his cards into his hands
		self.player2.cards_in_hand = self.deck.draw_cards("player")
	
	# 4- animation of player 2 getting his cards into his hands
	
	def manage_mouse_events(self, mouse_position):
		# player has chosen a card in his hand
		if (card_index := self.player1.mouse_is_on_card(mouse_position)) > -1:
			# changing mode in order to enable the player to take cards on the table
			self.player1.toggle_card(card_index)
			self.table_cards.disable_all_cards()  # cards selected on the table are deselected
			if self.player1.selected_card is None:
				self.mode = "choice"
			else:
				self.mode = "take"
				self.apply_throwing_rules()  # check if what the user is doing is valid for a throw move
			# [1- create a list of possible moves for the chosen card
			# 2- activate the cards on the table that would be taken using the selected card]
		# player has chosen a card on the table
		elif self.mode == "take":
			self.table_cards.activate_cards(mouse_position)
			if len([1 for card in self.table_cards.cards if card.active]) == 0:
				self.apply_throwing_rules()
			else:
				self.apply_taking_rules()  # check if what the user is doing is valid for a taking move
	
	def apply_taking_rules(self):
		# TAKE: the player is planning to use a selected card to take cards on the table
		# selected card's sum is more than can be taken OR there is a card with the same value as the selected one
		if self.table_cards.selected_cards_sum > self.player1.selected_card.number \
			or self.player1.selected_card.number in [card.number for card in self.table_cards.cards] \
			and [card.number for card in self.table_cards.cards if card.active][0] != self.player1.selected_card.number:
			self.move_type = "invalid-take"
		# selected card's sum is less than required to take them with the selected card
		elif self.table_cards.selected_cards_sum < self.player1.selected_card.number:
			self.move_type = "incomplete-take"
		# selected card's sum has the same value of selected card
		elif self.table_cards.selected_cards_sum == self.player1.selected_card.number:
			self.move_type = "valid-take"
		print(f"Mode: {self.mode} | Move-Type: {self.move_type}")
	
	def apply_throwing_rules(self):
		# THROW: The player didn't select any card to take therefore he wants to throw the card on the table
		# there are possible ways to perform a valid take. Future update: len(possible_take_moves()) > 0
		if taking_is_possible(self.player1.selected_card.number, [card.number for card in self.table_cards.cards]):
			self.move_type = "invalid-throw"
		else:
			self.move_type = "valid-throw"
		print(f"Mode: {self.mode} | Move-Type: {self.move_type} | Table: {[card.number for card in self.table_cards.cards]}")
	
	def highlight_hovered_card(self, coo_mouse: (int, int)):
		self.player1.highlight_hovered_card(coo_mouse)
		self.table_cards.highlight_hovered_card(coo_mouse)
	
	def start(self):
		# 1- animation of the cards going to the table: move from deck to table (face down) and the get facing up
		self.table_cards.cards = self.deck.draw_cards("table")  # put the cards on the table
		self.game_loop()  # starting the actual game
