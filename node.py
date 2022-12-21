from copy import deepcopy

class Node:
    def __init__(self, state, heuristic, operator="", parent=None):
        self.state = state #konfiguracia
        self.operator = operator #operacia pouzita na prechod z konfiguracie v rodicovskom uzle do konfiguracie ulozenej v danom uzle
        self.parent = parent
        self.heuristic = heuristic
        if parent is None:
            self.depth = 0
        else:
            self.depth = parent.depth+1


    def foundGoal(self, goal_state):
        current_state = self.state.configuration
        for row in range(len(current_state)):
            for column in range(len(current_state[0])):
                if current_state[row][column] != goal_state[row][column]:
                    return False
        return True


    def generateChildren(self, h, goal):
        avaliableMoves = ["U","D","L","R"]
        if self.parent is not None: #ak nejde o korenovy uzol
            if self.state.zero[0] == 0 and self.parent.operator != "D":
                avaliableMoves.remove("U")
            elif self.state.zero[0] == self.state.rows-1 and self.parent.operator != "U":
                avaliableMoves.remove("D")

            if self.state.zero[1] == 0 and self.parent.operator != "R":
                avaliableMoves.remove("L")
            elif self.state.zero[1] == self.state.columns-1 and self.parent.operator != "L":
                avaliableMoves.remove("R")
        else: #ak rozvijame korenovy uzol
            if self.state.zero[0] == 0:
                avaliableMoves.remove("U")
            elif self.state.zero[0] == self.state.rows-1:
                avaliableMoves.remove("D")

            if self.state.zero[1] == 0:
                avaliableMoves.remove("L")
            elif self.state.zero[1] == self.state.columns-1:
                avaliableMoves.remove("R")

        children = []
        for move in range(0, len(avaliableMoves)):
            newConfiguration = deepcopy(self.state) #prekopiruje aktualnu konfiguraciu
            newConfiguration.makeMove(avaliableMoves[move]) #a posunie medzeru
            children.append(Node(newConfiguration, newConfiguration.chooseHeuristic(h, goal), avaliableMoves[move], self)) #vytvori novy uzol
        return children


    #pre porovnanie uzlov v prioritnom rade
    def __eq__(self, other): 
        return (self.heuristic == other.heuristic)


    def __lt__(self, other):
        return (self.heuristic < other.heuristic)


    def __gt__(self, other):
        return (self.heuristic > other.heuristic) 

       