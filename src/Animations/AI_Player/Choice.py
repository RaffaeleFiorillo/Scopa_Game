from pygame import draw
from src.Animations.AI_Player.Base import PlayerAnimation
from pygame.image import load


class ChoiceAnimation(PlayerAnimation):
	def __init__(self):
		super().__init__()
		self.thinking_balloon_image = load("assets/AI_Player/thinking/thinking_balloon.png").convert_alpha()
		self.math_symbols_images = [load(f"assets/AI_Player/thinking/symbol{i}.png").convert_alpha() for i in range(1, 13)]
		self.math_symbol_index = 0  # the number of dots to be displayed inside the balloon image
	
	def reset(self):
		pass
	
	def update(self, dt, cards):
		super().update(dt, cards)
		self.math_symbol_index = (self.math_symbol_index + 4*dt) % 11  # when reaching 12 it starts over
	
	def draw(self, screen):
		screen.blit(self.thinking_balloon_image, (605, 51))
		screen.blit(self.math_symbols_images[round(self.math_symbol_index)], (680, 110))
		super().draw(screen)
