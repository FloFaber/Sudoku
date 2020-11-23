import pygame
import pyautogui
from classes import stealgrid
from time import sleep

COLORS = {
    "BLACK": (0, 0, 0),
    "WHITE": (255, 255, 255),
    "RED": (255, 0, 0),
    "BLUE": (0, 0, 255)
}


class Game:

    run = True
    grid = []
    CLOCK = None
    SCREEN = None
    FONT = None
    FPS = 30

    stealer = stealgrid

    WIDTH_GRID, HEIGHT_GRID = 9, 9
    SQUARE_SIZE = 80
    WIDTH_SCREEN = SQUARE_SIZE * WIDTH_GRID
    HEIGHT_SCREEN = SQUARE_SIZE * HEIGHT_GRID

    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Sudoku")
        self.FONT = pygame.font.SysFont('Arial', 25)
        self.SCREEN = pygame.display.set_mode((self.WIDTH_SCREEN, self.HEIGHT_SCREEN))
        self.CLOCK = pygame.time.Clock()
        self.make_grid(False)

    def make_grid(self, fill):
        self.grid = [[0 for i in range(9)] for j in range(9)]
        self.draw()

        if fill:
            pyautogui.click(1000, 380)
            sleep(2)
            pyautogui.click(1090, 620)
            sleep(2)
            self.stealer.steal()
            f = open("grids/1.txt", "r")
            for i in range(9):
                line = f.readline().split(",")
                for j in range(9):
                    self.grid[i][j] = int(line[j].replace("\n", ""))
            f.close()

    def show_grid(self):
        for i in range(len(self.grid)):
            print()
            for j in range(len(self.grid[i])):
                print(self.grid[i][j], end=" ")

    def paint_grid(self):
        for i in range(len(self.grid)):
            for j in range(len(self.grid[i])):

                rect = pygame.Rect(j * self.SQUARE_SIZE, i * self.SQUARE_SIZE, self.SQUARE_SIZE, self.SQUARE_SIZE)

                if self.grid[i][j] != 0:
                    font = self.FONT.render(str(self.grid[i][j]), True, COLORS["BLUE"])
                    self.SCREEN.blit(font, (j * self.SQUARE_SIZE + self.SQUARE_SIZE / 2 - font.get_width() / 2,
                                            i * self.SQUARE_SIZE + self.SQUARE_SIZE / 2 - font.get_height() / 2))

                pygame.draw.rect(self.SCREEN, COLORS["BLACK"], rect, 1)

    def set_num(self, x, y, num):
        self.grid[y][x] = int(num)

    def possible(self, y, x, num):

        for i in range(0, 9):
            if self.grid[y][i] == num:
                return False

        for i in range(0, 9):
            if self.grid[i][x] == num:
                return False

        x0 = (x//3)*3
        y0 = (y//3)*3

        for i in range(0, 3):
            for j in range(0, 3):
                if self.grid[y0+i][x0+j] == num:
                    return False

        return True

    def solve(self):
        for y in range(len(self.grid)):
            for x in range(len(self.grid[y])):
                if self.grid[y][x] == 0:
                    for n in range(1, 10):
                        if self.possible(y, x, n):
                            self.grid[y][x] = n
                            self.draw()
                            self.solve()
                            if not self.solve_done():
                                self.grid[y][x] = 0
                    return
        self.draw()

    def solve_done(self):
        for y in range(len(self.grid)):
            for x in range(len(self.grid[y])):
                if self.grid[y][x] == 0:
                    return False
        return True

    def draw(self):
        self.SCREEN.fill(COLORS["WHITE"])
        self.paint_grid()
        pygame.display.update()

    def loop(self):
        while self.run:

            self.CLOCK.tick(self.FPS)
            self.draw()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run = False
                if event.type == pygame.KEYUP:
                    val = pygame.key.name(event.key)
                    if val == "s":
                        self.solve()
                    elif val == "a":
                        self.show_grid()
                    elif val == "m":
                        self.make_grid(True)
                        self.solve()
                        sleep(3)
                        self.make_grid(True)
                        self.solve()
                        sleep(3)
                        self.make_grid(True)
                        self.solve()
                        sleep(3)
                        self.make_grid(True)
                        self.solve()
                        sleep(3)


if __name__ == "__main__":
    g = Game()
    g.loop()
