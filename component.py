from abc import ABC, abstractmethod
import pygame
import typing
if typing.TYPE_CHECKING:
    from enemy import Enemy

class Components(ABC):

    def __init__(self) -> None:
        super().__init__()
        self._gameObject = None

    @property
    def gameObject(self):
        return self._gameObject
    
    @gameObject.setter
    def gameObject(self,value):
        self._gameObject = value

    @abstractmethod
    def awake(self, game_world):
        pass
    
    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def update(self, delta_time):
        pass

class Transform(Components):

    def __init__(self, position) -> None:
        super().__init__()
        self._position = position

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, value):
        self._position = value

    def translate(self, direction):
        self._position += direction

    def awake(self, game_world):
        pass

    def start(self):
        pass

    def update(self, delta_time):
        pass

class SpriteRenderer(Components):

    def __init__(self, sprite_name) -> None:
        super().__init__()

        self._sprite_image = pygame.image.load(f"Assets\\{sprite_name}")
        self._sprite = pygame.sprite.Sprite()
        self._sprite.rect = self._sprite_image.get_rect()
        self._sprite_mask = pygame.mask.from_surface(self.sprite_image)

    def resize(self, width, height):
        self._sprite_image = pygame.transform.scale(self._sprite_image, (width, height))
        self._sprite.rect = self._sprite_image.get_rect()
        self._sprite_mask = pygame.mask.from_surface(self._sprite_image)

    @property
    def sprite_image(self):
        return self._sprite_image
    
    @property
    def sprite_mask(self):
        return self._sprite_mask
    
    @sprite_image.setter
    def sprite_image(self, value):
        self._sprite_image= value

    @property
    def sprite(self):
        return self._sprite
   
    def awake(self, game_world):
      self._game_world = game_world
      self._sprite.rect.topleft = self.gameObject.transform.position

    def start(self):
        pass
   
    def update(self, delta_time):
        self._sprite.rect.topleft = self.gameObject.transform.position
        self._game_world.screen.blit(self._sprite_image,self._sprite.rect)
    

class Animator(Components):

    def __init__(self) -> None:
        super().__init__()
        self._animations = {}
        self._current_animation = None
        self._animation_time = 0
        self._current_frame_index = 0

    def add_animation(self, name, *args):
        frames =[]
        for arg in args:
            sprite_image = pygame.image.load(f"Assets\\{arg}")
            frames.append(sprite_image)
        
        self._animations[name] = frames
    
    def play_animation(self, animation):
        self._current_animation = animation

    def awake(self, game_world):
        self._sprite_renderer = self._gameObject.get_component("SpriteRenderer")
    
    def start(self):
        pass

    def update(self, delta_time):
        frame_duration = 0.1

        self._animation_time += delta_time

        #skal vi skifte frame
        if self._animation_time >= frame_duration:
            self._animation_time = 0
            self._current_frame_index += 1
            
            #får vi fat på vores aimation
            animation_sequence = self._animations[self._current_animation]

            if self._current_frame_index >= len(animation_sequence):
                self._current_frame_index = 0 #Resetter vores animation
            
            #Skifter til en ny sprite
            self._sprite_renderer.sprite_image = animation_sequence[self._current_frame_index]

class Laser(Components):

    def awake(self, game_world):
        pass

    def start(self):
        pass

    def update(self, delta_time):
        speed = 500
        movement = pygame.math.Vector2(0, -speed)
        
        self.gameObject.transform.translate(movement * delta_time)

        if self.gameObject.transform.position.y < 0:
            self.gameObject.destroy()

    def on_collision_enter(self, other):
        if other.gameObject.get_component("Enemy") is not None:
            self.gameObject.destroy()
            other.gameObject.destroy()

class Collider(Components):
    def __init__(self) -> None:
        super().__init__()
        self._subscriptions = {}

    def subscribe(self, event_type, callback):
        if event_type not in self._subscriptions:
            self._subscriptions[event_type] = []
        self._subscriptions[event_type].append(callback)

    def notify(self, event_type, other):
        if event_type in self._subscriptions:
            for callback in self._subscriptions[event_type]:
                callback(other)

    def awake(self, game_world):
        pass

    def start(self):
        pass

    def update(self, delta_time):
        pass