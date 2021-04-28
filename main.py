import pygame
from pygame.locals import *
import time
import random

# Global Variables
GLOBAL_SIZE = 40
BG_COLOR = (110, 110, 5)


class Fruit:
    def __init__(self, screen):
        self.screen = screen
        self.image = pygame.image.load('assets/apple.jpg').convert()
        self.X = 120
        self.Y = 120

    # Draw fruit on screen
    def draw_fruit(self):
        self.screen.blit(self.image, (self.X, self.Y))
        pygame.display.flip()

    # Moving randomly fruit on game screen after snake eat this
    def move(self):
        self.X = random.randint(1, 24) * GLOBAL_SIZE
        self.Y = random.randint(1, 19) * GLOBAL_SIZE


class Snake:
    def __init__(self, screen):
        self.screen = screen
        self.image= pygame.image.load("assets/block.jpg").convert()
        # The direction is the way of the snake that the started the game
        self.direction = "right"
        self.length = 1
        self.X = [40]
        self.Y = [40]

    def move_up(self):
        self.direction ="up"

    def move_down(self):
        self.direction = "down"

    def move_left(self):
        self.direction = "left"

    def move_right(self):
        self.direction = "right"


    def draw_snake(self):
        for i in range(self.length):
            self.screen.blit(self.image, (self.X[i], self.Y[i]))

        pygame.display.flip()

    def get_bigger_snake(self):
        self.length += 1
        self.X.append(-1)
        self.Y.append(-1)

    def moving_snake(self):
        # Updating snake body
        for i in range(self.length-1, 0, -1):
            self.X[i] = self.X[i-1]
            self.Y[i] = self.Y[i-1]

        if self.direction == "up":
            self.Y[0] -= GLOBAL_SIZE
        if self.direction == "down":
            self.Y[0] += GLOBAL_SIZE
        if self.direction == "right":
            self.X[0] += GLOBAL_SIZE
        if self.direction == "left":
            self.X[0] -= GLOBAL_SIZE
        self.draw_snake()


class Game:
    def __init__(self):
        pygame.init()
        # Set the game name
        pygame.display.set_caption('Snake Game')
        pygame.mixer.init()
        # Set the background music
        self.main_music()
        # Adjusting the game window size
        self.surface = pygame.display.set_mode((1000, 800))
        self.snake = Snake(self.surface)
        self.snake.draw_snake()
        self.fruit = Fruit(self.surface)
        self.fruit.draw_fruit()

    def score(self):
        font = pygame.font.SysFont('arial', 30)
        score = font.render(f'Score: {self.snake.length}', True, (255, 255, 255))
        self.surface.blit(score, (800, 10))

    def set_bgImage(self):
        image = pygame.image.load('assets/background.jpg')
        self.surface.blit(image, (0, 0))

    def play_sound(self, path):
        sound = pygame.mixer.Sound(f'assets/{path}.mp3')
        pygame.mixer.Sound.play(sound)

    def main_music(self):
        pygame.mixer.music.load('assets/bg_music.mp3')
        pygame.mixer.music.play()

    # Return start options again
    def reset_game(self):
        self.snake = Snake(self.surface)
        self.fruit = Fruit(self.surface)

    # Check the collision control
    def collision(self, x1, y1, x2, y2):
        if x1 >= x2 and x1 < x2 + GLOBAL_SIZE:
            if y1 >= y2 and y1 < y2 + GLOBAL_SIZE:
                return True
        return False

    def play(self):
        self.set_bgImage()
        self.snake.moving_snake()
        self.fruit.draw_fruit()
        self.score()
        pygame.display.flip()

        # Getting collision with the fruit
        for i in range(self.snake.length):
            if self.collision(self.snake.X[i], self.snake.Y[i], self.fruit.X, self.fruit.Y):
                self.play_sound('ding')
                self.snake.get_bigger_snake()
                self.fruit.move()

        # Getting collision with itself
        for i in range(3, self.snake.length):
            if self.collision(self.snake.X[0], self.snake.Y[0], self.snake.X[i], self.snake.Y[i]):
                self.play_sound('crash')
                raise Exception("Collision !!")

        if not (0 <= self.snake.X[0] <= 1000 and 0 <= self.snake.Y[0] <= 800):
            self.play_sound('crash')
            raise Exception("Error")

    def game_over(self):
        # Set window image again
        self.set_bgImage()
        font = pygame.font.SysFont('arial', 30)
        score_text = font.render(f'Game Over !!  Your Score {self.snake.length}', True, (255, 255, 255))
        self.surface.blit(score_text, (200, 300))
        again_text = font.render('Press Enter To Play Again. To Exit Press ESC', True, (255, 255, 255))
        self.surface.blit(again_text, (200, 350))
        pygame.display.flip()

    def run(self):
        running = True
        pause = False

        # Snake control keys
        while running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False

                    if event.key == K_RETURN:
                        pygame.mixer.music.unpause()
                        pause = False

                    if not pause:
                        if event.key == K_LEFT:
                            self.snake.move_left()
                        if event.key == K_RIGHT:
                            self.snake.move_right()
                        if event.key == K_UP:
                            self.snake.move_up()
                        if event.key == K_DOWN:
                            self.snake.move_down()

                elif event.type == QUIT:
                    running = False
            # Controlling Restart game or quit
            try:
                if not pause:
                    self.play()

            except Exception:
                self.game_over()
                pause = True
                self.reset_game()

            # Snake moving time
            time.sleep(.1)

# Game is Ready
if __name__ == "__main__":
    game = Game()
    game.run()



