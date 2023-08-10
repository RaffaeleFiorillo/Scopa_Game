import pygame
from random import uniform, randint


class FireParticle:
	def __init__(self, position, velocity):
		self.position = position
		self.velocity = velocity
		self.color = (randint(200, 255), randint(0, 100), 0)
	
	def update(self, dt):
		self.position[0] += self.velocity[0] * dt
		self.position[1] += self.velocity[1] * dt
	
	def draw(self, screen):
		pygame.draw.circle(screen, self.color, (int(self.position[0]), int(self.position[1])), 3)


class FireParticleManager:
	def __init__(self, position, num_particles=30):
		self.position = position
		self.particles = [FireParticle(self.position, [uniform(-30, 30), uniform(-30, 30)]) for _ in range(num_particles)]
	
	def update(self, dt):
		for particle in self.particles:
			particle.update(dt)
	
	def draw(self, screen):
		for particle in self.particles:
			particle.draw(screen)
