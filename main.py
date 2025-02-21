import pygame
from gameWorld import GameWorld

def main():
    game_world = GameWorld()
    game_world.awake()
    game_world.start()

    while game_world._running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_world._running = False

        game_world._clock.tick(60)
        delta_time = game_world._clock.get_time() / 1000.0

        game_world.update(delta_time)

        game_world._screen.fill((0, 0, 0))  # Clear the screen with black
        for game_object in game_world._gameObjects:
            sprite_renderer = game_object.get_component("SpriteRenderer")
            if sprite_renderer:
                sprite_renderer.update(delta_time)

        pygame.display.flip()

if __name__ == "__main__":
    main()