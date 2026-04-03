import pygame
import sys
import random
import math

class SnakeGame:
    def __init__(self):
        pygame.init()
        self.width = 800
        self.height = 600
        self.cell_size = 20
        self.fps = 10
        
        # Colors
        self.black = (0, 0, 0)
        self.white = (255, 255, 255)
        self.green = (0, 255, 0)
        self.red = (255, 0, 0)
        self.blue = (0, 100, 255)
        
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption('贪吃蛇游戏')
        self.clock = pygame.time.Clock()
        
        self.reset_game()
    
    def reset_game(self):
        self.snake = [(self.width // 2, self.height // 2)]
        self.direction = (self.cell_size, 0)  # Start moving right
        self.food = self.generate_food()
        self.game_over = False
        self.score = 0
    
    def generate_food(self):
        while True:
            x = random.randint(0, (self.width - self.cell_size) // self.cell_size) * self.cell_size
            y = random.randint(0, (self.height - self.cell_size) // self.cell_size) * self.cell_size
            food_pos = (x, y)
            if food_pos not in self.snake:
                return food_pos
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if self.game_over:
                    if event.key == pygame.K_r:
                        self.reset_game()
                    elif event.key == pygame.K_q:
                        return False
                else:
                    if event.key == pygame.K_UP and self.direction != (0, self.cell_size):
                        self.direction = (0, -self.cell_size)
                    elif event.key == pygame.K_DOWN and self.direction != (0, -self.cell_size):
                        self.direction = (0, self.cell_size)
                    elif event.key == pygame.K_LEFT and self.direction != (self.cell_size, 0):
                        self.direction = (-self.cell_size, 0)
                    elif event.key == pygame.K_RIGHT and self.direction != (-self.cell_size, 0):
                        self.direction = (self.cell_size, 0)
        return True
    
    def update(self):
        if self.game_over:
            return
            
        # Move snake
        head_x, head_y = self.snake[0]
        new_head = (head_x + self.direction[0], head_y + self.direction[1])
        
        # Check wall collision
        if (new_head[0] < 0 or new_head[0] >= self.width or 
            new_head[1] < 0 or new_head[1] >= self.height):
            self.game_over = True
            return
        
        # Check self collision
        if new_head in self.snake:
            self.game_over = True
            return
            
        self.snake.insert(0, new_head)
        
        # Check food collision
        if new_head == self.food:
            self.score += 10
            self.food = self.generate_food()
            # Increase speed slightly with score
            self.fps = min(20, 10 + self.score // 50)
        else:
            self.snake.pop()
    
    def draw(self):
        self.screen.fill(self.black)
        
        # Draw snake
        for i, segment in enumerate(self.snake):
            color = self.green if i == 0 else (0, 200, 0)  # Head is brighter green
            pygame.draw.rect(self.screen, color, 
                           pygame.Rect(segment[0], segment[1], self.cell_size, self.cell_size))
            pygame.draw.rect(self.screen, self.white, 
                           pygame.Rect(segment[0], segment[1], self.cell_size, self.cell_size), 1)
        
        # Draw food
        pygame.draw.rect(self.screen, self.red, 
                       pygame.Rect(self.food[0], self.food[1], self.cell_size, self.cell_size))
        pygame.draw.circle(self.screen, self.blue, 
                         (self.food[0] + self.cell_size//2, self.food[1] + self.cell_size//2), 
                         self.cell_size//3)
        
        # Draw score
        font = pygame.font.Font(None, 36)
        score_text = font.render(f'Score: {self.score}', True, self.white)
        self.screen.blit(score_text, (10, 10))
        
        # Draw game over message
        if self.game_over:
            font_large = pygame.font.Font(None, 72)
            game_over_text = font_large.render('GAME OVER', True, self.red)
            restart_text = font.render('Press R to Restart or Q to Quit', True, self.white)
            
            self.screen.blit(game_over_text, 
                           (self.width//2 - game_over_text.get_width()//2, 
                            self.height//2 - game_over_text.get_height()//2))
            self.screen.blit(restart_text, 
                           (self.width//2 - restart_text.get_width()//2, 
                            self.height//2 + 50))
        
        pygame.display.flip()
    
    def run(self):
        running = True
        while running:
            running = self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(self.fps)
        
        pygame.quit()
        sys.exit()

if __name__ == '__main__':
    game = SnakeGame()
    game.run()
