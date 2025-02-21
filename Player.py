from component import Components
import pygame
from gameObject import GameObject
from component import Laser
from component import SpriteRenderer

class Player(Components):

    def awake(self, game_world):  
        self._time_since_last_shot = 1
        self._shoot_dealy = 1 
        self._game_world = game_world
        sr = self._gameObject.get_component("SpriteRenderer")
        self._screen_size = pygame.math.Vector2(game_world.screen.get_width(),game_world.screen.get_height())
        self._sprite_size = pygame.math.Vector2(sr.sprite_image.get_width(),sr.sprite_image.get_height())
        self._gameObject.transform.position.x = (self._screen_size.x/2) - (self._sprite_size.x/2)
        self._gameObject.transform.position.y = (self._screen_size.y) - (self._sprite_size.y)

    def start(self):
        pass

    def update(self, delta_time): 
        keys = pygame.key.get_pressed()
        speed = 250
        movement = pygame.math.Vector2(0,0)
        self._time_since_last_shot += delta_time

        if keys[pygame.K_w]:
            movement.y -= speed
        if keys[pygame.K_s]:
            movement.y += speed
        if keys[pygame.K_a]:
            movement.x -= speed
        if keys[pygame.K_d]:
            movement.x += speed
        if keys[pygame.K_SPACE]:
            self.shoot()

        self._gameObject.transform.translate(movement*delta_time)

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
        if self._time_since_last_shot >= self._shoot_dealy:
            projectile = GameObject(pygame.math.Vector2(0, 0))
            sr = projectile.add_component(SpriteRenderer("laser.png"))
            projectile.add_component(Laser())

            projectile_position = pygame.math.Vector2(self._gameObject.transform.position.x+(self._sprite_size.x/2)-sr.sprite_image.get_width()/2,
                                                      self._gameObject.transform.position.y-40)
            
            projectile.transform.position = projectile_position
            
            self._game_world.instantiate(projectile)
            
            self._time_since_last_shot = 0