from abc import ABC
from component import Components
import pygame
from gameObject import GameObject
from component import Laser, Collider
from component import SpriteRenderer

class Player(Components, ABC):

    def __init__(self):
        super().__init__()
        self.lives = 3
        self.invincible = False
        self._time_since_last_shot = 1
        self._shoot_delay = 0.1
        self._game_world = None
        self._screen_size = None
        self._sprite_size = None
        self.shoot_sound = None

    def awake(self, game_world):
        self._game_world = game_world
        sr = self._gameObject.get_component("SpriteRenderer")
        self._screen_size = pygame.math.Vector2(game_world.screen.get_width(), game_world.screen.get_height())
        self._sprite_size = pygame.math.Vector2(20, 20)
        # Position the player based on the desired size
        self._gameObject.transform.position.x = (self._screen_size.x / 2) - (self._sprite_size.x / 2)
        self._gameObject.transform.position.y = 600
        
        # Update the sprite's rect from the transform
        sr._sprite.rect.topleft = self._gameObject.transform.position
        
        # Manually adjust the collider bounds if needed:
        collider = self._gameObject.get_component("Collider")
        # For example, if the visible area is shifted 5 pixels to the right:
        custom_rect = sr._sprite.rect.copy()
        custom_rect.x += 5   # adjust this offset as needed
        custom_rect.width = 100  # ensure it matches the visible width
        custom_rect.height = 50  # and height
        collider._custom_rect = custom_rect  # store it in a custom attribute
        
        collider.subscribe("collision_enter", self.on_collision_enter)
        self.shoot_sound = pygame.mixer.Sound("laser.mp3")

    def start(self):
        pass

    def update(self, delta_time):
        keys = pygame.key.get_pressed()
        speed = 500
        movement = pygame.math.Vector2(0, 0)
        self._time_since_last_shot += delta_time

        if keys[pygame.K_a]:
            movement.x -= speed
        if keys[pygame.K_d]:
            movement.x += speed
        if keys[pygame.K_SPACE]:
            self.shoot()

        self._gameObject.transform.translate(movement * delta_time)

        if self._gameObject.transform.position.x < -self._sprite_size.x:
            self._gameObject.transform.position.x = self._screen_size.x
        elif self._gameObject.transform.position.x > self._screen_size.x:
            self._gameObject.transform.position.x = -self._sprite_size.x

        bottom_limit = self._screen_size.y - self._sprite_size.y
        if self._gameObject.transform.position.y > bottom_limit:
            self._gameObject.transform.position.y = bottom_limit
        elif self._gameObject.transform.position.y < 0:
            self._gameObject.transform.position.y = 0

    def shoot(self):
        if self._time_since_last_shot >= self._shoot_delay:
            active_lasers = [obj for obj in self._game_world._gameObjects if isinstance(obj.get_component(Laser), Laser)]

            if len(active_lasers) >= 2:
                return

            projectile = GameObject(None)
            projectile.tag = "Laser"  # Set tag for laser
            sr = projectile.add_component(SpriteRenderer("laser.png"))
            projectile.add_component(Laser())
            projectile.add_component(Collider())  # Add Collider component to the laser

            projectile_position = pygame.math.Vector2(
                self._gameObject.transform.position.x + (self._sprite_size.x / 2) - sr.sprite_image.get_width() / 2,
                self._gameObject.transform.position.y - 40
            )

            projectile.transform.position = projectile_position
            self._game_world.instantiate(projectile)

            self._time_since_last_shot = 0
            self.shoot_sound.play()

    def on_collision_enter(self, other):
        if self.invincible:
            return

        if "Enemy" in other.gameObject.tag or "EnemyLaser" in other.gameObject.tag:
            self.lives -= 1
            print(f"💥 Hit! {self.lives} lives left")

            if self.lives <= 0:
                self.game_over()
            else:
                self.become_invincible()

    @staticmethod
    def on_collision_exit(_other):
        print("collision exit")

    @staticmethod
    def on_pixel_collision_enter(_other):
        print("pixel collision enter")

    @staticmethod
    def on_pixel_collision_exit(_other):
        print("pixel collision exit")

    def become_invincible(self):
        self.invincible = True
        sr = self._gameObject.get_component("SpriteRenderer")

        # Blink effect
        def toggle_visibility():
            sr.set_alpha(100 if sr.sprite_image.get_alpha() == 255 else 255)

        for i in range(6):
            self._game_world.start_timer(i * 0.25, toggle_visibility)

        self._game_world.start_timer(1.5, lambda: setattr(self, "invincible", False))

    def game_over(self):
        print("❌ GAME OVER!")
