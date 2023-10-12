import pygame
import time

screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)

class Cargo:
	def __init__(self, x, y, speedx, speedy, mass, static = False):
		self.x = x
		self.y = y

		self.speedx = speedx
		self.speedy = speedy

		self.static = static

		self.mass = mass or 1
		self.links = []

	def add_link(self, cargo):
		self.links.append(cargo)
		cargo.links.append(self)

class Simulation:
	def __init__(self):
		self.enable = False
		self.screen_mode = False
		self.w = 0
		self.h = 0

		self.speed = 0.1
		self.frame_rate = 100

		self.start_speed = 200
		
		self.frame_time = 1 / self.frame_rate
		self.count = 350
		self.size = 5

		self.usex = False
		self.usey = True

		self.change_screen_mode()

		self.def_x = 0
		self.def_y = self.h // 2	

		self.generate_cargos()

	def generate_cargos(self):
		self.cargos = [Cargo(
			self.def_x + i * self.dist, self.def_y, # Start pos
			0, -self.start_speed if i < 5 else 0, # Start speed
			10 if i < 10 else 1 # Mass
			) for i in range(self.count)]

		self.cargos[0].static = True
		self.cargos[-1].static = False

		for cargo1, cargo2 in zip(self.cargos[:-1], self.cargos[1:]):
			cargo1.add_link(cargo2)

	def change_screen_mode(self):
		if not self.screen_mode:
			self.screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
		else:
			self.screen = pygame.display.set_mode((1440, 900))

		self.screen_mode = not self.screen_mode
		self.w = screen.get_width()
		self.h = screen.get_height()
		pygame.display.set_caption('SpringPy')
		self.dist = self.w / (self.count - 1)

	def start(self):
		self.enable = True
		while self.enable:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					quit()

				if event.type == pygame.KEYDOWN:
					if event.unicode.lower() == "f":
						self.change_screen_mode()

			self.screen.fill((0, 0, 0))

			for cargo in self.cargos:
				fx = sum([link.x for link in cargo.links]) / len(cargo.links)
				fy = sum([link.y for link in cargo.links]) / len(cargo.links)

				cargo.speedx += (fx - cargo.x) / cargo.mass
				cargo.speedy += (fy - cargo.y) / cargo.mass

			for cargo in self.cargos:
				if not cargo.static:
					if self.usex: cargo.x += cargo.speedx * self.speed
					if self.usey: cargo.y += cargo.speedy * self.speed
			
				pygame.draw.rect(self.screen, (200, 200, 200), (cargo.x - self.size // 2, cargo.y - self.size // 2, self.size, self.size))

			pygame.display.flip()
			time.sleep(self.frame_time)

if __name__ == "__main__":
	sim = Simulation()
	sim.start()