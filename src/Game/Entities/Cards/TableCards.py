from src.Game.Entities.Cards.Card import Card


class TableCards:
	def __init__(self):
		self.cards: [Card] = []

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
				card.active = card_was_activated
				return card_was_activated
		return False  # if it reaches this point, no card was activated

	def disable_all_cards(self):
		for card in self.cards:
			card.active = False

	def highlight_hovered_card(self, mouse_position):
		for card in self.cards:
			card.hoovered = card.mouse_is_inside(mouse_position)

	def draw(self, screen):
		[carta.draw(screen) for carta in self.cards]
