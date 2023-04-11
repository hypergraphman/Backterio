from random import randint
import pygame
from copy import deepcopy
from bacteria import Bacteria

PERCENTAGE_OF_FOOD = 10
START_BACTERIA = 50
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
        self.st = 0
        self.end = 40
        self.generator()

    def create_food(self, n):
        for _ in range(n):
            y = randint(0, self.height - 1)
            x = randint(0, self.width - 1)
            if isinstance(self.field[y][x], int):
                self.field[y][x] = FOOD

    def generator(self):
        self.create_food(self.height * self.width * PERCENTAGE_OF_FOOD // 100)
        self.code += 1
        for _ in range(START_BACTERIA):
            chromosome = [[randint(0, 5) for _ in range(4)] for _ in range(8)]
            bacteria = Bacteria(randint(0, self.width - 1), randint(0, self.height - 1),
                                chromosome, self.code, self.field)
            self.all_bacteria.append(bacteria)

    def render(self, scr):
        pygame.draw.rect(scr, 'Yellow', (0, self.st * self.cell_size, len(self.field[0]) * self.cell_size, 40 * self.cell_size))
        if self.st > self.end:
            pygame.draw.rect(scr, 'Yellow',
                             (0, 0, len(self.field[0]) * self.cell_size, self.end * self.cell_size))
        for x in range(self.width):
            for y in range(self.height):
                if self.field[y][x] == FOOD:
                    pygame.draw.ellipse(scr, 'Green', (x * self.cell_size + 1,
                                y * self.cell_size + 1, self.cell_size - 1, self.cell_size - 1))
        for bacteria in self.all_bacteria:
            pygame.draw.rect(scr, bacteria.color, (bacteria.x * self.cell_size + 1,
                        bacteria.y * self.cell_size + 1, self.cell_size - 1, self.cell_size - 1))


    def compare(self, st, end, t):
        return  st < t < end

    def not_compare(self, st, end, t):
        return  end > t or t > st

    def next_move(self):
        self.st += 0.125
        self.end += 0.125
        st = int(self.st) % len(self.field)
        end = int(self.end) % len(self.field)
        if self.st > len(self.field):
            self.st = 0
        if self.end > len(self.field):
            self.end = 0
        if self.st < self.end:
            comp = self.compare
        else:
            comp = self.not_compare
        for bacteria in self.all_bacteria:
            bacteria.move(self.all_bacteria, self.field, 6 if comp(st, end, bacteria.y) else 0)
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
font = pygame.font.Font(None, 24)
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
    score_text = font.render(f'st : {area.st}', True, (0, 0, 0))
    screen.blit(score_text, (10, 10))
    score_text = font.render(f'end: {area.end}', True, (0, 0, 0))
    screen.blit(score_text, (10, 25))
    score_text = font.render(f'bac: {len(area.all_bacteria)}', True, (0, 0, 0))
    screen.blit(score_text, (10, 50))
    pygame.display.flip()
    clock.tick(20)
pygame.quit()