class Configuration:

    def __init__(self, rows, columns, configuration = None):
        self.rows = rows
        self.columns = columns
        self.configuration = configuration
        if not configuration:
            print("in not")
            self.configuration = []
            for r in range(0, rows): #preddefinovana pociatocna konfiguracia, na testovanie
                self.configuration.append([])
                for c in range(0, columns):
                    self.configuration[r].append(r*c+c)
            self.zero = (0,0)
        else:
            print("in else")
            self.findZero()


    def findZero(self): #vyhlada suradnice medzery, ak sa vstup zadaval manualne
        for row in range(0, self.rows): 
            for column in range(0, self.columns):
                if self.configuration[row][column] == 0:
                    self.zero = (row, column)
                    break


    def makeMove(self, move):
        if move == "U":
            self.up()
        if move == "D":
            self.down()
        if move == "L":
            self.left()
        if move == "R":
            self.right()
    

    def up(self):
        row = self.zero[0]
        column = self.zero[1]
        holder = self.configuration[row-1][column]
        self.configuration[row-1][column] = self.configuration[row][column]
        self.configuration[row][column] = holder

        self.zero = (row-1, column)


    def down(self):
        row = self.zero[0]
        column = self.zero[1]
        holder = self.configuration[row+1][column]
        self.configuration[row+1][column] = self.configuration[row][column]
        self.configuration[row][column] = holder

        self.zero = (row+1, column)


    def left(self):
        row = self.zero[0]
        column = self.zero[1]
        holder = self.configuration[row][column-1]
        self.configuration[row][column-1] = self.configuration[row][column]
        self.configuration[row][column] = holder

        self.zero = (row, column-1)
    

    def right(self):
        row = self.zero[0]
        column = self.zero[1]
        holder = self.configuration[row][column+1]
        self.configuration[row][column+1] = self.configuration[row][column]
        self.configuration[row][column] = holder

        self.zero = (row, column+1)


    def printConfiguration(self):
        for row in range(0, self.rows): 
            print(*self.configuration[row])



    def chooseHeuristic(self, h, goal):
        return self.heuristic_1(goal) if h==1 else self.heuristic_2(goal)


    def heuristic_2(self, goal_state): 
        current_state = self.configuration
        sum_of_distances = 0
        #pre kazde policko v aktualnej konfiguracii
        for row in range(len(current_state)):
            for column in range(len(current_state[0])):
                if current_state[row][column] == 0: #igrorujeme posuny medzery
                    continue
                #vyhladame policko s rovnakou hodnotou v cielovej konfiguracii
                for r in range(len(current_state)):
                    for c in range(len(current_state[0])):
                        if current_state[row][column] == goal_state[r][c]:
                            sum_of_distances += abs(row-r) #pocet posunov hore/dole
                            sum_of_distances += abs(column-c) #pocet posunov vlavo/vpravo
        return sum_of_distances


    def heuristic_1(self, goal_state):
        current_state = self.configuration
        num_of_misplaced_elements = 0
        for row in range(len(current_state)):
            for column in range(len(current_state[0])):
                if current_state[row][column] != 0 and current_state[row][column] != goal_state[row][column]:
                    num_of_misplaced_elements += 1 
        return num_of_misplaced_elements
