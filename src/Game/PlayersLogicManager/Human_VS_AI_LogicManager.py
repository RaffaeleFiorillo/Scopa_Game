import pygame
from src.Game.Matches.scopa_functions import taking_is_possible, get_move_points
from src.Game.Entities.Players import AI, Human
from src.Game.PlayersLogicManager.PlayersLogicManager import PlayersManager


# This class Manages how the players make moves in the match. Waiting for their turn, organizing move-states,
# taking points, ... Everything that has to do with the interaction between the player and the game's logic and rules.
class Human_VS_AI_Manager(PlayersManager):
	def __init__(self, table_cards, player1: Human, player2: AI):
		super().__init__(table_cards, player1, player2)
		self.mouse_position: (int, int) = (0, 0)  # coordinates of the mouse  inside the game's screen
		
		# how the player uses one of his cards: take (take cards from the table); throw (put it on the table)
		self.move_type: str = ""
		# incomplete (cards are missing), valid, invalid, point (move makes 1 point), points (move makes >= 2 points)
		self.move_effect = "hover"
		# incomplete-take, invalid-take, invalid-throw
		self.error_code: str = ""
	
	# ----------------------------------------------- RULES ------------------------------------------------------------
	def move_is_invalid(self) -> bool:
		# Condition 1: Selected card's sum is more than can be taken. Ex: player tries to take 7+2 with an 8
		too_much_to_take: bool = self.table_cards.selected_cards_sum > self.player1.selected_card.number
		
		# Condition 2: The player selects a card to play and tries to use it to take via sum,
		# but there is a card with same number on the table. In this case player must take that card.
		card_is_on_table: bool = self.player1.selected_card.number in [card.number for card in self.table_cards.cards]
		correct_card_not_selected: bool = [card.number != self.player1.selected_card.number
		                                   for card in self.table_cards.cards
		                                   if card.active][0]
		same_card_number_is_available_but_not_selected = card_is_on_table and correct_card_not_selected
		
		return too_much_to_take or same_card_number_is_available_but_not_selected
	
	def apply_taking_rules(self) -> None:
		# TAKE: the player is planning to use a selected card to take cards on the table
		self.move_type = "take"
		
		if self.move_is_invalid():
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
	
	def apply_throwing_rules(self) -> None:
		# THROW: The player didn't select any card to take therefore he wants to throw the card on the table
		self.move_type = "throw"
		
		# there are possible ways to perform a valid take. Future update: len(possible_take_moves()) > 0
		if taking_is_possible(self.player1.selected_card.number, [card.number for card in self.table_cards.cards]):
			self.move_effect = "invalid"
		else:
			self.move_effect = "valid"
	
	# ---------------------------------------- PLAYER 1: HUMAN ACTIONS -------------------------------------------------
	
	def manage_player1_input(self) -> None:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				exit()
			elif self.turn == "1":  # the player is only allowed to play on its turn
				if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
					self.manage_mouse_events()
				elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN and self.player1.selected_card:
					self.manage_keyboard_events()
	
	def manage_mouse_events(self):
		# player has chosen a card in his hand
		if (card_index := self.player1.mouse_is_on_card(self.mouse_position)) > -1:
			# changing mode in order to enable the player to take cards on the table
			self.player1.toggle_card(card_index)
			self.table_cards.disable_all_cards()  # cards selected on the table are deselected
			if self.player1.selected_card is None:
				self.player1.state = "choice"
			else:
				self.player1.state = "take"
				self.apply_throwing_rules()  # check if what the user is doing is valid for a throw move
		# [1- create a list of possible moves for the chosen card
		# 2- activate the cards on the table that would be taken using the selected card]
		# player has chosen a card on the table
		elif self.player1.state == "take":
			self.table_cards.activate_clicked_card(self.mouse_position)
			if len([1 for card in self.table_cards.cards if card.active]) == 0:
				self.apply_throwing_rules()
			else:
				self.apply_taking_rules()  # check if what the user is doing is valid for a taking move
	
	def manage_keyboard_events(self):
		if self.move_type == "take":  # if possible, the player must play to take
			if self.move_effect == "valid" or self.move_effect[:5] == "point":
				self.player1.take_cards(self.table_cards.pop_selected_cards())
				self.turn = "2"  # should be "waiting"
			elif self.move_effect == "incomplete":
				pass  # make some error noise and show the user why
			elif self.move_effect == "invalid":  # if unable to take, the card is thrown on the table
				pass  # make some error noise and show the user why
		elif self.move_type == "throw":
			if self.move_effect == "valid":
				self.table_cards.receive_card(self.player1.pop_selected_card())
				self.turn = "2"  # should be "waiting"
			elif self.move_effect == "invalid":
				pass  # make some error noise and show the user why
	
	# ----------------------------------------- PLAYER 1: AI ACTIONS ---------------------------------------------------
	
	def manage_player2_input(self):
		if self.turn != "2":  # AI moves only if it's its turn
			return None
		
		# the AI player should not be waiting anymore since its turn arrived, and should start the process to make his move
		if self.player2.state == "waiting":
			self.player2.set_up_for_thinking()
		# if the process of choosing a move to make has ended, it's time to apply it
		elif self.player2.is_ready_to_make_a_move:
			self.apply_AI_chosen_move()
			self.end_AI_player_turn()
	
	def end_AI_player_turn(self):
		self.player2.end_turn()
		self.turn = "1"
		self.player1.state = "choice"
	
	def apply_AI_chosen_move(self):
		if self.player2.state == "throw":
			self.table_cards.receive_card(self.player2.pop_selected_card())
		elif self.player2.state == "take":
			self.player2.take_cards(self.table_cards.pop_selected_cards())
	
	# ----------------------------------------------- GENERAL ----------------------------------------------------------
	
	def update(self, dt) -> None:
		self.mouse_position = pygame.mouse.get_pos()  # avoid multiples execution of the same function
		self.table_cards.update(dt, self.move_effect, self.mouse_position)  # update table cards
		self.player1.update(dt, self.move_effect, self.mouse_position)      # update player cards
		self.player2.update(dt)  # update player2
