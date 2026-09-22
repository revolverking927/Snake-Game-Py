"""
Snake — eat the apples, don't hit yourself or the walls!

Controls:
    Arrow keys / WASD - move
    P                 - pause
    R                 - restart after game over
    Esc / close window - quit

Requires: pygame  (pip install pygame)
"""

import pygame
import random
import sys

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
CELL_SIZE = 24
GRID_WIDTH = 25
GRID_HEIGHT = 20
WIDTH = CELL_SIZE * GRID_WIDTH
HEIGHT = CELL_SIZE * GRID_HEIGHT
FPS_START = 10          # initial game speed
FPS_MAX = 20             # speed cap as the snake grows
SPEEDUP_EVERY = 5        # apples eaten before speed increases

# Colors
BG_COLOR = (18, 18, 24)
GRID_COLOR = (28, 28, 36)
SNAKE_HEAD_COLOR = (90, 220, 120)
SNAKE_BODY_COLOR = (60, 180, 95)
APPLE_COLOR = (230, 70, 70)
APPLE_STEM_COLOR = (120, 80, 40)
TEXT_COLOR = (240, 240, 240)
SHADOW_COLOR = (0, 0, 0)

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)


class Snake:
    def __init__(self):
        cx, cy = GRID_WIDTH // 2, GRID_HEIGHT // 2
        self.body = [(cx, cy), (cx - 1, cy), (cx - 2, cy)]
        self.direction = RIGHT
        self.pending_direction = RIGHT
        self.grow_pending = 0

    def set_direction(self, new_dir):
        # Prevent reversing directly into itself
        opposite = (-self.direction[0], -self.direction[1])
        if new_dir != opposite:
            self.pending_direction = new_dir

    def head(self):
        return self.body[0]

    def move(self):
        self.direction = self.pending_direction
        hx, hy = self.head()
        dx, dy = self.direction
        new_head = (hx + dx, hy + dy)
        self.body.insert(0, new_head)
        if self.grow_pending > 0:
            self.grow_pending -= 1
        else:
            self.body.pop()

    def grow(self, amount=1):
        self.grow_pending += amount

    def collides_with_self(self):
        return self.head() in self.body[1:]

    def collides_with_wall(self):
        hx, hy = self.head()
        return not (0 <= hx < GRID_WIDTH and 0 <= hy < GRID_HEIGHT)


class Apple:
    def __init__(self, snake_body):
        self.position = (0, 0)
        self.respawn(snake_body)

    def respawn(self, snake_body):
        free_cells = [
            (x, y)
            for x in range(GRID_WIDTH)
            for y in range(GRID_HEIGHT)
            if (x, y) not in snake_body
        ]
        self.position = random.choice(free_cells) if free_cells else None


def draw_grid(surface):
    for x in range(0, WIDTH, CELL_SIZE):
        pygame.draw.line(surface, GRID_COLOR, (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, CELL_SIZE):
        pygame.draw.line(surface, GRID_COLOR, (0, y), (WIDTH, y))


def draw_snake(surface, snake):
    for i, (x, y) in enumerate(snake.body):
        rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        color = SNAKE_HEAD_COLOR if i == 0 else SNAKE_BODY_COLOR
        pygame.draw.rect(surface, color, rect.inflate(-2, -2), border_radius=6)


def draw_apple(surface, apple):
    if apple.position is None:
        return
    x, y = apple.position
    cx = x * CELL_SIZE + CELL_SIZE // 2
    cy = y * CELL_SIZE + CELL_SIZE // 2
    radius = CELL_SIZE // 2 - 3
    pygame.draw.circle(surface, APPLE_COLOR, (cx, cy), radius)
    pygame.draw.line(
        surface, APPLE_STEM_COLOR,
        (cx, cy - radius), (cx + 3, cy - radius - 6), 3
    )


def draw_text_center(surface, text, size, y_offset=0, color=TEXT_COLOR):
    font = pygame.font.SysFont("consolas", size, bold=True)
    shadow = font.render(text, True, SHADOW_COLOR)
    label = font.render(text, True, color)
    rect = label.get_rect(center=(WIDTH // 2, HEIGHT // 2 + y_offset))
    surface.blit(shadow, rect.move(2, 2))
    surface.blit(label, rect)


def draw_score(surface, score, high_score):
    font = pygame.font.SysFont("consolas", 20, bold=True)
    text = font.render(f"Score: {score}   Best: {high_score}", True, TEXT_COLOR)
    surface.blit(text, (10, 8))


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Snake — Eat the Apples")
    clock = pygame.time.Clock()

    snake = Snake()
    apple = Apple(snake.body)
    score = 0
    high_score = 0
    fps = FPS_START
    game_over = False
    paused = False

    key_map = {
        pygame.K_UP: UP, pygame.K_w: UP,
        pygame.K_DOWN: DOWN, pygame.K_s: DOWN,
        pygame.K_LEFT: LEFT, pygame.K_a: LEFT,
        pygame.K_RIGHT: RIGHT, pygame.K_d: RIGHT,
    }

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key in key_map and not game_over:
                    snake.set_direction(key_map[event.key])
                elif event.key == pygame.K_p and not game_over:
                    paused = not paused
                elif event.key == pygame.K_r and game_over:
                    snake = Snake()
                    apple = Apple(snake.body)
                    score = 0
                    fps = FPS_START
                    game_over = False
                    paused = False

        if not game_over and not paused:
            snake.move()

            if snake.collides_with_wall() or snake.collides_with_self():
                game_over = True
                high_score = max(high_score, score)
            elif apple.position and snake.head() == apple.position:
                snake.grow(1)
                score += 1
                apple.respawn(snake.body)
                if score % SPEEDUP_EVERY == 0:
                    fps = min(FPS_MAX, fps + 1)

        # ---- draw ----
        screen.fill(BG_COLOR)
        draw_grid(screen)
        draw_apple(screen, apple)
        draw_snake(screen, snake)
        draw_score(screen, score, max(high_score, score))

        if paused and not game_over:
            draw_text_center(screen, "PAUSED", 40)
        if game_over:
            draw_text_center(screen, "GAME OVER", 44, y_offset=-20)
            draw_text_center(screen, "Press R to restart", 22, y_offset=25)

        pygame.display.flip()
        clock.tick(fps)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()