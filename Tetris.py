from Figures import Figure

"""
Defines the currrent game and pieces
"""
class Tetris:
    level = 1
    score = 0
    total_placed = 0
    placed = 0
    field = []
    state = 'start'
    height = 0
    width = 0
    x = 100
    y = 60
    zoom = 20
    figure = None
    
    def __init__(self, height, width):
        """ Initalises the play board at input 1 height and input 2 width """
        self.height = height
        self.width = width
        self.field = []
        for i in range(height):
            new_line = []
            for j in range(width):
                new_line.append(0)
            self.field.append(new_line)
    
    
    def new_figure(self):
        """ Randomly selects and sets new block """
        self.figure = Figure(3, 0)
        
    def intersects(self):
        """ Checks if the current block intersects with an already placed block """
        intersection = False
        for i in range(4):
            for j in range(4):
                if i * 4 + j in self.figure.image():
                    if i + self.figure.y > self.height - 1 or \
                       j + self.figure.x > self.width - 1 or \
                       j + self.figure.x < 0 or \
                       self.field[i + self.figure.y][j + self.figure.x] > 0:
                        intersection = True
        return intersection
    
    def freeze(self):
        """ Freezes the current block, checks for full lines,
        gets new block and returns 0 if game is over"""
        for i in range(4):
            for j in range(4):
                if i * 4 + j in self.figure.image():
                    self.field[i + self.figure.y][j + self.figure.x] = self.figure.color
        self.break_lines()
        self.placed += 1
        self.total_placed += 1
        if self.placed > 15:
            self.level += 1
            self.placed = 0
        self.new_figure()
        if self.intersects():
            return 0
        else:
            return 1
    
    def break_lines(self):
        """ Clears full lines and moves other blocks down """
        lines = 0
        for i in range(1, self.height):
            zeros = 0
            for j in range(self.width):
                if self.field[i][j] == 0:
                    zeros += 1
            if zeros == 0:
                lines += 1
                for i1 in range(i, 1, -1):
                    for j in range(self.width):
                        self.field[i1][j] = self.field[i1 - 1][j]
        if lines > 0:
            self.score += (lines + self.level - 1) ** 2
    
    # Movements
    def go_space(self):
        """ Moves block to lowest possible point on y-axis, calls freeze()
        and returns freeze output. """
        while not self.intersects():
            self.figure.y += 1
        self.figure.y -= 1
        x = self.freeze()
        return x
    
    
    def go_down(self):
        """ If possible, moves block down once,
        else calls freeze() and returns output """
        self.figure.y += 1
        if self.intersects():
            self.figure.y -= 1
            x = self.freeze()
            return x
    
    
    def go_side(self, direction):
        """ Moves block in specified direction
        Acceptable inputs: -1, 1 """
        old_x = self.figure.x
        self.figure.x += direction
        if self.intersects():
            self.figure.x = old_x
        
    def rotate(self):
        """ If possible, rotates the current block """
        old_rotation = self.figure.rotation
        self.figure.rotate()
        if self.intersects():
            self.figure.rotation = old_rotation

    def read_scores(self):
        """ Reads past scores (used for initialisation) from scores.txt """
        scores = []
        try:
            f = open("scores.txt", "r")
            for i in range(0, 5):
                scores.append(f.readline().rstrip())
            return(scores)
        except:
            self.write_scores([0,0,0,0,0])
            
    def check_highscore(self):
        """ Checks if a new highscore has been made.
        If so, sets new highscore list """
        scores = self.read_scores()
        for i in range(0, len(scores)):
            if self.score > int(scores[i]):
                cur = self.score
                for j in range(i, len(scores)):
                    nex = scores[j]
                    scores[j] = cur
                    cur = nex
                self.write_scores(scores)
                break

    def write_scores(self, scores):
        """ Writes inputted scores to file """
        f = open("scores.txt", "w")
        for i in scores:
            f.write(str(i) + "\n")