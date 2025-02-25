import pygame
import random
from gameObject import GameObject
from component import Animator
from component import SpriteRenderer
from player import Player
from builder import PlayerBuilder
from builder import EnemyBuilder

class GameWorld:

    def __init__(self) -> None:
        pygame.init()

        screen_size = (720, 720)
        self._gameObjects = []
        self._colliders = []
        self.score = 0  # Score system
        self.font = pygame.font.Font(None, 48)  # Larger font for better visibility

        builder = PlayerBuilder()
        builder.build()
        self._gameObjects.append(builder.get_gameObject())

        self._enemy_builder = EnemyBuilder()
        self._enemy_builder.build_wave("enemy_01.png", pygame.math.Vector2(65, 200), 26, size=(35, 35),
                                       screen_width=screen_size[0])
        self._gameObjects.extend(self._enemy_builder.get_gameObject_list())

        self._enemy_builder2 = EnemyBuilder()
        self._enemy_builder2.build_wave("enemy_02.png", pygame.math.Vector2(58, 150), 12, size=(40, 40),
                                        screen_width=screen_size[0])
        self._gameObjects.extend(self._enemy_builder2.get_gameObject_list())

        self._enemy_builder3 = EnemyBuilder()
        self._enemy_builder3.build_wave("enemy_03.png", pygame.math.Vector2(65, 90), 9, size=(55, 55),
                                        screen_width=screen_size[0])
        self._gameObjects.extend(self._enemy_builder3.get_gameObject_list())

        self._screen = pygame.display.set_mode(screen_size)
        self._running = True
        self._clock = pygame.time.Clock()
        self._attack_interval = 1  # seconds
        self._time_since_last_attack = 0
        self._attack_cooldown = 1  # seconds between each enemy attack
        self._time_since_last_enemy_attack = 0
        self._front_row_enemies = self._enemy_builder.get_front_row_enemies()
        self._shared_time = 0

    def awake(self):
        for game_object in self._gameObjects:
            game_object.awake(self)

    def start(self):
        for game_object in self._gameObjects:
            game_object.start()

    def instantiate(self, game_object):
        self._gameObjects.append(game_object)
        game_object.awake(self)
        game_object.start()

    def trigger_attack(self):
        if self._front_row_enemies:
            enemy = random.choice(self._front_row_enemies)
            enemy.get_component("Enemy").start_attack()

    @property
    def screen(self):
        return self._screen

    @property
    def colliders(self):
        return self._colliders

    def increase_score(self):
        self.score += 100
        print(f"Score: {self.score}")

    def draw_score(self):
        score_surface = self.font.render(f"Score: {self.score}", True, (255, 255, 255))
        self._screen.blit(score_surface, (20, 20))  # Draw score at top-left corner with padding

    def update(self, delta_time):
        self._time_since_last_attack += delta_time
        self._time_since_last_enemy_attack += delta_time
        self._shared_time += delta_time

        if self._time_since_last_attack >= self._attack_interval:
            if self._time_since_last_enemy_attack >= self._attack_cooldown:
                self.trigger_attack()
                self._time_since_last_enemy_attack = 0
            self._time_since_last_attack = 0

        # Opdater alle game objects
        for game_object in self._gameObjects[:]:
            enemy_component = game_object.get_component("Enemy")
            if enemy_component and hasattr(enemy_component, "is_alive") and not enemy_component.is_alive():
                self.increase_score()
                self._gameObjects.remove(game_object)
            else:
                game_object.update(delta_time)

        # 🔥 1. Ryd skærmen 🔥
        self._screen.fill((0, 0, 0))

        # 🔥 2. Tegn alle game objects 🔥
        for game_object in self._gameObjects:
            sprite_renderer = game_object.get_component("SpriteRenderer")
            if sprite_renderer:
                sprite_renderer.update(delta_time)  # 🚀 Opdater sprite
                if hasattr(sprite_renderer, "image") and hasattr(sprite_renderer, "position"):
                    self._screen.blit(sprite_renderer.image, sprite_renderer.position)  # 🔥 Tegn sprite

        # 🔥 3. Tegn scoren 🔥
        self.draw_score()

        # 🔥 4. Opdater skærmen 🔥
        pygame.display.update()  # Opdater én gang efter alt er tegnet
