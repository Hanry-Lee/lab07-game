"""Example game showing a circle moving on screen."""
import os
import pygame
from typing import Optional

from game import Game
from player import Player
from opponent import Opponent
from food import Food, FoodList
from save_state import save_game, load_game

SAVE_FILE = "savegame.json"

def welcome_screen(screen: pygame.Surface) -> str:
    """Display welcome screen. Returns 'start', 'load', or 'exit'."""
    clock = pygame.time.Clock()

    while True:
        screen.fill("purple")

        title_font = pygame.font.Font(None, 72)
        title = title_font.render("Chase & Collect", True, "yellow")
        title_rect = title.get_rect(center=(screen.get_width() / 2, 150))
        screen.blit(title, title_rect)

        menu_font = pygame.font.Font(None, 48)

        start_text = menu_font.render("Press ENTER to Start", True, "white")
        start_rect = start_text.get_rect(center=(screen.get_width() / 2, 300))
        screen.blit(start_text, start_rect)

        load_color = "white" if os.path.exists(SAVE_FILE) else "gray"
        load_text = menu_font.render("Press L to Load Game", True, load_color)
        load_rect = load_text.get_rect(center=(screen.get_width() / 2, 380))
        screen.blit(load_text, load_rect)

        exit_text = menu_font.render("Press ESC to Exit", True, "white")
        exit_rect = exit_text.get_rect(center=(screen.get_width() / 2, 460))
        screen.blit(exit_text, exit_rect)

        hint_font = pygame.font.Font(None, 24)
        hint = hint_font.render("Use mouse to control player | Collect food before the opponent!", True, "gray")
        hint_rect = hint.get_rect(center=(screen.get_width() / 2, 550))
        screen.blit(hint, hint_rect)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "exit"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return "start"
                if event.key == pygame.K_l and os.path.exists(SAVE_FILE):
                    return "load"
                if event.key == pygame.K_ESCAPE:
                    return "exit"

        clock.tick(60)

def draw(game: Game, player: Player, opponent: Opponent, food_list: FoodList, winner: Optional[str] = None, message: Optional[str] = None):
    game.screen.fill(game.background)

    for s in [player, opponent]:
        pygame.draw.circle(game.screen, s.color, pygame.Vector2(s.x, s.y), s.size)
    for f in food_list.food:
        pygame.draw.circle(game.screen, "blue", pygame.Vector2(f.x, f.y), f.size)

    font = pygame.font.Font(None, 36)

    player_score = font.render(f"Player: {player.count}", True, "white")
    opponent_score = font.render(f"Opponent: {opponent.count}", True, "white")
    game.screen.blit(player_score, (10, 10))
    game.screen.blit(opponent_score, (10, 50))

    controls = pygame.font.Font(None, 24).render("Controls: Mouse | S=Save | L=Load | P=Pause | ESC/Q=Quit", True, "gray")
    game.screen.blit(controls, (10, game.screen.get_height() - 30))

    if message:
        msg_font = pygame.font.Font(None, 36)
        msg_text = msg_font.render(message, True, "lime")
        msg_rect = msg_text.get_rect(center=(game.screen.get_width() / 2, 100))
        game.screen.blit(msg_text, msg_rect)

    if winner:
        big_font = pygame.font.Font(None, 72)
        text = big_font.render(f"{winner} Wins!", True, "yellow")
        rect = text.get_rect(center=(game.screen.get_width() / 2, game.screen.get_height() / 2))
        game.screen.blit(text, rect)

        restart = font.render("R=Restart | Q=Quit | M=Menu", True, "white")
        restart_rect = restart.get_rect(center=(game.screen.get_width() / 2, game.screen.get_height() / 2 + 50))
        game.screen.blit(restart, restart_rect)

    pygame.display.flip()

def main():
    pygame.init()

    screen = pygame.display.set_mode((1280, 720))
    choice = welcome_screen(screen)

    if choice == "exit":
        pygame.quit()
        return

    game = Game(
        screen     = screen,
        clock      = pygame.time.Clock(),
        background = "purple",
        fps        = 60,
        running    = True,
        deltaT     = 0,
    )

    player = Player(
        x     = 200,
        y     = game.screen.get_height() / 2,
        size  = 40,
        speed = 300,
        color = "red"
    )

    opponent = Opponent(
        x     = game.screen.get_width() - 200,
        y     = game.screen.get_height() / 2,
        size  = 40,
        speed = 150,
        color = "green"
    )

    food_list = FoodList([])
    food_list.populate(100, (game.screen.get_width(), game.screen.get_height()))

    if choice == "load" and os.path.exists(SAVE_FILE):
        state = load_game(SAVE_FILE)
        player.x, player.y = state["player"]["x"], state["player"]["y"]
        player.size, player.count = state["player"]["size"], state["player"]["count"]
        opponent.x, opponent.y = state["opponent"]["x"], state["opponent"]["y"]
        opponent.size, opponent.count = state["opponent"]["size"], state["opponent"]["count"]
        food_list.food = [Food(x=f["x"], y=f["y"], size=f["size"]) for f in state["food"]]

    winner = None
    message = None
    message_timer = 0
    paused = False

    screen_w, screen_h = game.screen.get_width(), game.screen.get_height()

    while game.running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game.running = False
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                if winner:
                    if event.key == pygame.K_r:
                        main()
                        return
                    if event.key == pygame.K_q:
                        game.running = False
                        pygame.quit()
                        return
                    if event.key == pygame.K_m:
                        main()
                        return
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_q:
                    game.running = False
                    pygame.quit()
                    return
                if event.key == pygame.K_p:
                    paused = not paused
                if event.key == pygame.K_s:
                    save_game(SAVE_FILE, player, opponent, food_list)
                    message = "Game Saved!"
                    message_timer = 120
                if event.key == pygame.K_l and os.path.exists(SAVE_FILE):
                    state = load_game(SAVE_FILE)
                    player.x, player.y = state["player"]["x"], state["player"]["y"]
                    player.size, player.count = state["player"]["size"], state["player"]["count"]
                    opponent.x, opponent.y = state["opponent"]["x"], state["opponent"]["y"]
                    opponent.size, opponent.count = state["opponent"]["size"], state["opponent"]["count"]
                    food_list.food = [Food(x=f["x"], y=f["y"], size=f["size"]) for f in state["food"]]
                    winner = None
                    message = "Game Loaded!"
                    message_timer = 120

        if message_timer > 0:
            message_timer -= 1
        else:
            message = None

        game.tick()

        if not winner and not paused:
            player.move_to(pygame.mouse.get_pos())
            player.x = max(player.size, min(screen_w - player.size, player.x))
            player.y = max(player.size, min(screen_h - player.size, player.y))

            opponent.move(food_list, (player.x, player.y), game.deltaT)
            opponent.x = max(opponent.size, min(screen_w - opponent.size, opponent.x))
            opponent.y = max(opponent.size, min(screen_h - opponent.size, opponent.y))

            food_list.eat(player)
            food_list.eat(opponent)

            food_list.move((screen_w, screen_h))

            if not food_list.food:
                if player.count > opponent.count:
                    winner = "Player"
                elif opponent.count > player.count:
                    winner = "Opponent"
                else:
                    winner = "Tie"

        if paused:
            message = "PAUSED - Press P to resume"

        draw(game, player, opponent, food_list, winner, message)

if __name__ == "__main__":
    main()
