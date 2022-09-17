import sys
import pygame
from pygame.locals import *
from pygame.math import Vector2 as VEC
from random import *

WIDTH, HEIGHT = 800, 600
CELL_SIZE = 10
NUM_OF_CELLS = WIDTH // CELL_SIZE, HEIGHT // CELL_SIZE
NEIGHBORS = {(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, 1), (1, -1)}

inttup = lambda tup: (int(tup[0]), int(tup[1]))
wrap_cells = lambda tup: (tup[0] % NUM_OF_CELLS[0], tup[1] % NUM_OF_CELLS[1])
get_neighbors = lambda cell_pos: sum([Cell.grid[pos].state for neighbor in NEIGHBORS if (pos := inttup(cell_pos + neighbor)) in Cell.grid])
get_neighbors_wrap = lambda cell_pos: sum([Cell.grid[wrap_cells(inttup(cell_pos + neighbor))].state for neighbor in NEIGHBORS])

gun = {(23, 4), (14, 4), (27, 1), (37, 3), (4, 6), (19, 6), (27, 7), (17, 6), (13, 5), (24, 5), (38, 4), (18, 4), (23, 3), (4, 5), (27, 6), (3, 6), (19, 5), (24, 4), (13, 7), (25, 6), (16, 3), (16, 9), (38, 3), (20, 6), (23, 5), (37, 4), (3, 5), (27, 2), (14, 8), (19, 7), (25, 2), (24, 3), (13, 6), (15, 3), (15, 9), (18, 8)}

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT), DOUBLEBUF | HWSURFACE)
clock = pygame.time.Clock()

class Cell:
    grid = {}
    changed = {}

    def __init__(self, pos, state) -> None:
        self.pos = VEC(pos)
        self.__class__.grid[inttup(self.pos)] = self
        self.state = state
        self.new_state = self.state

    def update(self) -> None:
        neighbors = (get_neighbors_wrap if wrap else get_neighbors)(self.pos)
        self.new_state = not (neighbors < 2 or neighbors > 3) if self.state else neighbors == 3

    def draw(self) -> None:
        if self.state:
            pygame.draw.rect(screen, (0, 0, 0), ((self.pos * CELL_SIZE), (CELL_SIZE,) * 2))
        else:
            pygame.draw.rect(screen, (200, 200, 200), ((self.pos * CELL_SIZE), (CELL_SIZE + 1,) * 2), 1)

for x in range(NUM_OF_CELLS[0]):
    for y in range(NUM_OF_CELLS[1]):
        # Cell((x, y), bool(randint(0, 2)))
        Cell((x, y), True if (x, y) in gun else False)

fps = 30
wrap = False
pause = True
running = True
while running:
    clock.tick_busy_loop(fps)
    pygame.display.set_caption(f"Conway's GOL Pygame | Intended FPS: {fps} | Actual FPS: {round(clock.get_fps())} | Paused: {pause} | Wrap: {wrap}")

    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        elif event.type == KEYDOWN:
            if event.key == K_SPACE:
                pause = not pause
            elif event.key == K_RETURN:
                for cell in Cell.grid.values():
                    cell.update()
            elif event.key == K_s:
                active = set()
                for cell in Cell.grid.values():
                    if cell.state:
                        active.add(inttup(cell.pos))
                print(active)
            elif event.key == K_w:
                wrap = not wrap
        elif event.type == MOUSEBUTTONDOWN:
            if event.button == 1:
                mpos = VEC(pygame.mouse.get_pos())
                cell_pos = mpos // CELL_SIZE
                held_state = Cell.grid[inttup(cell_pos)].state
            elif event.button == 4:
                fps += 1
            elif event.button == 5:
                fps -= 1

    if pygame.mouse.get_pressed()[0]:
        mpos = VEC(pygame.mouse.get_pos())
        cell_pos = mpos // CELL_SIZE
        Cell.grid[inttup(cell_pos)].new_state = not held_state

    screen.fill((255, 255, 255))
    
    for cell in Cell.grid.values():
        if not pause:
            cell.update()
        cell.draw()
    for cell in Cell.grid.values():
        cell.state = cell.new_state

    pygame.display.flip()

pygame.quit()
sys.exit()