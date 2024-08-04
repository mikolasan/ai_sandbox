import pygame
import math
import random
from enum import Enum
from collections import namedtuple
import numpy as np
import torch

ENABLE_WINDOW = False

class Direction(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4

Point = namedtuple('Point', 'x, y')

# rgb colors
WHITE = (255, 255, 255)
RED = (200,0,0)
BLUE1 = (0, 0, 255)
BLUE2 = (0, 100, 255)
BLACK = (0,0,0)

BOARD_SIZE = 12
BLOCK_SIZE = 20
SPEED = 20

class SnakeGameAI:

    def __init__(self, device, w=BOARD_SIZE*BLOCK_SIZE, h=BOARD_SIZE*BLOCK_SIZE): # original values = w= 640, h= 480
        self.device = device
        self.board_shape = (BOARD_SIZE, BOARD_SIZE)
        self.w = w
        self.h = h
        self.head = Point(0,0)
        self.snake = []
        self.score = 0
        self.food = None
        
        self.reset()
        
        # init display
        if ENABLE_WINDOW:
            pygame.init()
            self.font = pygame.font.Font('arial.ttf', 25)
            self.display = pygame.display.set_mode((self.w, self.h))
            pygame.display.set_caption('Snake')
            self.clock = pygame.time.Clock()


    def reset(self):
        # init game state
        self.direction = Direction.RIGHT

        self.head = Point(self.w/2, self.h/2)
        self.snake = [self.head,
                      Point(self.head.x-BLOCK_SIZE, self.head.y),
                      Point(self.head.x-(2*BLOCK_SIZE), self.head.y)]

        self.score = 0
        self.food = None
        self._place_food()
        self.frame_iteration = 0


    def _place_food(self):
        x = random.randint(0, BOARD_SIZE - 1) * BLOCK_SIZE
        y = random.randint(0, BOARD_SIZE - 1) * BLOCK_SIZE
        self.food = Point(x, y)
        if self.food in self.snake:
            self._place_food()


    def get_action(self):
        straight = self._move(torch.tensor([1,0,0]))
        right = self._move(torch.tensor([0,1,0]))
        left = self._move(torch.tensor([0,0,1]))
        
        straight_dist = (self.food.x - straight.x)**2 + (self.food.y - straight.y)**2
        right_dist = (self.food.x - right.x)**2 + (self.food.y - right.y)**2
        left_dist = (self.food.x - left.x)**2 + (self.food.y - left.y)**2
        
        dist = torch.tensor([straight_dist, right_dist, left_dist])
        if self.is_collision(straight):
            dist[0] = math.inf
        if self.is_collision(right):
            dist[1] = math.inf
        if self.is_collision(left):
            dist[2] = math.inf
        
        dir_id = torch.argmin(dist).item()
        if dir_id == 0:
            a = torch.tensor([1,0,0], device=self.device)
        elif dir_id == 1:
            a = torch.tensor([0,1,0], device=self.device)
        elif dir_id == 2:
            a = torch.tensor([0,0,1], device=self.device)
        else:
            print('else case')
            a = torch.tensor([1,0,0], device=self.device)
        return a
            

    def calc_value(self, action):
        moved = self._move(action) # update the head
        if moved:
            self.snake.insert(0, self.head)
        reward = 0 #was 0
        if not moved:
            reward = -10.0
            return reward, game_over, self.score

        if self.head == self.food:
            reward = 10.0
        else:
            reward = 1.0
            
        
    def play_step(self, action):
        self.frame_iteration += 1
        # 1. collect user input
        if ENABLE_WINDOW:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

        reward = 0 #was 0
        game_over = False
        
        # 2. move
        new_pos = self._move(action) # update the head
        if not self.is_collision(new_pos):
            self.head = new_pos
            self.snake.insert(0, self.head)
        else:
            game_over = True
            reward = -1.0
            
            # 5. update ui and clock
            if ENABLE_WINDOW:
                self._update_ui()
                self.clock.tick(SPEED)
            return reward, game_over, self.score

        # 4. place new food or just move
        if self.head == self.food:
            self.score += 1
            reward = 1.0
            self._place_food()
        else:
            self.snake.pop()
            reward = -0.01 #min(-1.0, -0.1 * self.frame_iteration + self.score * 20)
        
        # 5. update ui and clock
        if ENABLE_WINDOW:
            self._update_ui()
            self.clock.tick(SPEED)
        
        # 6. return game over and score
        return reward, game_over, self.score

    def is_collision(self, pt=None):
        if pt is None:
            pt = self.head
        # hits boundary
        if pt.x > self.w - BLOCK_SIZE or pt.x < 0 or pt.y > self.h - BLOCK_SIZE or pt.y < 0:
            return True
        # hits itself
        if pt in self.snake[1:]:
            return True

        return False

    def _update_ui(self):
        self.display.fill(BLACK)

        for pt in self.snake:
            pygame.draw.rect(self.display, BLUE1, pygame.Rect(pt.x, pt.y, BLOCK_SIZE, BLOCK_SIZE))
            pygame.draw.rect(self.display, BLUE2, pygame.Rect(pt.x+4, pt.y+4, 12, 12))

        pygame.draw.rect(self.display, RED, pygame.Rect(self.food.x, self.food.y, BLOCK_SIZE, BLOCK_SIZE))

        text = self.font.render("Score: " + str(self.score), True, WHITE)
        self.display.blit(text, [0, 0])
        pygame.display.flip()

    def _move(self, action):
        # [straight, right, left]

        clock_wise = [Direction.RIGHT, Direction.DOWN, Direction.LEFT, Direction.UP]
        idx = clock_wise.index(self.direction)

        action_id = torch.argmax(action).item()
        # straight
        if action_id == 0:
            new_dir = clock_wise[idx] # no change
        # right
        elif action_id == 1:
            next_idx = (idx + 1) % 4
            new_dir = clock_wise[next_idx] # right turn r -> d -> l -> u
        # left
        else: # [0, 0, 1]
            next_idx = (idx - 1) % 4
            new_dir = clock_wise[next_idx] # left turn r -> u -> l -> d

        self.direction = new_dir

        x = self.head.x
        y = self.head.y
        if self.direction == Direction.RIGHT:
            x += BLOCK_SIZE
        elif self.direction == Direction.LEFT:
            x -= BLOCK_SIZE
        elif self.direction == Direction.DOWN:
            y += BLOCK_SIZE
        elif self.direction == Direction.UP:
            y -= BLOCK_SIZE
        
        p = Point(x, y)
        return p
   
    def get_current_state(self) -> torch.Tensor:
        # apple
        # apple_coord = (int(self.food.y // BLOCK_SIZE), int(self.food.x // BLOCK_SIZE))
        # print(f'apple {apple_coord}')
        # board[apple_coord[0]][apple_coord[1]] = 1.0
        # snake's head
        # head_coord = (int(self.head.y // BLOCK_SIZE), int(self.head.x // BLOCK_SIZE))
        # print(f'head {head_coord}')
        # board[head_coord[0], head_coord[1]] = 0.5
        # body
        # for part in self.snake[1:]:
            # snake_coord = (int(part.y // BLOCK_SIZE), int(part.x // BLOCK_SIZE))
        #     # print(f'snake {snake_coord}')
            # board[snake_coord[0], snake_coord[1]] = 0.5
        # print(f'board {board}')
        
        # dx = BOARD_SIZE + apple_coord[0] - head_coord[0]
        # dy = BOARD_SIZE + apple_coord[1] - head_coord[1]
        # board[dx][dy] = 1.0
        # board[0] = apple_coord[0] - head_coord[0]
        # board[1] = apple_coord[1] - head_coord[1]
        
        pos = self.head
        dx = (pos[0] - self.food[0]) / BLOCK_SIZE
        dy = (pos[1] - self.food[1]) / BLOCK_SIZE
        wall_left = 1.0 if pos[0] - 1 < 0 else 0.0
        wall_right = 1.0 if pos[0] + 1 < 0 else 0.0
        wall_up = 1.0 if pos[1] - 1 >= BOARD_SIZE else 0.0
        wall_down = 1.0 if pos[1] + 1 >= BOARD_SIZE else 0.0
        tail_left = 1.0 if Point(pos[0] - 1, pos[1]) in self.snake[1:] else 0.0
        tail_right = 1.0 if Point(pos[0] + 1, pos[1]) in self.snake[1:] else 0.0
        tail_up = 1.0 if Point(pos[0], pos[1] - 1) in self.snake[1:] else 0.0
        tail_down = 1.0 if Point(pos[0], pos[1] + 1) in self.snake[1:] else 0.0
        state = [dx, dy,
                 wall_left, wall_right, wall_up, wall_down,
                 tail_left, tail_right, tail_up, tail_down]
        return torch.tensor(state, device=self.device)
    