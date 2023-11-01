from src.Animations.AI_Player.Base import PlayerAnimation


class TakeAnimation(PlayerAnimation):
	def __init__(self):
		super().__init__()
	
	def reset(self):
		pass
	
	def update(self, dt, cards):
		super().update(dt, cards)
	
	def draw(self, screen):
		# screen.blit(self.card_in_hand_image, (480, 150))
		# screen.blit(self.card_in_hand_image, (495, 150))
		# screen.blit(self.card_in_hand_image, (512, 150))
		if len(self.cards_in_hand) == 3:
			screen.blit(self.card_in_hand_image, (510, 150))
			screen.blit(self.card_in_hand_image, (540, 150))
		elif len(self.cards_in_hand) == 2:
			screen.blit(self.card_in_hand_image, (530, 150))
			
