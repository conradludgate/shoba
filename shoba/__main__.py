import sys

# type: ignore
import pygame
from pygame.locals import *

from scene import Scene
from menu import Menu

def main():
	# initialize the pygame module
	pygame.init()
	pygame.display.set_caption("Shoba")

	# Set display size to square, 80% of max size
	info = pygame.display.Info()
	size = int(min(info.current_w, info.current_h) * 0.8)
	
	screen = pygame.display.set_mode((size, size))
	
	# define variables to control and time the main loop
	running: bool = True
	clock = pygame.time.Clock()

	# Game state
	scene: Scene = Menu(screen)

	# main loop
	while running:
		for event in pygame.event.get():
			if event.type == QUIT: sys.exit()

		screen.fill(0)

		# Primitive draw update loop. Should separate them
		# Eventually have 3 loops, draw, update and network

		new_scene = scene.update()
		if new_scene is not None:
			scene = new_scene

		scene.draw()
		pygame.display.update()

		clock.tick(30)


if __name__ == "__main__":
	main()


