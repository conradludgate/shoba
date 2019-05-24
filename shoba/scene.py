from __future__ import annotations

from typing import Optional

# type: ignore
from pygame import Surface

class Scene:
	screen: Surface

	@classmethod
	def update(self) -> Optional[Scene]:
		pass

	def draw(self, screen: Surface):
		pass
