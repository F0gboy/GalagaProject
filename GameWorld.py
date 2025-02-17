import pygame

class GameWorld:
    
    def __init__(self) -> None:
        pygame.init()

        self._screen = pygame.display.set_mode((1280, 720))
        self._running = True
        self._clock = pygame.time.Clock()

    def Awake(self):
        pass

    def Start(self):
        pass

    def Update(self):

        while self._running:
            # poll for events
            # pygame.QUIT event means the user clicked X to close your window
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self._running = False

            # fill the screen with a color to wipe away anything from last frame
            self._screen.fill("cornflowerblue")

            # flip() the display to put your work on screen
            pygame.display.flip()

            self._clock.tick(60)  # limits FPS to 60

        pygame.quit()

gw = GameWorld()

gw.Awake()
gw.Start()
gw.Update()