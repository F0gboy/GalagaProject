import pygame
import random
from gameObject import GameObject
from component import Animator, SpriteRenderer, Collider
from player import Player
from builder import PlayerBuilder, EnemyBuilder, MenuBuilder
from soundManager import SoundManager
from enemy import Enemy

class GameWorld:

    def __init__(self) -> None:
        pygame.init()

        self._gameObjects = []
        self._colliders = []
        self._timers = []  # List to keep track of timers
        self._screen = pygame.display.set_mode((720, 720))
        self._running = True
        self._clock = pygame.time.Clock()
        self._attack_interval = 1  # seconds
        self._time_since_last_attack = 0
        self._attack_cooldown = 1  # seconds between each enemy attack
        self._time_since_last_enemy_attack = 0
        self._shared_time = 0
        self._startGame = False
        self._options_started = False
        self._clock = pygame.time.Clock()
        self.sound_manager = SoundManager()
        self._running = True
        self._options_started = False
        self._current_music = None
        self._level = 1
        
        self.menu = MenuBuilder() \
            .add_button("Start", (self._screen.get_width() / 2 - 100, 200), (200, 50), (255, 255, 255), lambda: self.start_game()) \
            .add_button("Options", (self._screen.get_width() / 2 - 100, 300), (200, 50), (255, 255, 255), lambda: self.show_options()) \
            .add_button("Quit", (self._screen.get_width() / 2 - 100, 400), (200, 50), (255, 255, 255), lambda: self.quit_game()) \
            .build()

        self.options_menu = MenuBuilder() \
            .add_button("Volume +", (self._screen.get_width() / 2 - 100, 250), (200, 50), (255, 255, 255), lambda: self.sound_manager.increase_volume()) \
            .add_button("Volume -", (self._screen.get_width() / 2 - 100, 350), (200, 50), (255, 255, 255), lambda: self.sound_manager.decrease_volume()) \
            .add_button("Back", (self._screen.get_width() / 2 - 100, 450), (200, 50), (255, 255, 255), lambda: self.back_to_menu()) \
            .build()

    def awake(self):
        for game_object in self._gameObjects:
            game_object.awake(self)

    def start_game(self):
        self.reset_scene()
        # Build and instantiate the player so that its components get a reference to game_world
        builder = PlayerBuilder()
        builder.build()
        self.instantiate(builder.get_gameObject())

        if self._level == 1:
            self._enemy_builder = EnemyBuilder()
            self._enemy_builder.build_wave("enemy_01.png", pygame.math.Vector2(65, 200), 26, size=(35, 35), screen_width=self.screen.get_size()[0])
            for enemy in self._enemy_builder.get_gameObject_list():
                self.instantiate(enemy)

            self._enemy_builder2 = EnemyBuilder()
            self._enemy_builder2.build_wave("enemy_02.png", pygame.math.Vector2(58, 150), 12, size=(40, 40), screen_width=self.screen.get_size()[0])
            for enemy in self._enemy_builder2.get_gameObject_list():
                self.instantiate(enemy)

            self._enemy_builder3 = EnemyBuilder()
            self._enemy_builder3.build_wave("enemy_03.png", pygame.math.Vector2(65, 90), 9, size=(55, 55), screen_width=self.screen.get_size()[0])
            for enemy in self._enemy_builder3.get_gameObject_list():
                self.instantiate(enemy)


        if self._level == 2:
            self._enemy_builder = EnemyBuilder()
            self._enemy_builder.build_wave("enemy_02.png", pygame.math.Vector2(65, 200), 96, size=(15, 15), screen_width=self.screen.get_size()[0])
            for enemy in self._enemy_builder.get_gameObject_list():
                self.instantiate(enemy)

            self._enemy_builder3 = EnemyBuilder()
            self._enemy_builder3.build_wave("enemy_03.png", pygame.math.Vector2(75, 90), 6, size=(85, 85), screen_width=self.screen.get_size()[0])
            for enemy in self._enemy_builder3.get_gameObject_list():
                self.instantiate(enemy)


        if self._level == 3:
            self._enemy_builder = EnemyBuilder()
            self._enemy_builder.build_wave("enemy_01.png", pygame.math.Vector2(65, 75), 26, size=(35, 35), screen_width=self.screen.get_size()[0])
            for enemy in self._enemy_builder.get_gameObject_list():
                self.instantiate(enemy)

            self._enemy_builder2 = EnemyBuilder()
            self._enemy_builder2.build_wave("enemy_02.png", pygame.math.Vector2(58, 250), 24, size=(40, 40), screen_width=self.screen.get_size()[0])
            for enemy in self._enemy_builder2.get_gameObject_list():
                self.instantiate(enemy)

            self._enemy_builder3 = EnemyBuilder()
            self._enemy_builder3.build_wave("enemy_03.png", pygame.math.Vector2(75, 350), 6, size=(85, 85), screen_width=self.screen.get_size()[0])
            for enemy in self._enemy_builder3.get_gameObject_list():
                self.instantiate(enemy)

        self._startGame = True

    def start(self):
        for game_object in self._gameObjects:
            game_object.start()

    def instantiate(self, game_object):
        self._gameObjects.append(game_object)
        game_object.awake(self)
        game_object.start()

    def destroy(self, game_object):
        if game_object in self._gameObjects:
            self._gameObjects.remove(game_object)
            collider = game_object.get_component("Collider")
            if collider and collider in self._colliders:
                self._colliders.remove(collider)
            game_object.destroy()  # Ensure the game object is marked as destroyed

    def reset_scene(self):
        self._gameObjects.clear()
        self._colliders.clear()
        self._timers.clear()
        self._time_since_last_attack = 0
        self._shared_time = 0
        self._attack_interval = 1  # Reset attack interval

    def trigger_attack(self):
        # Get all enemies that are not destroyed
        self._front_row_enemies = [enemy for enemy in self._gameObjects if isinstance(enemy.get_component("Enemy"), Enemy) and not enemy.is_destroyed]

        if self._front_row_enemies:
            enemy = random.choice(self._front_row_enemies)
            enemy.get_component("Enemy").start_attack()

        # Adjust the attack interval based on the number of remaining enemies
        remaining_enemies = len(self._front_row_enemies)
        if remaining_enemies > 0:
            self._attack_interval = max(0.5, 1.0 / remaining_enemies)

    def start_timer(self, delay, callback):
        event_id = pygame.USEREVENT + len(self._timers)
        pygame.time.set_timer(event_id, int(delay * 1000))
        self._timers.append((event_id, callback))

    def quit_game(self):
        self._running = False

    def show_options(self):
        self._options_started = True

    def back_to_menu(self):
        self._options_started = False

    def handle_timers(self):
        for event in pygame.event.get():
            if event.type >= pygame.USEREVENT:
                for timer in self._timers:
                    if event.type == timer[0]:
                        timer[1]()
                        pygame.time.set_timer(event.type, 0)  # Stop the timer

    @property
    def screen(self):
        return self._screen
    
    @property
    def colliders(self):
        return self._colliders

    def update(self, delta_time):
        self._time_since_last_attack += delta_time
        self._shared_time += delta_time

        if self._startGame:
            if self._time_since_last_attack >= self._attack_interval:
                self.trigger_attack()
                self._time_since_last_attack = 0

            # Check if all enemies are destroyed to progress to the next level
            if not any(isinstance(obj.get_component("Enemy"), Enemy) and not obj.is_destroyed for obj in self._gameObjects):
                self._level += 1
                self.start_game()

        for game_object in self._gameObjects:
            game_object.update(delta_time)

        self.handle_timers()  # Handle timer events