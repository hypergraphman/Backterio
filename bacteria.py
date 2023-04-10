from random import randint
# import pygame
from copy import deepcopy

MAX_LIFETIME = 500
MIN_LIFETIME = 500
MAX_ENERGY = 200
MIN_ENERGY = 100
NORTH = 0
WEST = 1
SOUTH = 2
EAST = 3

N_DIRECTION = 4


class Bacteria:
    def __init__(self, x, y, chromosome, code, field):
        self.code = code + 1
        self.direction = NORTH
        self.x = x
        self.y = y
        field[y][x] = self
        self.chromosome = chromosome
        self.max_energy = MAX_ENERGY
        self.energy = self.max_energy // 3 * 2
        self.lifetime = MAX_LIFETIME
        self.is_alive = True
        s = 0
        for i in chromosome:
            s = s * 8 + sum(i)
        self.color = s % 256**3 - 100 * 256**2 - 100 * 256
        # self.color = 'Red'

    def move(self, all_bacteria, field):
        field[self.y][self.x] = 0

        self.lifetime -= 1
        self.energy += 1 + (6 if 100 < self.y < 110 else 0)
        # Деление
        if self.energy >= self.max_energy:
            for _ in range(2):
                chromosome = deepcopy(self.chromosome)
                if randint(1, 10) == 1:
                    chromosome[randint(0, 7)][randint(0, 3)] = randint(0, 5)
                b1 = Bacteria((self.x + randint(-3, 3)) % len(field[0]), (self.y + randint(-3, 3)) % len(field),
                              chromosome, self.code, field)
                all_bacteria.append(b1)
            self.is_alive = False
        elif self.lifetime <= 0 or self.energy <= 0:
            self.is_alive = False
            pass
        elif self.is_alive:
            m = 0
            if self.direction == NORTH:
                y = (self.y - 1) % len(field)
                for x in (self.x - 1) % len(field[0]), self.x, (self.x + 1) % len(field[0]):
                    m *= 2
                    if isinstance(field[y][x], int):
                        m += 1
            if self.direction == WEST:
                x = (self.x - 1) % len(field[0])
                for y in (self.y - 1) % len(field), self.y, (self.y + 1) % len(field):
                    m *= 2
                    if isinstance(field[y][x], int):
                        m += 1
            if self.direction == SOUTH:
                y = (self.y + 1) % len(field)
                for x in (self.x - 1) % len(field[0]), self.x, (self.x + 1) % len(field[0]):
                    m *= 2
                    if isinstance(field[y][x], int):
                        m += 1
            if self.direction == EAST:
                x = (self.x + 1) % len(field[0])
                for y in (self.y - 1) % len(field), self.y, (self.y + 1) % len(field):
                    m *= 2
                    if isinstance(field[y][x], int):
                        m += 1

            for move in self.chromosome[m]:
                # разворот влево
                if move == 1:
                    self.direction = (self.direction + 1) % N_DIRECTION
                # разворот направо
                elif move == 2:
                    self.direction = (self.direction - 1) % N_DIRECTION
                # left
                elif move == 3:
                    if self.direction == NORTH:
                        self.y = (self.y - 1) % len(field)
                        self.x = (self.x - 1) % len(field[0])
                    elif self.direction == WEST:
                        self.y = (self.y + 1) % len(field)
                        self.x = (self.x - 1) % len(field[0])
                    elif self.direction == SOUTH:
                        self.y = (self.y + 1) % len(field)
                        self.x = (self.x + 1) % len(field[0])
                    elif self.direction == EAST:
                        self.y = (self.y - 1) % len(field)
                        self.x = (self.x + 1) % len(field[0])
                # forward
                elif move == 4:
                    if self.direction == NORTH:
                        self.y = (self.y - 1) % len(field)
                        # self.x = (self.x - 1) % len(field[0])
                    elif self.direction == WEST:
                        # self.y = (self.y + 1) % len(field)
                        self.x = (self.x - 1) % len(field[0])
                    elif self.direction == SOUTH:
                        self.y = (self.y + 1) % len(field)
                        # self.x = (self.x + 1) % len(field[0])
                    elif self.direction == EAST:
                        # self.y = (self.y - 1) % len(field)
                        self.x = (self.x + 1) % len(field[0])
                # right
                elif move == 5:
                    if self.direction == NORTH:
                        self.y = (self.y - 1) % len(field)
                        self.x = (self.x + 1) % len(field[0])
                    elif self.direction == WEST:
                        self.y = (self.y - 1) % len(field)
                        self.x = (self.x - 1) % len(field[0])
                    elif self.direction == SOUTH:
                        self.y = (self.y + 1) % len(field)
                        self.x = (self.x - 1) % len(field[0])
                    elif self.direction == EAST:
                        self.y = (self.y + 1) % len(field)
                        self.x = (self.x + 1) % len(field[0])
                if isinstance(field[self.y][self.x], int):
                    self.energy += field[self.y][self.x]
                    field[self.y][self.x] = 0
                else:
                    b = field[self.y][self.x]
                    if abs(b.energy - self.energy) < 10:
                        if randint(1, 5) == 1:
                            for i in range(len(self.chromosome)):
                                self.chromosome[i] = self.chromosome[i] if randint(0, 1) else b.chromosome[i]
                            self.lifetime = MAX_LIFETIME
                            b.is_alive = False
                    elif b.energy < self.energy:
                        self.energy += 10
                        b.is_alive = False
                    else:
                        b.energy += 10
                        self.is_alive = False
                        break
                self.energy -= 1
            field[self.y][self.x] = self

            # self.x = (self.x + self.moves[self.current_move][0]) % WIDTH
            # self.y = (self.y + self.moves[self.current_move][1]) % HEIGHT
                 # abs(self.moves[self.current_move][0]) + abs(self.moves[self.current_move][1])
            # self.current_move = (self.current_move + 1) % len(self.moves)
