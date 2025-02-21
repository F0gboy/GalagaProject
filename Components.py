from abc import ABC, abstractmethod
import pygame

class Component(ABC):

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

class Transform(Component):

    def __init__(self, position) -> None:
        super().__init__()
        self._position = position

    @property
    def position(self):
        return self._position
    
    @position.setter
    def position(self,value):
        self._position = value

    def translate(self, direction):
        self._position += direction
        
    def awake(self, game_world):
        pass

    def start(self):
        pass
   
    def update(self, delta_time):
        pass

class SpriteRenderer(Component):

    def __init__(self, sprite_name) -> None:
        super().__init__()
        self._sprite_image = pygame.image.load(f"Assets\\{sprite_name}")
        self._sprite = pygame.sprite.Sprite()
        self._sprite.rect = self._sprite_image.get_rect()
        self._sprite_mask = pygame.mask.from_surface(self.sprite_image)
        self._game_world = None  # Add this line to define the attribute

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
        print(f"Awakening SpriteRenderer with game_world: {game_world}")
        self._game_world = game_world  # Set the game world here
        self._sprite.rect.topleft = self.gameObject.transform.position

    def start(self):
        pass
   
    def update(self, delta_time):
        if self._game_world is None:
            print("Error: _game_world is None in SpriteRenderer.update")
        self._sprite.rect.topleft = self.gameObject.transform.position
        self._game_world.screen.blit(self._sprite_image, self._sprite.rect) 

# ...existing code...
class Animator(Component):

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

class Laser(Component):

    def awake(self, game_world):
        pass

    def start(self):
        pass

    def update(self, delta_time):
        speed = 500
        movement = pygame.math.Vector2(0,-speed)
        
        self._gameObject.transform.translate(movement*delta_time)

        if self._gameObject.transform.position.y < 0:
            self._gameObject.destroy()

class Button(Component):
    def __init__(self, position, size, text, color, callback):
        super().__init__()
        self.position = position
        self.size = size
        self.text = text
        self.color = color
        self.callback = callback
        self.font = pygame.font.Font(None, 36)
        self.rect = pygame.Rect(position, size)
        self.text_surface = self.font.render(text, True, (255, 255, 255))

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

class Collider():
    def __init__(self) -> None:
        self._other_colliders = []
        self._other_masks = []
        self._listeners = {}

    def awake(self, game_world):
        sr = self.gameObject.get_component("SpriteRenderer")
        self._collision_box = sr.sprite.rect
        self._sprite_mask = sr.sprite_mask
        game_world.colliders.append(self)

    @property
    def collision_box(self):
        return self._collision_box
    
    @property 
    def sprite_mask(self):
        return self._sprite_mask

    def subscribe(self, service, method):
        self._listeners[service] = method
    
    def collision_check(self, other):
        is_rect_colliding = self._collision_box.colliderect(other.collision_box)
        is_already_colliding = other in self._other_colliders

        if is_rect_colliding:
            if not is_already_colliding:
                self.collision_enter(other)
                other.collision_enter(self)
            if self.check_pixel_collision(self._collision_box, other.collision_box,self._sprite_mask, other.sprite_mask):
                if other not in self._other_masks:
                    self.pixel_collision_enter(other)
                    other.pixel_collision_enter(self)
               
            else:
                if other in self._other_masks:
                    self.pixel_collision_exit(other)
                    other.pixel_collision_exit(self)
        else:
            if is_already_colliding:
                self.collision_exit(other)
                other.collision_exit(self)


    def check_pixel_collision(self, collision_box1, collision_box2, mask1, mask2):
        offset_x = collision_box2.x - collision_box1.x
        offset_y = collision_box2.y - collision_box1.y

        return mask1.overlap(mask2, (offset_x,offset_y)) is not None




    def start(self):
        pass

    def update(self, delta_time):
        pass

    def collision_enter(self, other):
        self._other_colliders.append(other)
        if "collision_enter" in self._listeners:
            self._listeners["collision_enter"](other)

    def collision_exit(self, other):
         self._other_colliders.remove(other)
         if "collision_exit" in self._listeners:
            self._listeners["collision_exit"](other)

    def pixel_collision_enter(self,other):
        self._other_masks.append(other)
        if "pixel_collision_enter" in self._listeners:
            self._listeners["pixel_collision_enter"](other)

    def pixel_collision_exit(self,other):
         self._other_masks.remove(other)
         if "pixel_collision_exit" in self._listeners:
            self._listeners["pixel_collision_exit"](other)

        
