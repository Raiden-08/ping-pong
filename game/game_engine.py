import pygame
from .paddle import Paddle
from .ball import Ball
import sys

WHITE = (255, 255, 255)

class GameEngine:
    def __init__(self, screen, width, height):
        self.screen = screen
        self.width = width
        self.height = height
        self.paddle_width = 10
        self.paddle_height = 100

        self.player = Paddle(10, height // 2 - 50, self.paddle_width, self.paddle_height)
        self.ai = Paddle(width - 20, height // 2 - 50, self.paddle_width, self.paddle_height)
        self.ball = Ball(width // 2, height // 2, 7, 7, width, height)

        self.font = pygame.font.SysFont("Arial", 30)
        self.large_font = pygame.font.SysFont("Arial", 50)
        
        self.paddle_hit_sound = pygame.mixer.Sound("assets/paddle_hit.wav")
        self.wall_bounce_sound = pygame.mixer.Sound("assets/wall_bounce.wav")
        self.score_sound = pygame.mixer.Sound("assets/score.wav")

        self.winning_score = 5
        self.game_over = False
        self.winner_text = ""
        self.reset_game(self.winning_score)

    def handle_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.player.move(-10, self.height)
        if keys[pygame.K_s]:
            self.player.move(10, self.height)

    def update(self):
        if self.ball.move():
            self.wall_bounce_sound.play()

        if self.ball.check_collision(self.player, self.ai):
            self.paddle_hit_sound.play()
        
        self.ai.auto_track(self.ball, self.height)

        if self.ball.x <= 0:
            self.ai_score += 1
            self.score_sound.play()
            self.ball.reset()
        elif self.ball.x >= self.width:
            self.player_score += 1
            self.score_sound.play()
            self.ball.reset()

    def render(self):
        pygame.draw.rect(self.screen, WHITE, self.player.rect())
        pygame.draw.rect(self.screen, WHITE, self.ai.rect())
        pygame.draw.ellipse(self.screen, WHITE, self.ball.rect())
        pygame.draw.aaline(self.screen, WHITE, (self.width//2, 0), (self.width//2, self.height))

        player_text = self.font.render(str(self.player_score), True, WHITE)
        ai_text = self.font.render(str(self.ai_score), True, WHITE)
        self.screen.blit(player_text, (self.width//4, 20))
        self.screen.blit(ai_text, (self.width * 3//4, 20))

    def check_for_winner(self):
        if self.player_score >= self.winning_score:
            self.winner_text = "Player Wins!"
            self.game_over = True
        elif self.ai_score >= self.winning_score:
            self.winner_text = "AI Wins!"
            self.game_over = True

    def reset_game(self, winning_score):
        self.player_score = 0
        self.ai_score = 0
        self.ball.reset()
        self.winning_score = winning_score
        self.game_over = False
        self.winner_text = ""