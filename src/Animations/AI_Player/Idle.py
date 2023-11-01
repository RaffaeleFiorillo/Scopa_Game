import pygame.draw

from src.Animations.AI_Player.Base import PlayerAnimation


class IdleAnimation(PlayerAnimation):
	def __init__(self):
		super().__init__()
	
	# when the player has *key* cards the end of the arm (hand position) is drawn at the coordinates *value*
	# remember the mirror effect when viewing the arm's side (left-> right and right -> left)
	right_arm_coo = {0: (520, 188), 1:  (520, 188), 2:  (510, 190), 3:  (500, 192)}
	left_arm_coo = {0: (540, 188), 1: (540, 188), 2:  (550, 190), 3:  (560, 192)}
	
	def reset(self):
		pass
	
	def update(self, dt, cards):
		super().update(dt, cards)
	
	def draw(self, screen):
		super().draw(screen)
		# right arm
		pygame.draw.line(screen, self.body_color, self.right_elbow_coo, self.right_arm_coo[self.len_cards_in_hand], 6)
		# left arm
		pygame.draw.line(screen, self.body_color, self.left_elbow_coo, self.left_arm_coo[self.len_cards_in_hand], 6)
