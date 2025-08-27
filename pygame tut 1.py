import pygame
import random

# Initialize pygame
pygame.init()

# Screen dimensions (larger board)
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 800
BLOCK_SIZE = 40

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
CYAN = (0, 255, 255)
YELLOW = (255, 255, 0)
MAGENTA = (255, 0, 255)
ORANGE = (255, 165, 0)
PINK = (255, 105, 180)
LIME = (173, 255, 47)

# Tetromino shapes (classic + new ones)
SHAPES = [
    [[1, 1, 1], [0, 1, 0]],       # T
    [[0, 1, 1], [1, 1, 0]],       # S
    [[1, 1, 0], [0, 1, 1]],       # Z
    [[1, 1, 1, 1]],               # I
    [[1, 1], [1, 1]],             # O
    [[1, 1, 1], [1, 0, 0]],       # L
    [[1, 1, 1], [0, 0, 1]],       # J
    [[1, 1, 1], [0, 1, 0], [0, 1, 0]],  # Plus (+)
    [[1, 0, 1], [1, 1, 1]],       # U
    [[1, 1, 1], [1, 1, 1]],       # Big square (3x3 filled except corners)
]

# Tetromino colors
SHAPE_COLORS = [CYAN, YELLOW, MAGENTA, GREEN, BLUE, ORANGE, RED, PINK, LIME, WHITE]

class Tetromino:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.shape = random.choice(SHAPES)
        self.color = SHAPE_COLORS[SHAPES.index(self.shape)]
        self.rotation = 0

    def image(self):
        return self.shape

    def rotate(self):
        self.shape = [list(row) for row in zip(*self.shape[::-1])]

class Tetris:
    def __init__(self, screen):
        self.screen = screen
        self.cols = SCREEN_WIDTH // BLOCK_SIZE
        self.rows = SCREEN_HEIGHT // BLOCK_SIZE
        self.grid = [[BLACK for _ in range(self.cols)] for _ in range(self.rows)]
        self.current_piece = Tetromino(self.cols // 2 - 2, 0)
        self.next_piece = Tetromino(self.cols // 2 - 2, 0)
        self.score = 0
        self.game_over = False

    def draw_grid(self):
        for y in range(self.rows):
            for x in range(self.cols):
                pygame.draw.rect(self.screen, self.grid[y][x],
                                 (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 0)
                pygame.draw.rect(self.screen, WHITE,
                                 (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 1)

    def draw_piece(self, piece):
        for y, row in enumerate(piece.image()):
            for x, value in enumerate(row):
                if value:
                    pygame.draw.rect(self.screen, piece.color,
                                     ((piece.x + x) * BLOCK_SIZE, (piece.y + y) * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 0)

    def collide(self):
        for y, row in enumerate(self.current_piece.image()):
            for x, value in enumerate(row):
                if value:
                    new_x = self.current_piece.x + x
                    new_y = self.current_piece.y + y
                    if new_x < 0 or new_x >= self.cols or new_y >= self.rows:
                        return True
                    if new_y >= 0 and self.grid[new_y][new_x] != BLACK:
                        return True
        return False

    def freeze(self):
        for y, row in enumerate(self.current_piece.image()):
            for x, value in enumerate(row):
                if value:
                    self.grid[self.current_piece.y + y][self.current_piece.x + x] = self.current_piece.color
        self.clear_lines()
        self.current_piece = self.next_piece
        self.next_piece = Tetromino(self.cols // 2 - 2, 0)
        if self.collide():
            self.game_over = True

    def clear_lines(self):
        lines_cleared = 0
        for i in range(self.rows - 1, -1, -1):
            if all(self.grid[i][j] != BLACK for j in range(self.cols)):
                del self.grid[i]
                self.grid.insert(0, [BLACK for _ in range(self.cols)])
                lines_cleared += 1
        self.score += lines_cleared ** 2

    def move(self, dx):
        self.current_piece.x += dx
        if self.collide():
            self.current_piece.x -= dx

    def drop(self):
        self.current_piece.y += 1
        if self.collide():
            self.current_piece.y -= 1
            self.freeze()

    def hard_drop(self):
        while not self.collide():
            self.current_piece.y += 1
        self.current_piece.y -= 1
        self.freeze()

    def rotate(self):
        old_shape = self.current_piece.shape
        self.current_piece.rotate()
        if self.collide():
            self.current_piece.shape = old_shape

    def run(self):
        clock = pygame.time.Clock()
        while not self.game_over:
            self.screen.fill(BLACK)
            self.draw_grid()
            self.draw_piece(self.current_piece)
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game_over = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.move(-1)
                    if event.key == pygame.K_RIGHT:
                        self.move(1)
                    if event.key == pygame.K_DOWN:
                        self.drop()
                    if event.key == pygame.K_UP:
                        self.rotate()
                    if event.key == pygame.K_SPACE:
                        self.hard_drop()

            # ⚠️ Removed automatic self.drop(), so blocks move only when you press keys
            clock.tick(15)

# Main
def main():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Complex Tetris')

    game = Tetris(screen)
    game.run()

    print("Game Over! Final Score:", game.score)
    pygame.quit()

if __name__ == '__main__':
    main()