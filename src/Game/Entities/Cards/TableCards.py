from src.Game.Entities.Cards.Card import Card


class TableCards:
	def __init__(self):
		self.cards: [Card] = []
		self.selected_cards_sum = 0

	# removes all the selected cards on the table and returns them
	def take_selected_cards(self):
		cards_to_take = []
		for i, card in enumerate(self.cards[::]):
			if card.active:
				cards_to_take.append(self.cards.pop(i))
		return cards_to_take

	def activate_cards(self, mouse_position):
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

	def draw(self, screen, selected_card):
		if selected_card is None or self.selected_cards_sum < selected_card.number:
			[carta.draw(screen) for carta in self.cards]
		elif self.selected_cards_sum == selected_card.number:
			[carta.draw(screen, (50, 250, 120)) for carta in self.cards]
		else:  # self.selected_cards_sum > selected_card.number
			[carta.draw(screen, (255, 0, 0)) for carta in self.cards]
