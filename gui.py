from demineur import Demineur
from consts import *
import pygame as pg
import pygame.locals
import math

class MyFrame():

    def __init__(self, master_, game=None):
        self.master = master_
        self.win = self.master.win
        self.colors = [(0,0,0), (0,0,0), (15, 137, 216), (27, 189, 88), (189, 46, 27), (17, 13, 119), (199, 58, 128), (236, 184, 24), (255, 0, 39), (0, 0, 0)]

        self.game = Demineur(difficulty=2) if game == None else game
        self.game.new_game()

        self.w = self.master.w
        self.h = self.master.h

    def draw_grid(self):
        myfont = pygame.font.SysFont('Comic Sans MS', int(CASE_SIZE*0.5))
        self.win.fill((235, 235, 235))

        width = CASE_SIZE * GRID_WIDTH + CASE_BORDER * (GRID_WIDTH+1)
        height = CASE_SIZE * GRID_HEIGHT + CASE_BORDER * (GRID_HEIGHT+1)

        x = (self.w - width)/2
        y = (self.h - height)/2

        rect = pg.Rect(x, y, width, height)
        pg.draw.rect(self.win, (255,255,255), rect)

        for i in range(GRID_WIDTH):
            for j in range(GRID_HEIGHT):
                if self.game.board_discovered[i][j] == 1 and self.game.board[i][j] != -1:
                    posx = x + CASE_SIZE*j + CASE_BORDER*(j+1)
                    posy = y + CASE_SIZE*i + CASE_BORDER*(i+1)
                    pg.draw.rect(self.win, (255, 245, 205), (posx, posy, CASE_SIZE+1, CASE_SIZE+1))

        for i in range(GRID_WIDTH + 1):
            rect = pg.Rect(x+(i*(CASE_SIZE+CASE_BORDER)), y, CASE_BORDER, height)
            pg.draw.rect(self.win, (0, 0, 0), rect)

        for i in range(GRID_HEIGHT+1):
            rect = pg.Rect(x, y+(i*(CASE_SIZE+CASE_BORDER)), width, CASE_BORDER)
            pg.draw.rect(self.win, (0, 0, 0), rect)

        for i in range(GRID_WIDTH):
            for j in range(GRID_HEIGHT):
                posx = x + CASE_SIZE*j + CASE_BORDER*j
                posy = y + CASE_SIZE*i + CASE_BORDER*i
                shift = CASE_SIZE
                if self.game.board_discovered[i][j] == 1:
                    if self.game.board_count[i][j] == -1:
                        self.win.blit(BOMB_IMAGE, (posx,posy))
                    elif self.game.board_count[i][j] > 0:
                        c=str(self.game.board_count[i][j])

                        textsurface = myfont.render(c, True, self.colors[self.game.board_count[i][j]+1])
                        text_rect = textsurface.get_rect(center=(posx+shift/2, posy+shift/2))
                        self.win.blit(textsurface, text_rect)

                elif self.game.board_discovered[i][j] == -1:
                    self.win.blit(FLAG_IMAGE, (posx,posy))
                

        
    def draw_mouse(self):
        width = CASE_SIZE * GRID_WIDTH + CASE_BORDER * (GRID_WIDTH+1)
        height = CASE_SIZE * GRID_HEIGHT + CASE_BORDER * (GRID_HEIGHT+1)

        x = (self.w - width)/2
        y = (self.h - height)/2

        (j,i) = self.get_pointed_case()
        
        if (j,i) != (-1,-1):
            posx = x + CASE_SIZE*j + CASE_BORDER*(j+1)
            posy = y + CASE_SIZE*i + CASE_BORDER*(i+1)
            pg.draw.rect(self.win, (120, 120, 120), (posx, posy, CASE_SIZE, CASE_SIZE), CASE_BORDER)

    def draw(self, mouse=True):
        self.draw_grid()
        self.draw_mouse()
        pg.display.update()

    def click(self, button):
        width = CASE_SIZE * GRID_WIDTH + CASE_BORDER * (GRID_WIDTH+1)
        height = CASE_SIZE * GRID_HEIGHT + CASE_BORDER * (GRID_HEIGHT+1)

        x = (self.w - width)/2
        y = (self.h - height)/2

        (j,i) = self.get_pointed_case()
        
        if (j,i) != (-1,-1):
            if button == 1 and self.game.board_discovered[i][j] == 0:
                self.game.discover_case(i,j)
            elif button == 3:
                self.game.board_discovered[i][j] = -1 if self.game.board_discovered[i][j] == 0 else 0

    def get_pointed_case(self):
        width = CASE_SIZE * GRID_WIDTH + CASE_BORDER * (GRID_WIDTH+1)
        height = CASE_SIZE * GRID_HEIGHT + CASE_BORDER * (GRID_HEIGHT+1)

        x = (self.w - width)/2
        y = (self.h - height)/2

        mx, my = pygame.mouse.get_pos()
        if mx >= x+CASE_BORDER and mx < x+width-CASE_BORDER and my >= y+CASE_BORDER and my < y+width-CASE_BORDER:
            gx = math.trunc((mx-(x+GRID_WIDTH*CASE_BORDER)) / CASE_SIZE)
            gy = math.trunc((my-(y+GRID_HEIGHT*CASE_BORDER)) / CASE_SIZE)
            return (gx,gy)
        return (-1, -1)

class MainWindow:
    def __init__(self, size=None, title="Puissance 4"):
        self.size = (0,0)
        if size != None:
            self.size = size 
        else:
            xs = (GRID_WIDTH * CASE_SIZE) + (GRID_WIDTH+1)*CASE_BORDER + 4*CASE_SIZE
            ys = (GRID_HEIGHT * CASE_SIZE) + (GRID_HEIGHT+1)*CASE_BORDER + 3*CASE_SIZE
            self.size = (xs, ys)

        self.w = self.size[0]
        self.h = self.size[1]

        self.win = pg.display.set_mode((self.w, self.h))
        pg.display.set_caption(title)

        self.frame = MyFrame(self)

        self.run()

    def run(self):

        self.frame.draw()

        clock = pg.time.Clock()
        res = 0
        while res == 0:

            clock.tick(120)

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    exit(0)

                if event.type == pg.MOUSEBUTTONDOWN:
                    self.frame.click(event.button)

            self.frame.draw()

            res = self.frame.game.is_end()
        
        self.frame.draw()
        if res == -1:
            print("PARTIE PERDUE")
        else:
            print("PARTIE GAGNEE",res)
        print()

        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    exit(0)


def main():
    pygame.init()
    pygame.font.init()
    main = MainWindow()

if __name__ == '__main__':
    main()