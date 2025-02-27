from component import Components
from gameObject import GameObject
from component import Boss_Laser
from component import SpriteRenderer
from component import Collider
import random
import pygame

class BossEnemy(Components):
    def awake(self, game_world):
        sr = self.gameObject.get_component("SpriteRenderer")
        self._screen_size = pygame.math.Vector2(game_world.screen.get_width(), game_world.screen.get_height())
        self._sprite_size = pygame.math.Vector2(sr.sprite_image.get_width(), sr.sprite_image.get_height())
        self._game_world = game_world

        self.shoot_sound = pygame.mixer.Sound("assets/shoot.mp3")
        self.reload_sound = pygame.mixer.Sound("assets/reload_2.mp3")
        # Set starting position
        self.random_x = random.randint(0, int(self._screen_size.x))
        self.random_y = random.randint(50, min(200, int(self._screen_size.y)))
        self.gameObject.transform.position = pygame.math.Vector2(self.random_x, self.random_y)

        # Timing for shooting
        self.time_since_last_shot = 0
        self.reload_time = 1.0  # Reload time in seconds
        self.is_reloading = False 

        self.shoot_timer = 0  # Counts how long the boss has been shooting
        self.reload_interval = 2  # Reload interval

        # Movement target
        self.target_x = self.random_x
        self.target_y = self.random_y

        self._lives = 10
        
        collider = self.gameObject.get_component("Collider")
        collider.subscribe("collision_enter", self.on_collision_enter)
        
        self.gameObject.tag = "BossEnemy"

    def start(self):
        pass

    def update(self, delta_time):
        speed = 350
        self.time_since_last_shot += delta_time
        self.shoot_timer += delta_time
        # Calculate direction toward target
        direction = pygame.math.Vector2(self.target_x, self.target_y) - self.gameObject.transform.position
        if direction.length() < 10:
            self.target_x = random.randint(0, int(self._screen_size.x))
            self.target_y = random.randint(50, min(200, int(self._screen_size.y)))
        if direction.length() > 0:
            direction = direction.normalize() * speed * delta_time
            self.gameObject.transform.translate(direction)
        # Reload mechanism
        if self.is_reloading:
            self.reload_timer -= delta_time
            self.reload_sound.play()
            if self.reload_timer <= 0:
                self.is_reloading = False
                self.shoot_timer = 0
        else:
            if self.shoot_timer >= self.reload_interval:
                self.is_reloading = True
                self.reload_timer = self.reload_time
            elif self.time_since_last_shot >= 0.8:
                self.shoot(delta_time)
                self.time_since_last_shot = 0

    def shoot(self, delta_time):
        projectile = GameObject(None)
        sr = projectile.add_component(SpriteRenderer("laser.png"))
        projectile.add_component(Boss_Laser())
        projectile.add_component(Collider())  # Ensure collision detection
        projectile.tag = "EnemyLaser"  # Tag it as an enemy laser
        projectile_position = pygame.math.Vector2(
            self._gameObject.transform.position.x + (self._sprite_size.x / 2) - sr.sprite_image.get_width() / 2,
            self._gameObject.transform.position.y + 120
        )
        projectile.transform.position = projectile_position
        self._game_world.instantiate(projectile)
        self.shoot_sound.play()

    def on_collision_enter(self, other):
        if other.gameObject.tag == "Laser":
            self._lives -= 1
            self._game_world.destroy(other.gameObject)
            if self._lives <= 0:
                self._game_world.destroy(self.gameObject)
