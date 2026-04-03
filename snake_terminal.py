import random
import time
import os
import sys

class TerminalSnake:
    def __init__(self, width=20, height=15):
        self.width = width
        self.height = height
        self.reset_game()
    
    def reset_game(self):
        self.snake = [(self.width // 2, self.height // 2)]
        self.direction = (1, 0)  # Start moving right
        self.food = self.generate_food()
        self.game_over = False
        self.score = 0
    
    def generate_food(self):
        while True:
            x = random.randint(0, self.width - 1)
            y = random.randint(0, self.height - 1)
            food_pos = (x, y)
            if food_pos not in self.snake:
                return food_pos
    
    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def draw(self):
        self.clear_screen()
        
        # Create empty board
        board = [[' ' for _ in range(self.width)] for _ in range(self.height)]
        
        # Place snake
        for i, (x, y) in enumerate(self.snake):
            if 0 <= x < self.width and 0 <= y < self.height:
                board[y][x] = 'O' if i == 0 else 'o'
        
        # Place food
        fx, fy = self.food
        if 0 <= fx < self.width and 0 <= fy < self.height:
            board[fy][fx] = '*'
        
        # Draw border and board
        print('+' + '-' * self.width + '+')
        for row in board:
            print('|' + ''.join(row) + '|')
        print('+' + '-' * self.width + '+')
        
        print(f"Score: {self.score}")
        if self.game_over:
            print("GAME OVER! Press 'r' to restart or 'q' to quit.")
        else:
            print("Use WASD to move, 'q' to quit")
    
    def get_input(self):
        try:
            import msvcrt
            if msvcrt.kbhit():
                return msvcrt.getch().decode('utf-8').lower()
        except ImportError:
            import sys, tty, termios
            fd = sys.stdin.fileno()
            old_settings = termios.tcgetattr(fd)
            try:
                tty.setraw(sys.stdin.fileno())
                if sys.stdin.readable():
                    return sys.stdin.read(1).lower()
            finally:
                termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return None
    
    def update(self, key):
        if self.game_over:
            if key == 'r':
                self.reset_game()
                return True
            elif key == 'q':
                return False
            return True
        
        if key == 'q':
            return False
        elif key == 'w' and self.direction != (0, 1):
            self.direction = (0, -1)
        elif key == 's' and self.direction != (0, -1):
            self.direction = (0, 1)
        elif key == 'a' and self.direction != (1, 0):
            self.direction = (-1, 0)
        elif key == 'd' and self.direction != (-1, 0):
            self.direction = (1, 0)
        
        # Move snake
        head_x, head_y = self.snake[0]
        new_head = (head_x + self.direction[0], head_y + self.direction[1])
        
        # Check wall collision
        if (new_head[0] < 0 or new_head[0] >= self.width or 
            new_head[1] < 0 or new_head[1] >= self.height):
            self.game_over = True
            return True
        
        # Check self collision
        if new_head in self.snake:
            self.game_over = True
            return True
        
        self.snake.insert(0, new_head)
        
        # Check food collision
        if new_head == self.food:
            self.score += 10
            self.food = self.generate_food()
        else:
            self.snake.pop()
        
        return True
    
    def run(self):
        print("Welcome to Terminal Snake Game!")
        print("Use WASD keys to control the snake.")
        time.sleep(2)
        
        running = True
        while running:
            self.draw()
            key = self.get_input()
            if key:
                running = self.update(key)
            time.sleep(0.2)  # Game speed
        
        print("Thanks for playing!")

if __name__ == '__main__':
    try:
        game = TerminalSnake()
        game.run()
    except KeyboardInterrupt:
        print("\nGame interrupted. Thanks for playing!")
