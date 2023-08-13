from src.Animations.AI_Player.Base import PlayerAnimation


class ThrowAnimation(PlayerAnimation):
	def __init__(self):
		super().__init__()
	
	def reset(self):
		pass
	
	def update(self, dt, cards):
		super().update(dt, cards)
	
	def draw(self, screen):
		pass
