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
    def gameObject(self, value):
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
        self._game_world = None
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
        self._sprite_image = value
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
        self._game_world._screen.blit(self._sprite_image, self._sprite.rect)
    def set_alpha(self, alpha):
        self._sprite_image.set_alpha(alpha)

class Animator(Components):
    def __init__(self) -> None:
        super().__init__()
        self._animations = {}
        self._current_animation = None
        self._animation_time = 0
        self._current_frame_index = 0
    def add_animation(self, name, *args):
        frames = []
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
        if self._animation_time >= frame_duration:
            self._animation_time = 0
            self._current_frame_index += 1
            animation_sequence = self._animations[self._current_animation]
            if self._current_frame_index >= len(animation_sequence):
                self._current_frame_index = 0
            self._sprite_renderer.sprite_image = animation_sequence[self._current_frame_index]

class Laser(Components):
    def awake(self, game_world):
        self._game_world = game_world
        collider = self._gameObject.get_component("Collider")
        collider.subscribe("collision_enter", self.on_collision_enter)
    def start(self):
        pass
    def update(self, delta_time):
        speed = 500
        movement = pygame.math.Vector2(0, -speed)
        self.gameObject.transform.translate(movement * delta_time)
        if self.gameObject.transform.position.y < 0:
            self._game_world.destroy(self.gameObject)
    def on_collision_enter(self, other):
        if other.gameObject.tag == "Enemy":
            self._game_world.destroy(self.gameObject)
            self._game_world.destroy(other.gameObject)

class Button(Components):
    def __init__(self, position, size, text, color, callback):
        super().__init__()
        self.position = position
        self.size = size
        self.text = text
        self.color = color
        self.callback = callback
        self.font = pygame.font.Font(None, 36)
        self.rect = pygame.Rect(position, size)
        self.text_surface = self.font.render(text, True, (0, 0, 0))
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        screen.blit(self.text_surface, (self.rect.x + 10, self.rect.y + 10))
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos):
            self.callback()
    def awake(self, game_world):
        pass
    def start(self):
        pass
    def update(self, delta_time):
        pass

class Boss_Laser(Components):
    def awake(self, game_world):
        self._game_world = game_world
        collider = self._gameObject.get_component("Collider")
        collider.subscribe("collision_enter", self.on_collision_enter)
    def start(self):
        pass
    def update(self, delta_time):
        speed = 500
        movement = pygame.math.Vector2(0, speed)
        self._gameObject.transform.translate(movement * delta_time)
        if self._gameObject.transform.position.y < 0:
            self._gameObject.destroy()
    def on_collision_enter(self, other):
        if other.gameObject.tag == "Enemy":
            self._game_world.destroy(self._gameObject)
            self._game_world.destroy(other.gameObject)
        elif other.gameObject.tag == "Player":
            self._game_world.destroy(self._gameObject)

class Collider(Components):
    def __init__(self) -> None:
        super().__init__()
        self._subscriptions = {}
        self._custom_rect = None
    def subscribe(self, event_type, callback):
        if event_type not in self._subscriptions:
            self._subscriptions[event_type] = []
        self._subscriptions[event_type].append(callback)
    def set_size(self, width, height):
        pos = self.gameObject.transform.position
        self._custom_rect = pygame.Rect(pos.x, pos.y, width, height)
    def awake(self, game_world):
        self._game_world = game_world
        self._game_world.colliders.append(self)
        sr = self.gameObject.get_component("SpriteRenderer")
        if sr:
            self._custom_rect = sr._sprite.rect.copy()
    def start(self):
        pass
    def update(self, delta_time):
        if self.gameObject.is_destroyed:
            return
        if self._custom_rect is not None:
            self._custom_rect.topleft = self.gameObject.transform.position
        for other in self._game_world.colliders:
            if other != self and not other.gameObject.is_destroyed:
                if self.check_collision(other):
                    self.notify("collision_enter", other)
                    other.notify("collision_enter", self)
    def notify(self, event_type, other):
        if event_type in self._subscriptions:
            for callback in self._subscriptions[event_type]:
                callback(other)
    def check_collision(self, other):
        self_rect = self._custom_rect or self.gameObject.get_component("SpriteRenderer").sprite.rect
        other_rect = other._custom_rect or other.gameObject.get_component("SpriteRenderer").sprite.rect
        return self_rect.colliderect(other_rect)
