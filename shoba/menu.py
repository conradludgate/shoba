from typing import Optional

# type: ignore
from pygame import Surface, mouse
# type: ignore
from pygame.draw import circle

from scene import Scene

from arena import Arena

class Menu(Scene):
	radius: int
	def __init__(self, screen: Surface):
		self.radius = 200
		self.screen = screen

	def update(self) -> Optional[Scene]:
		(x, y) = mouse.get_pos()
		(w, h) = self.screen.get_size()
		if (w // 2 - x) ** 2 + (h // 2 - y) ** 2 < self.radius ** 2:
			self.radius = 220
		else:
			self.radius = 200

		(x, _, _) = mouse.get_pressed()
		if x and self.radius == 220:
			return Arena(self.screen)

	def draw(self):
		(w, h) = self.screen.get_size()

		circle(self.screen, (255, 0, 0), (w // 2, h // 2), self.radius)