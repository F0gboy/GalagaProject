import pygame
from gameWorld import GameWorld
from component import Button

def main():
    game_world = GameWorld()
    game_world.awake()
    game_world.start()

    runOnce = False

    while game_world._running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_world._running = False

            if not game_world._startGame and not game_world._options_started:
                for component in game_world.menu._components.values():
                    if isinstance(component, Button):
                        component.handle_event(event)
            
            if game_world._options_started:
                for component in game_world.options_menu._components.values():
                    if isinstance(component, Button):
                        component.handle_event(event)

        game_world._screen.fill((0, 0, 0))  # Clear the screen with black

        delta_time = game_world._clock.tick(60) / 1000.0

        if game_world._startGame and game_world._current_music != "space ingame":
            game_world.sound_manager.stop_sound()
            game_world.sound_manager.play_sound("space ingame")
            game_world._current_music = "space ingame"
        elif game_world._options_started and game_world._current_music != "space menu2":
            game_world.sound_manager.stop_sound()
            game_world.sound_manager.play_sound("space menu2")
            game_world._current_music = "space menu2"
        elif not game_world._startGame and not game_world._options_started and game_world._current_music != "space menu":
            game_world.sound_manager.stop_sound()
            game_world.sound_manager.play_sound("space menu")
            game_world._current_music = "space menu"

        if game_world._startGame:
            if not runOnce:
                game_world.awake()
                game_world.start()
                runOnce = True
            game_world.update(delta_time)

            active_colliders = [c for c in game_world._colliders if not c.gameObject.is_destroyed]
            for i, collider1 in enumerate(active_colliders):
                for j in range(i + 1, len(active_colliders)):
                    collider2 = active_colliders[j]
                    if collider1.check_collision(collider2):
                        collider1.notify("collision_enter", collider2)
                        collider2.notify("collision_enter", collider1)

            game_world._gameObjects = [obj for obj in game_world._gameObjects if not obj.is_destroyed]
        elif game_world._options_started:
            for component in game_world.options_menu._components.values():  
                if hasattr(component, "draw"):
                    component.draw(game_world._screen)
        elif not game_world._startGame and not game_world._options_started:
            for component in game_world.menu._components.values():  
                if hasattr(component, "draw"):
                    component.draw(game_world._screen)
        
        pygame.display.flip()
        game_world._clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()