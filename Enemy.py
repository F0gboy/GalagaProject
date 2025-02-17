from Components import Component
import random
import pygame
class Enemy(Component):

    def awake(self, game_world):
        sr = self.gameObject.get_component("SpriteRenderer")

        random_x = random.randint(0, game_world.screen.get_width()-sr.sprite_image.get_width())
        self._screen_size = pygame.math.Vector2(game_world._screen.get_width(), game_world._screen.get_height())
        self.gameObject.transform.position = pygame.math.Vector2(random_x,0)

    def start(self):
        pass

    def update(self, delta_time):
        speed = 0
        movement = pygame.math.Vector2(0,speed)

        self._gameObject.transform.translate(movement*delta_time)
        bottom_limit = self._screen_size.y
        if self._gameObject.transform.position.y > bottom_limit:
            self._gameObject.destroy()

