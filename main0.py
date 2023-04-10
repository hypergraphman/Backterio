from random import randint
import pygame
from copy import deepcopy

MAX_LIFETIME = 1000
MIN_LIFETIME = 500
MAX_ENERGY = 400
MIN_ENERGY = 100
MIN_PHOTOSYNTHESIS = 0
MAX_PHOTOSYNTHESIS = 1
PERCENTAGE_OF_FOOD = 10
START_BACTERIA = 10
EDA = 1000
FOOD = 10
RULES = [[(randint(-1, 1), randint(-1, 1)),
          (randint(-1, 1), randint(-1, 1)),
          (randint(-1, 1), randint(-1, 1)),
          (randint(-1, 1), randint(-1, 1)),
          (randint(-1, 1), randint(-1, 1)),
          (randint(-1, 1), randint(-1, 1)),
          (randint(-1, 1), randint(-1, 1)),
          (randint(-1, 1), randint(-1, 1)),
          (randint(-1, 1), randint(-1, 1))],
         randint(MIN_LIFETIME, MAX_LIFETIME),
         randint(MIN_ENERGY, MAX_ENERGY)]
WIDTH = 253
HEIGHT = 133


class Bacteria:
    def __init__(self, x, y, rules, code, field):
        super().__init__()
        self.code = code + 1
        self.x = x
        self.y = y
        field[y][x] = self
        self.rules = deepcopy(rules)
        self.max_energy = self.rules[2]
        self.energy = self.max_energy // 2
        self.lifetime = self.rules[1]
        self.moves = rules[0]
        if randint(0, 7) == 0:
            rule = randint(0, 10)
            if rule == 1:
                self.lifetime += randint(-1, 10)
            elif rule == 2:
                self.max_energy += randint(-1, 10)
            else:
                self.moves[randint(0, len(self.moves) - 1)] = (randint(-1, 1), randint(-1, 1))
        self.current_move = 0
        self.is_alive = True

    def move(self, all_bacteria, field):
        self.lifetime -= 1
        self.energy += 0.7
        if self.energy >= self.max_energy:
            b1 = Bacteria((self.x + randint(-3, 3)) % WIDTH, (self.y + randint(-3, 3)) % HEIGHT,
                          self.rules, self.code, field)
            b2 = Bacteria((self.x + randint(-3, 3)) % WIDTH, (self.y + randint(-3, 3)) % HEIGHT,
                          self.rules, self.code, field)
            all_bacteria += [b1, b2]
            self.is_alive = False
        if self.lifetime <= 0 or self.energy <= 0:
            self.is_alive = False
            pass
        elif self.is_alive:
            self.x = (self.x + self.moves[self.current_move][0]) % WIDTH
            self.y = (self.y + self.moves[self.current_move][1]) % HEIGHT
            self.energy -= abs(self.moves[self.current_move][0]) + abs(self.moves[self.current_move][1])
            self.current_move = (self.current_move + 1) % len(self.moves)


class Area:
    def __init__(self, width, height, cell_size):
        self.width = width
        self.height = height
        self.cell_size = cell_size
        self.all_bacteria = []
        self.field = [[0] * width for _ in range(height)]
        self.code = 0
        self.generator()

    def create_food(self, n):
        for _ in range(n):
            self.field[randint(0, self.height - 1)][randint(0, self.width - 1)] = FOOD

    def generator(self):
        self.create_food(self.height * self.width * PERCENTAGE_OF_FOOD // 100)
        self.code += 1
        for _ in range(START_BACTERIA):
            bacteria = Bacteria(randint(0, self.width - 1), randint(0, self.height - 1),
                                RULES, self.code, self.field)
            self.all_bacteria.append(bacteria)

    def render(self, scr):
        for x in range(self.width):
            for y in range(self.height):
                if self.field[y][x] == FOOD:
                    pygame.draw.ellipse(scr, 'Green', (x * self.cell_size + 1,
                                y * self.cell_size + 1, self.cell_size - 1, self.cell_size - 1))
        for bacteria in self.all_bacteria:
            pygame.draw.rect(scr, 'Red', (bacteria.x * self.cell_size + 1,
                        bacteria.y * self.cell_size + 1, self.cell_size - 1, self.cell_size - 1))

    def next_move(self):
        for bacteria in self.all_bacteria:
            self.field[bacteria.y][bacteria.x] = 0
            bacteria.move(self.all_bacteria, self.field)
            if isinstance(self.field[bacteria.y][bacteria.x], int):
                bacteria.energy += self.field[bacteria.y][bacteria.x]
            elif self.field[bacteria.y][bacteria.x] != bacteria and abs(bacteria.code - self.field[bacteria.y][bacteria.x].code) > 3:
                if self.field[bacteria.y][bacteria.x].energy - bacteria.energy > 10:
                    bacteria.is_alive = False
                elif self.field[bacteria.y][bacteria.x].energy - bacteria.energy < 10:
                    self.field[bacteria.y][bacteria.x].is_alive = False
                else:
                    bacteria.is_alive = False
                    self.field[bacteria.y][bacteria.x].is_alive = False
            self.field[bacteria.y][bacteria.x] = bacteria

        for i in range(len(self.all_bacteria) - 1, -1, -1):
            if not self.all_bacteria[i].is_alive:
                b = self.all_bacteria.pop(i)
                self.field[b.y][b.x] = FOOD
        self.create_food(self.height * self.width // EDA)


pygame.init()

w, h = WIDTH, HEIGHT
cell_size = 5
screen = pygame.display.set_mode([cell_size * w, cell_size * h])
pygame.display.set_caption('Backterio')
area = Area(w, h, cell_size)
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill('White')
    area.render(screen)
    area.next_move()
    pygame.display.flip()
pygame.quit()