from typing import Optional

# type: ignore
from pygame import Surface, mouse, key, time
# type: ignore
from pygame.draw import circle

from pygame.locals import *

from scene import Scene
from camera import Camera, Vec2

from math import cos, sin, pi

class Arena(Scene):
	zoom_pow: float
	theta: float

	def __init__(self, screen: Surface):
		self.screen = Camera(screen)

		self.zoom_pow = 0

		self.theta = 0

	def update(self) -> Optional[Scene]:
		# self.screen.zoom = 1 + cos(time.get_ticks() / 500) / 2
		# print(self.screen.get_game_pos(mouse.get_pos()))

		keys = key.get_pressed()

		# Update zoom if zoom keys are pressed
		if keys[K_PLUS] or keys[K_EQUALS]:
			self.zoom_pow += 0.1
			self.screen.zoom = 2 ** self.zoom_pow
		elif keys[K_MINUS] or keys[K_UNDERSCORE]:
			self.zoom_pow -= 0.1
			self.screen.zoom = 2 ** self.zoom_pow

		# Update the position
		vec = Vec2(0, 0)
		if keys[K_RIGHT]: 	vec += Vec2( 1,  0)
		if keys[K_LEFT]: 	vec += Vec2(-1,  0)
		if keys[K_UP]: 		vec += Vec2( 0,  1)
		if keys[K_DOWN]: 	vec += Vec2( 0, -1)

		vec.set_length(0.05 * (2 ** -self.zoom_pow))

		self.screen.pos += vec

		# Update the circle position
		self.theta = (time.get_ticks() / 500) % (2 * pi)

		pass

	def draw(self):
		# (w, h) = self.screen.get_size()
		self.screen.rect((255, 255, 255), Vec2(0.1, 0.1), Vec2(0.1, 0.2))

		# p = self.screen.get_game_pos(mouse.get_pos())
		p = Vec2(0.5, 0.5) + Vec2(cos(self.theta), sin(self.theta)) * 0.25

		self.screen.circle((255, 0, 0), p, 0.05)