import pygame
from random import randint, choice


class FireParticle:
	def __init__(self, x, y, max_height):
		self.x: int = x
		self.y: int = y
		self.max_height: int = max_height
		self.color = pygame.Color(randint(255, 255), randint(0, 255), 0)
		self.size: (int, int) = randint(2, 10)
		self.speed: int = round(400/(self.size/5)**2)
		self.is_alive = lambda: self.y > self.max_height
	
	def update(self, dt):
		self.y -= self.speed * dt
		# self.alpha -= int(self.speed * dt)  # Fading effect
		
	def draw(self, screen):
		pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.size)


class FireEffect:
	def __init__(self, xs, ys, max_height=25, num_particles=100):
		self.xs: [int, int] = xs  # interval of the x-axis where the particles can appear
		self.ys: [int, int] = ys  # interval of the y-axis where the particles can appear
		self.max_height = self.ys[0] - max_height  # maximum height of the particles relative to the card
		self.particles = []  # all the particles for this effect
		self.num_particles = num_particles  # the number of particles of this effect
		self.generate_particles()
	
	def generate_particles(self):
		particles_number = (self.num_particles-len(self.particles))
		for _ in range(round(particles_number*0.5)):  # display lateral particles (50% of total particles)
			particle = FireParticle(choice(self.xs), randint(self.ys[0], self.ys[1]), self.max_height)
			self.particles.append(particle)
		for _ in range(round(particles_number*0.5)):  # display top particles (50% of total particles)
			particle = FireParticle(randint(self.xs[0], self.xs[1]), self.ys[0], self.max_height)
			self.particles.append(particle)
	
	def update(self, dt):
		for particle in self.particles:
			particle.update(dt)
		# make sure new particles are created every time old particles "die"
		self.particles = [particle for particle in self.particles if particle.is_alive()]
		if len(self.particles) < self.num_particles:
			self.generate_particles()
	
	def draw(self, screen):
		for particle in self.particles:
			particle.draw(screen)
