import pygame
from GameObject import GameObject
from Components import Animator, SpriteRenderer, Button
from Player import Player
from Builder import PlayerBuilder, EnemyBuilder, MenuBuilder
from SoundManager import SoundManager

pygame.init()

class GameWorld:

    def __init__(self) -> None:
        pygame.init()

        self._gameObjects = []
        self._colliders = []
        
        self._screen = pygame.display.set_mode((1280,720))
        self._clock = pygame.time.Clock()
        self.sound_manager = SoundManager()
        self._running = True
        self._game_started = False
        self._options_started = False
        self._current_music = None

        self.menu = MenuBuilder() \
            .add_button("Start", (self._screen.get_width() / 2 -100, 200), (200, 50), (255, 255, 255), lambda: self.start_game()) \
            .add_button("Options", (self._screen.get_width() / 2 -100, 300), (200, 50), (255, 255, 255), lambda: self.show_options()) \
            .add_button("Quit", (self._screen.get_width() / 2 -100, 400), (200, 50), (255, 255, 255), lambda: self.quit_game()) \
            .build()

        self.options_menu = MenuBuilder() \
            .add_button("Volume +", (self._screen.get_width() / 2 -100, 250), (200, 50), (255, 255, 255), lambda: self.sound_manager.increase_volume()) \
            .add_button("Volume -", (self._screen.get_width() / 2 -100, 350), (200, 50), (255, 255, 255), lambda: self.sound_manager.decrease_volume()) \
            .add_button("Back", (self._screen.get_width() / 2 -100, 450), (200, 50), (255, 255, 255), lambda: self.back_to_menu()) \
            .build()
        
    @property
    def screen(self):
        return self._screen
    
    @property
    def colliders(self):
        return self._colliders
    
    def start_game(self):
        self._game_started = True
        self._gameObjects = []

        player_builder = PlayerBuilder()
        player_builder.build()
        self.instantiate(player_builder.get_gameObject())

        enemy_builder = EnemyBuilder()
        enemy_builder.build()
        self.instantiate(enemy_builder.get_gameObject())
        

    def quit_game(self):
        self._running = False

    def show_options(self):
        self._options_started = True

    def back_to_menu(self):
        self._options_started = False
    
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

            if not self._game_started and not self._options_started:
                for component in self.menu._components.values():
                    if isinstance(component, Button):
                        component.handle_event(event)
            
            if self._options_started:
                for component in self.options_menu._components.values():
                    if isinstance(component, Button):
                        component.handle_event(event)

            self._screen.fill("black")

            delta_time = self._clock.tick(60) / 1000.0

            if self._game_started and self._current_music != "space ingame":
                self.sound_manager.stop_sound()
                self.sound_manager.play_sound("space ingame")
                self._current_music = "space ingame"
            elif self._options_started and self._current_music != "space menu2":
                self.sound_manager.stop_sound()
                self.sound_manager.play_sound("space menu2")
                self._current_music = "space menu2"
            elif not self._game_started and not self._options_started and self._current_music != "space menu":
                self.sound_manager.stop_sound()
                self.sound_manager.play_sound("space menu")
                self._current_music = "space menu"

            if self._game_started:
                for gameObject in self._gameObjects[:]:
                    gameObject.update(delta_time)

                for i, collider1 in enumerate(self._colliders):
                    for j in range(i + 1, len(self._colliders)):
                        collider2 = self._colliders[j]
                        collider1.collision_check(collider2)

                self._gameObjects = [obj for obj in self._gameObjects if not obj.is_destroyed]
            elif self._options_started:
                for component in self.options_menu._components.values():  
                    if hasattr(component, "draw"):
                        component.draw(self._screen)
            elif not self._game_started and not self._options_started:
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
        