from src.Game.Entities.Cards.Card import Card


class TableCards:
	def __init__(self):
		self.cards: [Card] = []
		self.available_indexes = []  # indexes, ordered by priority, of where to put the cards (avoids stacking them)
		self.selected_cards_sum = 0

	# removes all the selected cards on the table and returns them
	def take_selected_cards(self):
		cards_to_take = []
		for i, card in enumerate(self.cards[::]):
			if card.active:
				cards_to_take.append(self.cards.pop(i))
		return cards_to_take

	def activate_clicked_card(self, mouse_position):
		for card in self.cards:
			if card.mouse_is_inside(mouse_position):
				card_was_activated = not card.active  # reverts the state of the card to its opposite
				if card_was_activated:
					self.selected_cards_sum += card.number
				else:
					self.selected_cards_sum -= card.number
				card.active = card_was_activated
				return card_was_activated
		return False  # if it reaches this point, no card was activated
	
	def disable_all_cards(self):
		for card in self.cards:
			card.active = False
		self.selected_cards_sum = 0

	def highlight_hovered_card(self, mouse_position):
		for card in self.cards:
			card.hoovered = card.mouse_is_inside(mouse_position)

	def receive_card(self, card):
		# 1- order: define where to put the card and removing that position's availability
		# 2- update the appearance and location of the card
		order = self.available_indexes.pop(0) if len(self.available_indexes) else len(self.cards)
		card.load_card("table", order)  # update the appearance and location of the card
		self.cards.append(card)  # include the card on the table

	def pop_selected_cards(self):
		cards, deleted_number = [], 0
		range_number = len(self.cards)  # we want this to be a fixed value to avoid issues when using .pop()
		for i in range(range_number):
			if self.cards[i-deleted_number].active:
				self.available_indexes.append(self.cards[i-deleted_number].order)  # new available place to put a card
				cards.append(self.cards.pop(i - deleted_number))
				deleted_number += 1
		return cards

	def update(self, dt, color_code, mouse_position):
		for card in self.cards:
			card.hoovered = card.mouse_is_inside(mouse_position)
			if card.active:
				card.update(dt, color_code)
		
	def draw(self, screen):
		[card.draw(screen) for card in self.cards]
