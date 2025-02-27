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

            if game_world.win:
                game_world._screen.fill((0,0,0))
                win_text = game_world.font.render("You won! Final Score: " + str(game_world.score), True, (255,255,255))
                x = (game_world._screen.get_width() - win_text.get_width()) // 2
                y = (game_world._screen.get_height() - win_text.get_height()) // 2
                game_world._screen.blit(win_text, (x,y))
                pygame.display.flip()
                continue

            if game_world.lose:
                game_world._screen.fill((0,0,0))
                lose_text = game_world.font.render("You lost! Final Score: " + str(game_world.score), True, (255,0,0))
                x = (game_world._screen.get_width() - lose_text.get_width()) // 2
                y = (game_world._screen.get_height() - lose_text.get_height()) // 2
                game_world._screen.blit(lose_text, (x,y))
                pygame.display.flip()
                continue

            if not game_world._startGame and not game_world._options_started and not game_world.win and not game_world.lose:
                # Draw title on main menu
                title_surface = game_world.font.render("Galaga Project", True, (255,255,255))
                title_x = (game_world._screen.get_width() - title_surface.get_width()) // 2
                title_y = 50
                game_world._screen.blit(title_surface, (title_x, title_y))
                for component in game_world.menu._components.values():
                    if isinstance(component, Button):
                        component.handle_event(event)
            if game_world._options_started:
                for component in game_world.options_menu._components.values():
                    if isinstance(component, Button):
                        component.handle_event(event)

        if not (game_world.win or game_world.lose):
            game_world._screen.fill((0,0,0))
        delta_time = game_world._clock.tick(60) / 1000.0

        if not game_world._startGame and not game_world._options_started and not game_world.win and not game_world.lose:
            # Draw the title at the top center
            title_surface = game_world.font.render("Gologo", True, (255, 255, 255))
            title_x = (game_world._screen.get_width() - title_surface.get_width()) // 2
            title_y = 100  # You can adjust this Y offset as needed
            game_world._screen.blit(title_surface, (title_x, title_y))
            
            # Now draw the menu buttons
            for component in game_world.menu._components.values():
                if hasattr(component, "draw"):
                    component.draw(game_world._screen)

        if game_world._startGame and game_world._current_music != "space ingame":
            game_world.sound_manager.stop_sound()
            game_world.sound_manager.play_sound("space ingame")
            game_world._current_music = "space ingame"
        elif game_world._options_started and game_world._current_music != "space menu2":
            game_world.sound_manager.stop_sound()
            game_world.sound_manager.play_sound("space menu2")
            game_world._current_music = "space menu2"
        elif not game_world._startGame and not game_world._options_started and not (game_world.win or game_world.lose) and game_world._current_music != "space menu":
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
                for j in range(i+1, len(active_colliders)):
                    collider2 = active_colliders[j]
                    if collider1.check_collision(collider2):
                        collider1.notify("collision_enter", collider2)
                        collider2.notify("collision_enter", collider1)
            game_world._gameObjects = [obj for obj in game_world._gameObjects if not obj.is_destroyed]
        elif game_world._options_started and not (game_world.win or game_world.lose):
            for component in game_world.options_menu._components.values():
                if hasattr(component, "draw"):
                    component.draw(game_world._screen)
        elif not game_world._startGame and not game_world._options_started and not (game_world.win or game_world.lose):
            for component in game_world.menu._components.values():
                if hasattr(component, "draw"):
                    component.draw(game_world._screen)
        pygame.display.flip()
        game_world._clock.tick(60)
    pygame.quit()

if __name__ == "__main__":
    main()
