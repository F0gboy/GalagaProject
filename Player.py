from Components import Component
import pygame
from GameObject import GameObject
from Components import Laser
from Components import SpriteRenderer

class Player(Component):

    def awake(self, game_world):  
        self._time_since_last_shot = 1
        self._shoot_dealy = 1 
        self._game_world = game_world
        sr = self._gameObject.get_component("SpriteRenderer")
        self._screen_size = pygame.math.Vector2(game_world.screen.get_width(),game_world.screen.get_height())
        self._sprite_size = pygame.math.Vector2(sr.sprite_image.get_width(),sr.sprite_image.get_height())
        self._gameObject.transform.position.x = (self._screen_size.x/2) - (self._sprite_size.x/2)
        self._gameObject.transform.position.y = (self._screen_size.y) - (self._sprite_size.y)
        collider = self._gameObject.get_component("Collider")
        collider.subscribe("collision_enter",self.on_collision_enter)
        collider.subscribe("collision_exit", self.on_collision_exit)
        collider.subscribe("pixel_collision_enter", self.on_pixel_collision_enter)
        collider.subscribe("pixel_collision_exit", self.on_pixel_collision_exit)

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
            projectile = GameObject(None)
            sr = projectile.add_component(SpriteRenderer("laser.png"))
            projectile.add_component(Laser())

            projectile_position = pygame.math.Vector2(self._gameObject.transform.position.x+(self._sprite_size.x/2)-sr.sprite_image.get_width()/2
                                                    ,self._gameObject.transform.position.y-40)
            
            projectile.transform.position = projectile_position
            
            self._game_world.instantiate(projectile)
            
            self._time_since_last_shot = 0
    
    def on_collision_enter(self, other):
        print("collision enter")

    def on_collision_exit(self, other):
        print("collision exit")

    def on_pixel_collision_enter(self, other):
        print("pixel collision enter")

    def on_pixel_collision_exit(self, other):
        print("pixel collision exit")
        


