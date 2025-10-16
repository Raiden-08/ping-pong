import pygame
from game.game_engine import GameEngine

pygame.init()

WIDTH, HEIGHT = 800, 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ping Pong - Pygame Version")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

clock = pygame.time.Clock()
FPS = 60

engine = GameEngine(SCREEN, WIDTH, HEIGHT)

def main():
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        SCREEN.fill(BLACK)

        if not engine.game_over:
            engine.handle_input()
            engine.update()
            engine.check_for_winner()
            engine.render()
        else:
            winner_surf = engine.large_font.render(engine.winner_text, True, WHITE)
            winner_rect = winner_surf.get_rect(center=(WIDTH/2, HEIGHT/4))
            SCREEN.blit(winner_surf, winner_rect)

            options = [
                "Play Again:",
                "[3] - Best of 3",
                "[5] - Best of 5",
                "[7] - Best of 7",
                "[ESC] - Exit"
            ]
            for i, line in enumerate(options):
                option_surf = engine.font.render(line, True, WHITE)
                option_rect = option_surf.get_rect(center=(WIDTH/2, HEIGHT/2 + i * 40))
                SCREEN.blit(option_surf, option_rect)

            keys = pygame.key.get_pressed()
            if keys[pygame.K_3]:
                engine.reset_game(3)
            elif keys[pygame.K_5]:
                engine.reset_game(5)
            elif keys[pygame.K_7]:
                engine.reset_game(7)
            elif keys[pygame.K_ESCAPE]:
                running = False

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == '__main__':
    main()