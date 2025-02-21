from component import Components
import pygame
import math

class Enemy(Components):
    def __init__(self, speed=300, attack_frequency=0.5):
        super().__init__()
        self._movement_speed = speed  # pixels per second
        self._movement_frequency = attack_frequency  # oscillations per second

    def awake(self, game_world):
        sr = self.gameObject.get_component("SpriteRenderer")
        self._screen_size = pygame.math.Vector2(game_world.screen.get_width(), game_world.screen.get_height())
        self._initial_position = self.gameObject.transform.position.copy()
        self._movement_amplitude = 50  # pixels
        self._game_world = game_world
        self._attacking = False
        self._attack_target = pygame.math.Vector2(game_world._gameObjects[0].transform.position.x, game_world._gameObjects[0].transform.position.y)
        self._attack_phase = 0

    def start(self):
        pass

    def update(self, delta_time):
        if self._attacking:
            if self._attack_phase == 0:
                # Circular movement
                angle = self._game_world._shared_time * 2 * math.pi * self._movement_frequency
                radius = 100
                movement_x = radius * math.cos(angle)
                movement_y = radius * math.sin(angle)
                self.gameObject.transform.position = self._initial_position + pygame.math.Vector2(movement_x, movement_y)
                if self._game_world._shared_time >= 2:
                    self._attack_phase = 1
            elif self._attack_phase == 1:
                # Move towards the player
                direction = (self._attack_target - self.gameObject.transform.position).normalize()
                self.gameObject.transform.translate(direction * self._movement_speed * delta_time)
                if self.gameObject.transform.position.distance_to(self._attack_target) < 10:
                    self._attack_phase = 2
            elif self._attack_phase == 2:
                # Return to original position
                direction = (self._initial_position - self.gameObject.transform.position).normalize()
                self.gameObject.transform.translate(direction * self._movement_speed * delta_time)
                if self.gameObject.transform.position.distance_to(self._initial_position) < 10:
                    self._attacking = False
                    self._attack_phase = 0
        else:
            movement_x = self._movement_amplitude * math.sin(2 * math.pi * self._movement_frequency * self._game_world._shared_time)
            movement = pygame.math.Vector2(movement_x, 0)
            self.gameObject.transform.position = self._initial_position + movement

            bottom_limit = self._screen_size.y
            if self.gameObject.transform.position.y > bottom_limit:
                self.gameObject.destroy()

    def start_attack(self):
        self._attacking = True
        self._attack_target = pygame.math.Vector2(self._gameObject._game_world._gameObjects[0].transform.position.x, self._gameObject._game_world._gameObjects[0].transform.position.y)