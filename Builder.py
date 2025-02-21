from abc import ABC, abstractclassmethod
from gameObject import GameObject
from component import Animator, SpriteRenderer, Collider
from player import Player
from enemy import Enemy
import pygame
import random

class Builder(ABC):

    @abstractclassmethod
    def build(self):
        pass

    def get_gameObject(self) -> GameObject:
        pass

class PlayerBuilder(Builder):

    def build(self):
        self._gameObject = GameObject(pygame.math.Vector2(0,0))
        sprite_renderer = self._gameObject.add_component(SpriteRenderer("player.png"))
        sprite_renderer.resize(150, 150)  # Resize the player sprite to be smaller
        self._gameObject.add_component(Player())
        self._gameObject.add_component(Collider())  # Add Collider component
        animator = self._gameObject.add_component(Animator())

        animator.add_animation("Idle","player02.png",
                               "player03.png",
                               "player04.png",
                               "player05.png",
                               "player06.png",
                               "player07.png",
                               "player08.png",
                               "player07.png",
                               "player06.png",
                               "player05.png",
                               "player04.png",
                               "player03.png",)
        
        animator.play_animation("Idle")
    
    def get_gameObject(self) -> GameObject:
        return self._gameObject
    
class EnemyBuilder(Builder):
    def __init__(self):
        self._gameObjects = []

    def build(self, enemy_type, position, size=(50, 50), speed=300, attack_frequency=0.5):
        self.enemy_type = enemy_type
        self.position = position
        self._gameObject = GameObject(position)
        sprites = ["enemy_01.png", "enemy_02.png", "enemy_03.png"]
        selected_sprite = enemy_type
        sprite_renderer = self._gameObject.add_component(SpriteRenderer(selected_sprite))
        sprite_renderer.resize(size[0], size[1])
        self._gameObject.add_component(Enemy(speed, attack_frequency))
        self._gameObjects.append(self._gameObject)

    def build_wave(self, enemy_type, position, number_of_enemies, size=(50, 50), screen_width=1280, speed=300, attack_frequency=0.5):
        self._gameObjects = []
        x_offset = 0
        y_offset = 0
        for i in range(number_of_enemies):
            if position.x + x_offset + size[0] > screen_width - 50:
                x_offset = 0
                y_offset += size[1] + 10  # Move to the next line with some spacing
            self.build(enemy_type, pygame.math.Vector2(position.x + x_offset, position.y + y_offset), size, speed, attack_frequency)
            x_offset += size[0] + 10  # Add some spacing between enemies

    def get_gameObject_list(self) -> list:
        return self._gameObjects

    def get_front_row_enemies(self) -> list:
        if not self._gameObjects:
            return []
        front_row_y = max(enemy.transform.position.y for enemy in self._gameObjects)
        return [enemy for enemy in self._gameObjects if enemy.transform.position.y == front_row_y]