import pygame
import random
import asyncio
import platform

# 初始化 Pygame
pygame.init()

# 遊戲設置
WIDTH = 800
HEIGHT = 600
GRID_SIZE = 20
GRID_WIDTH = WIDTH // GRID_SIZE
GRID_HEIGHT = HEIGHT // GRID_SIZE
FPS = 10

# 顏色定義
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

# 蛇和食物的初始設置
class Snake:
    def __init__(self):
        self.positions = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = (1, 0)  # 初始向右
        self.length = 1

    def get_head_position(self):
        return self.positions[0]

    def update(self):
        cur = self.get_head_position()
        x, y = self.direction
        new = ((cur[0] + x) % GRID_WIDTH, (cur[1] + y) % GRID_HEIGHT)
        if new in self.positions[2:]:
            return False  # 撞到自己
        self.positions.insert(0, new)
        if len(self.positions) > self.length:
            self.positions.pop()
        return True

    def reset(self):
        self.positions = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = (1, 0)
        self.length = 1

class Food:
    def __init__(self):
        self.position = (0, 0)
        self.randomize_position()

    def randomize_position(self):
        self.position = (random.randint(0, GRID_WIDTH-1), random.randint(0, GRID_HEIGHT-1))

# 設置遊戲窗口
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("貪食蛇遊戲")
clock = pygame.time.Clock()

# 字體設置
font = pygame.font.SysFont(None, 36)

# 遊戲變量
snake = Snake()
food = Food()
score = 0
game_over = False

def setup():
    global snake, food, score, game_over
    snake = Snake()
    food = Food()
    score = 0
    game_over = False

def draw():
    screen.fill(BLACK)
    # 畫蛇
    for pos in snake.positions:
        pygame.draw.rect(screen, GREEN, (pos[0] * GRID_SIZE, pos[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE))
    # 畫食物
    pygame.draw.rect(screen, RED, (food.position[0] * GRID_SIZE, food.position[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE))
    # 顯示分數
    score_text = font.render(f"分數: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))
    # 顯示遊戲結束
    if game_over:
        game_over_text = font.render("遊戲結束! 按R重新開始", True, WHITE)
        screen.blit(game_over_text, (WIDTH//2 - 150, HEIGHT//2))
    pygame.display.flip()

async def main():
    global snake, food, score, game_over
    setup()
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and snake.direction != (0, 1):
                    snake.direction = (0, -1)
                elif event.key == pygame.K_DOWN and snake.direction != (0, -1):
                    snake.direction = (0, 1)
                elif event.key == pygame.K_LEFT and snake.direction != (1, 0):
                    snake.direction = (-1, 0)
                elif event.key == pygame.K_RIGHT and snake.direction != (-1, 0):
                    snake.direction = (1, 0)
                elif event.key == pygame.K_r and game_over:
                    setup()

        if not game_over:
            # 更新蛇的位置
            if not snake.update():
                game_over = True
            # 檢查是否吃到食物
            if snake.get_head_position() == food.position:
                snake.length += 1
                score += 1
                food.randomize_position()
            
            draw()
        
        clock.tick(FPS)
        await asyncio.sleep(1.0 / FPS)

if platform.system() == "Emscripten":
    asyncio.ensure_future(main())
else:
    if __name__ == "__main__":
        asyncio.run(main())


    