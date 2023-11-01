from src.Game.Entities.Players.Player import Player


class Human(Player):
	def __init__(self, name):
		super().__init__(name, 476)
	
	# returns the index of the card where the mouse is hovering. Returns -1 if no card is being hovered over
	def mouse_is_on_card(self, mouse_position):
		for i, card in enumerate(self.cards_in_hand):
			if card.mouse_is_inside(mouse_position):
				return i
		return -1
	
	# reverts the state of the card to its opposite and deselect all other cards
	def toggle_card(self, card_index):
		for i, card in enumerate(self.cards_in_hand):
			if i == card_index:
				card.active = not card.active
				self.selected_card = card if card.active else None
			else:
				card.active = False
		
	def update(self, dt, color_code, mouse_position):
		for card in self.cards_in_hand:
			card.hoovered = card.mouse_is_inside(mouse_position)
			if card.active:
				card.update(dt, color_code)
	
	def draw(self, screen):
		super(Human, self).draw(screen)
		for i, card in enumerate(self.cards_in_hand):
			card.draw(screen)
