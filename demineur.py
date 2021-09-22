import random
from consts import *

class Demineur:

    def __init__(self, board=None, width=GRID_WIDTH, height=GRID_HEIGHT, difficulty=None):

        self.width = width
        self.height = height 
        
        self.board = board if board != None else [[0 for i in range(height)] for j in range(width)]
        self.board_count = [[0 for i in range(height)] for j in range(width)]
        self.board_discovered = [[0 for i in range(height)] for j in range(width)]
        self.fill_counted_board()

        self.difficulty = difficulty if difficulty else self.define_difficulty()
        self.bombs_coords = self.get_bombs_coords()

    def __str__(self):
        s = ''
        for i in range(self.width):
            for j in range(self.height):
                if self.board_count[i][j] > 0:
                    s+=str(self.board_count[i][j])
                elif self.board_count[i][j] == 0:
                    s+= " "
                else:
                    s+= "X"
            s+='\n'
        return s[:-1]

    def new_game(self):
        self.bombs_coords = self.fill_bombs_coords()
        self.fill_board()
        self.fill_counted_board()

    def define_difficulty(self):
        if self.board == None:
            return 0

        nb_bombs = self.count_bombs()
        if nb_bombs == -1:
            return 0

        ratio_bombs = nb_bombs*100 / (self.width*self.height)
        if ratio_bombs == 0:
            return 2
        elif ratio_bombs < 0.10:  
            return 1
        elif ratio_bombs < 0.15:
            return 2
        elif ratio_bombs < 0.20:
            return 3
        return 4

    def count_bombs(self):
        if self.board == None:
            return -1

        ct = 0
        for i in range(self.width):
            for j in range(self.height):
                if self.board[i][j] == -1:
                    ct += 1
        return ct

    def get_bombs_coords(self):
        if not self.board:
            return None
        
        coords = set([])
        for i in range(self.width):
            for j in range(self.height):
                if self.board[i][j] == -1:
                    coords.add((i,j))
        return coords

    def fill_bombs_coords(self):
        if not self.board and not self.difficulty > 0:
            return -1
        
        board_size = self.width*self.height
        if self.difficulty == 1:
            ratio = random.randint(5,7)
        elif self.difficulty == 2:
            ratio = random.randint(8,12)
        elif self.difficulty == 3:
            ratio = random.randint(13,18)
        elif self.difficulty == 4:
            ratio = random.randint(19,25)
        else: 
            return -1

        nbombs = board_size*ratio/100
        coords = set([])
        while len(coords) < nbombs: 
            coords.add((random.randint(0,self.width-1),random.randint(0,self.height-1)))
        return coords

    def fill_board(self):
        if self.difficulty == 0:
            print("No difficulty set, can't fill board")
            return
        if len(self.bombs_coords) <= 0:
            print("No bomb found")
            return

        for x,y in self.bombs_coords:
            self.board[x][y] = -1

    def count_bombs_around(self, x, y):
        ct = 0
        for i in range(x-1, x+2):
            for j in range(y-1, y+2):
                if 0 <= i < self.width and 0 <= j < self.height:
                    if self.board[i][j] == -1:
                        ct+=1
        return ct

    def fill_counted_board(self):
        for i in range(self.width):
            for j in range(self.height):
                self.board_count[i][j] = -1 if self.board[i][j] == -1 else self.count_bombs_around(i,j)

    def is_end(self):
        cleared = True
        for i in range(self.width):
            for j in range(self.height):
                if self.board_discovered[i][j] == 1:
                    if self.board[i][j] == -1:
                        return -1
                elif self.board[i][j] != -1:
                    cleared = False
        return 1 if cleared else 0

    def discover_case(self, x, y):
        self.board_discovered[x][y] = 1
        if self.board_count[x][y] == 0:
            for i,j in [(x-1,y+0),(x+1,y+0),(x+0,y-1),(x+0,y+1)]:
                if 0 <= i < GRID_WIDTH and 0 <= j < GRID_HEIGHT:
                    if self.board_discovered[i][j] == 0:
                        self.discover_case(i, j)


if __name__ == '__main__':
    dem = Demineur()
    dem.new_game()
    print(dem)
