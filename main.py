from random import randint
import pygame
from copy import deepcopy
from bacteria import Bacteria

PERCENTAGE_OF_FOOD = 100
START_BACTERIA = 10
EDA = 10000
FOOD = 10
WIDTH = 253
HEIGHT = 131
cell_size = 5
clock = pygame.time.Clock()

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
            chromosome = [[randint(0, 5) for _ in range(4)] for _ in range(8)]
            bacteria = Bacteria(randint(0, self.width - 1), randint(0, self.height - 1),
                                chromosome, self.code, self.field)
            self.all_bacteria.append(bacteria)

    def render(self, scr):
        for x in range(self.width):
            for y in range(self.height):
                if self.field[y][x] == FOOD:
                    pygame.draw.ellipse(scr, 'Green', (x * self.cell_size + 1,
                                y * self.cell_size + 1, self.cell_size - 1, self.cell_size - 1))
        for bacteria in self.all_bacteria:
            pygame.draw.rect(scr, bacteria.color, (bacteria.x * self.cell_size + 1,
                        bacteria.y * self.cell_size + 1, self.cell_size - 1, self.cell_size - 1))

    def next_move(self):
        for bacteria in self.all_bacteria:
            bacteria.move(self.all_bacteria, self.field)
            # if isinstance(self.field[bacteria.y][bacteria.x], int):
            #     bacteria.energy += self.field[bacteria.y][bacteria.x]
            # elif self.field[bacteria.y][bacteria.x] != bacteria and abs(bacteria.code - self.field[bacteria.y][bacteria.x].code) > 3:
            #     if self.field[bacteria.y][bacteria.x].energy - bacteria.energy > 10:
            #         bacteria.is_alive = False
            #     elif self.field[bacteria.y][bacteria.x].energy - bacteria.energy < 10:
            #         self.field[bacteria.y][bacteria.x].is_alive = False
            #     else:
            #         bacteria.is_alive = False
            #         self.field[bacteria.y][bacteria.x].is_alive = False
            # self.field[bacteria.y][bacteria.x] = bacteria

        for i in range(len(self.all_bacteria) - 1, -1, -1):
            if not self.all_bacteria[i].is_alive:
                b = self.all_bacteria.pop(i)
                self.field[b.y][b.x] = FOOD
        self.create_food(self.height * self.width // EDA)


pygame.init()

w, h = WIDTH, HEIGHT
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
    clock.tick(20)
pygame.quit()