from __future__ import annotations

from typing import Tuple

# type: ignore
from pygame import Surface, Rect, Color
from pygame.transform import scale

from pygame.draw import circle, rect

import math

class Vec2:
	x: float
	y: float

	def __init__(self, x: float, y: float):
		self.x = x
		self.y = y

	def __add__(self, other: Vec2) -> Vec2:
		return Vec2(self.x + other.x, self.y + other.y)

	def __sub__(self, other: Vec2) -> Vec2:
		return Vec2(self.x - other.x, self.y - other.y)

	def __mul__(self, scale: float) -> Vec2:
		return Vec2(self.x * scale, self.y * scale)

	def __iadd__(self, other: Vec2):
		self.x += other.x
		self.y += other.y
		return self

	def __isub__(self, other: Vec2):
		self.x -= other.x
		self.y -= other.y
		return self

	def __imul__(self, scale: float):
		self.x *= scale
		self.y *= scale
		return self

	def __str__(self) -> str:
		return "Vec2(x: {0}, y: {1})".format(self.x, self.y)

	@property
	def norm(self) -> float:
		return self.x * self.x + self.y * self.y

	@property
	def length(self):
		return math.sqrt(self.norm)

	def set_length(self, length: float):
		l = self.length
		if l == 0: return

		self *= (length / l)

class Camera(Surface):
	screen: Surface
	
	pos: Vec2
	zoom: float

	def __init__(self, screen: Surface, pos: Vec2 = Vec2(0, 0), zoom: float = 1.0):
		self.screen = screen

		self.pos = pos
		self.zoom = zoom

	def draw(self, s: Surface, p: Vec2):
		# (self.pos - p)
		(width, height) = self.screen.get_size()
		(w, h) = s.get_size()

		# If w = 1, h = 1, zoom = 1, then scale to width, height
		# If w = 0.5, h = 0.5, zoom = 1 then scale to 0.5width, 0.5height
		# If w = 0.5, h = 0.5, zoom = 2, then scale to width, height

		(scale_w, scale_h) = (self.zoom * w, self.zoom * h)
		s = scale(s, (scale_w * width, scale_h * height))

		loc = get_screen_pos(p)

		return self.screen.blit(s, Rect(loc[0], loc[1], 0, 0))

	def blit(source: Surface, dest: Optional[Rect], area=None, special_flags = 0):
		if dest is None:
			return self.draw(source)
		else:
			return self.draw(source, Vec2(dest.x, dest.y))

	def get_game_pos(self, pos: Tuple[int, int]) -> Vec2:
		(w, h) = self.screen.get_size()
		p = Vec2(pos[0] / self.zoom / w, pos[1] / self.zoom / h)
		return p + self.pos

	def get_screen_pos(self, p: Vec2) -> Tuple[int, int]:
		(w, h) = self.screen.get_size()
		location = p - self.pos
		return int(location.x * self.zoom * w), int(location.y * self.zoom * h)

	def get_screen_size(self, size: Vec2):
		(w, h) = self.screen.get_size()
		return Rect(0, 0, size.x * self.zoom * w, size.y * self.zoom * h)

	def circle(self, colour: Color, center: Vec2, radius: float, width: float=0):
		size = self.get_screen_size(Vec2(radius, width))

		# print(self.get_screen_pos(center), int(radius*self.zoom*w), int(width*self.zoom*w))
		circle(self.screen, colour, self.get_screen_pos(center), size.w, size.h)

	def rect(self, colour: Color, pos: Vec2, size: Vec2, width: float=0):
		
		s = self.get_screen_size(size)
		(x, y) = self.get_screen_pos(pos)
		# print("bar", x, y)
		s.move_ip(x, y)

		# print(s)

		size = self.get_screen_size(Vec2(width, 0))

		rect(self.screen, colour, s, size.w)