from src.Game.Entities import Deck, Human, AI, TableCards
from src.Game.scopa_functions import taking_is_possible, get_move_points
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
		self.mouse_position: (int, int) = (0, 0)  # coordinates of the mouse  inside the game's screen
		self.clock = clock
		self.dt = 0
		self.screen = screen
		
		# the mode says if the player is "choosing" (the card to play), "taking" (cards on the table) or "waiting"
		# (the other player to make a move)
		self.mode: str = "choice"
		
		# how the player uses one of his cards: take (take cards on the table); throw (put it on the table)
		self.move_type: str = ""
		# incomplete (cards are missing), valid, invalid, point (move makes 1 point), points (move makes >= 2 points)
		self.move_effect = "incomplete"
		# incomplete-take, invalid-take, invalid-throw
		self.error_code: str = ""
	
	# play_animation(self.screen, "choosing_player")
	
	# INPUT HANDLING ---------------------------------------------------------------------------------------------------
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
				
	def manage_keyboard_events(self):
		if self.move_type == "take":  # if possible, the player must play to take
			if self.move_effect == "valid" or self.move_effect[:5] == "point":
				self.player1.take_cards(self.table_cards.pop_selected_cards())
				self.mode = "choice"  # should be "waiting"
			elif self.move_effect == "incomplete":
				pass  # make some error noise and show the user why
			elif self.move_effect == "invalid":  # if unable to take, the card is thrown on the table
				pass  # make some error noise and show the user why
		elif self.move_type == "throw":
			if self.move_effect == "valid":
				self.table_cards.receive_card(self.player1.pop_selected_card())
				self.mode = "choice"  # should be "waiting"
			elif self.move_effect == "invalid":
				pass  # make some error noise and show the user why
	
	# AUXILIARY --------------------------------------------------------------------------------------------------------
	def give_cards(self):
		# 1- animation of player 1 getting his cards into his hands
		self.player1.cards_in_hand = self.deck.draw_cards("player")
		# 2- animation of player 2 getting his cards into his hands
		self.player2.cards_in_hand = self.deck.draw_cards("player")
	
	# RULES ------------------------------------------------------------------------------------------------------------
	def apply_taking_rules(self):
		self.move_type = "take"
		# TAKE: the player is planning to use a selected card to take cards on the table
		# selected card's sum is more than can be taken OR there is a card with the same value as the selected one
		if self.table_cards.selected_cards_sum > self.player1.selected_card.number \
			or self.player1.selected_card.number in [card.number for card in self.table_cards.cards] \
			and [card.number for card in self.table_cards.cards if card.active][0] != self.player1.selected_card.number:
			self.move_effect = "invalid"
		# selected card's sum is less than required to take them with the selected card
		elif self.table_cards.selected_cards_sum < self.player1.selected_card.number:
			self.move_effect = "incomplete"
		# selected card's sum has the same value of selected card
		elif self.table_cards.selected_cards_sum == self.player1.selected_card.number:
			points = get_move_points(self.player1.selected_card, self.table_cards.cards)
			if points == 0:
				self.move_effect = "valid"
			elif points == 1:
				self.move_effect = "point"
			else:
				self.move_effect = "points"
		# print(f"Mode: {self.mode} | Move-Type: {self.move_type} | Card-Effect: {self.move_effect}")
	
	def apply_throwing_rules(self):
		self.move_type = "throw"
		# THROW: The player didn't select any card to take therefore he wants to throw the card on the table
		# there are possible ways to perform a valid take. Future update: len(possible_take_moves()) > 0
		if taking_is_possible(self.player1.selected_card.number, [card.number for card in self.table_cards.cards]):
			self.move_effect = "invalid"
		else:
			self.move_effect = "valid"
		# print(f"Mode: {self.mode} | Move-Type: {self.move_type} | Move-Effect: {self.move_effect}")
		
	# MAIN FUNCTIONS ---------------------------------------------------------------------------------------------------
	def start(self):
		# 1- animation of the cards going to the table: move from deck to table (face down) and the get facing up
		self.table_cards.cards = self.deck.draw_cards("table")  # put the cards on the table
		self.game_loop()  # starting the actual game
	
	def game_loop(self):
		match_is_on, rounds_left = True, 6
		while match_is_on:
			if not (len(self.player1.cards_in_hand) and len(self.player2.cards_in_hand)) and rounds_left > 1:
				self.give_cards()
				rounds_left -= 1
				match_is_on = rounds_left >= 0  # if there are no more cards in the deck the match is over
			
			# handling input
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					exit()
				elif self.mode != "wait":  # the player is only allowed to play on its turn
					if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
						self.manage_mouse_events(self.mouse_position)
					elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN and self.player1.selected_card:
						self.manage_keyboard_events()
			
			self.update()
			self.refresh()
			self.dt = self.clock.tick(FPS) / 1000
		self.end_of_match()
		
	def update(self):
		self.mouse_position = pygame.mouse.get_pos()  # avoid multiples execution of the same function
		self.table_cards.update(self.dt, self.move_effect, self.mouse_position)  # update the cards on the table
		self.player1.update(self.dt, self.move_effect, self.mouse_position)  # update player cards
		self.player2.update(self.dt)  # update player2
	
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
