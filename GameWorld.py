import pygame
from GameObject import GameObject
from Components import Animator
from Components import SpriteRenderer
from Components import Button
from Player import Player
from Builder import PlayerBuilder
from Builder import EnemyBuilder
from Builder import MenuBuilder
from SoundManager import SoundManager
pygame.init
class GameWorld:

    def __init__(self) -> None:
        pygame.init()

        self._gameObjects = []
        self._colliders = []
        
        self._screen = pygame.display.set_mode((1280,720))
        self._running = True
        self._clock = pygame.time.Clock()
        self._game_started = False

        self.menu = MenuBuilder() \
            .add_button("Start", (self._screen.get_width() / 2 -100, 200), (200, 50), (0, 128, 255), lambda: self.start_game()) \
            .add_button("Options", (self._screen.get_width() / 2 -100, 300), (200, 50), (0, 128, 255), lambda: self.show_options()) \
            .add_button("Quit", (self._screen.get_width() / 2 -100, 400), (200, 50), (0, 128, 255), lambda: self.quit_game()) \
            .build()
        
        self.sound_manager = SoundManager()

    @property
    def screen(self):
        return self._screen
    
    @property
    def colliders(self):
        return self._colliders
    
    def start_game(self):
        self._game_started = True
        self._gameObjects = []

        # Tilføj spilleren
        player_builder = PlayerBuilder()
        player_builder.build()
        self._gameObjects.append(player_builder.get_gameObject())

        # Tilføj fjender
        enemy_builder = EnemyBuilder()
        enemy_builder.build()
        self._gameObjects.append(enemy_builder.get_gameObject())

    def quit_game(self):
        self._running = False
    
    def instantiate(self, gameObject):
        gameObject.awake(self)
        gameObject.start()
        self._gameObjects.append(gameObject)


    def Awake(self):
        for gameObject in self._gameObjects[:]:
            gameObject.awake(self)
    
    def Start(self):
        for gameObject in self._gameObjects[:]:
            gameObject.start()

    def update(self):

        while self._running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self._running = False

                if not self._game_started:
                    # Hvis spillet ikke er startet, håndter menu-events
                    for component in self.menu._components.values():
                        if isinstance(component, Button):
                            component.handle_event(event)

            self._screen.fill("cornflowerblue")

            delta_time = self._clock.tick(60) / 1000.0

            if self._game_started:
            #draw your game
                for gameObject in self._gameObjects[:]:
                    gameObject.update(delta_time)

                for i, collider1 in enumerate(self._colliders):
                    for j in range(i + 1, len(self._colliders)):
                        collider2 = self._colliders[j]
                        collider1.collision_check(collider2)

                self._gameObjects = [obj for obj in self._gameObjects if not obj.is_destroyed]
            else:
                self.sound_manager.play_sound("space menu")
                for component in self.menu._components.values():  
                    if hasattr(component, "draw"):
                        component.draw(self._screen)
            
            pygame.display.flip()
            self._clock.tick(60)

        pygame.quit()
    

gw = GameWorld()

gw.Awake()
gw.Start()
gw.update()

        