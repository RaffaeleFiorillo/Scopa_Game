import pygame
from random import uniform, randint, choice, randrange


class FireParticle:
	def __init__(self, x, y, max_height):
		self.x = x
		self.y = y
		self.max_height = max_height
		self.color = pygame.Color(randint(255, 255), randint(0, 255), 0)
		self.size = randint(2, 10)
		self.speed = 400//(self.size/5)**2
		self.alpha = 255
		self.is_alive = lambda: self.y > self.max_height
	
	def update(self, dt):
		self.y -= self.speed * dt
		# self.alpha -= int(self.speed * dt)  # Fading effect
		
	def draw(self, screen):
		self.color.a = self.alpha
		pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.size)


class FireEffect:
	def __init__(self, xs, y_interval, max_height=25, num_particles=100):
		self.xs = xs
		self.y_interval = y_interval
		self.max_height = self.y_interval[0] - max_height  # maximum height of the particles relative to the card
		self.particles = []
		self.num_particles = num_particles
		self.generate_particles()
	
	def generate_particles(self):
		particles_number = (self.num_particles-len(self.particles))
		for _ in range(round(particles_number*0.5)):
			particle = FireParticle(choice(self.xs), randint(self.y_interval[0], self.y_interval[1]), self.max_height)
			self.particles.append(particle)
		for _ in range(round(particles_number*0.5)):
			particle = FireParticle(randint(self.xs[0], self.xs[1]), self.y_interval[0], self.max_height)
			self.particles.append(particle)
	
	def update(self, dt):
		for particle in self.particles:
			particle.update(dt)
		
		self.particles = [particle for particle in self.particles if particle.is_alive()]
		if len(self.particles) < self.num_particles:
			self.generate_particles()
	
	def draw(self, screen):
		for particle in self.particles:
			particle.draw(screen)
