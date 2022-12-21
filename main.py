import os
from queue import PriorityQueue
from timeit import default_timer as timer
from node import Node
from configuration import Configuration


def greedySearch(initial, goal, heuristic):
    allConfigurations = list() #vsetky vytvorene konfiguracie
    initState = Configuration(len(initial), len(initial[0]))
    initState.configuration = initial #ak zadava pouzivatel
    initState.findZero() #ak zadava pouzivatel
    currentNode = Node(initState, initState.chooseHeuristic(heuristic, goal)) #korenovy uzol

    generatedNotExpandedNodes = PriorityQueue()
    generatedNotExpandedNodes.put((currentNode.heuristic, currentNode)) #vlozime korenovy uzol do prioritneho radu, kde budu uzly zoradene podla heuristickej hodnoty
    allConfigurations.append(currentNode.state.configuration) #ulozime pociatocnu konfiguraciu
    
    #hlavny cyklus
    while True:
        if generatedNotExpandedNodes.empty(): #uz nie su nerozvite uzly, riesenie neexistuje
            return None
           
        if currentNode.foundGoal(goal): #nasiel sa cielovy stav
            print("vygenerovanych uzlov:")
            print(generatedNotExpandedNodes.qsize())
            return currentNode
        
        children = currentNode.generateChildren(heuristic, goal) #vygeneruje potomkov aktualneho uzla
        children.sort(key=lambda x: x.heuristic) #a usporiada ich vo vzostupnom poradi
    
        onlyNewNodes = [] #sem sa vyfiltruju nove konfiguracie
        for c in range(len(children)):
            if children[c].state.configuration not in allConfigurations: #ak konfiguracia este predtym neexistovala
                onlyNewNodes.append(children[c])

        if len(onlyNewNodes) == 0: #ak nevznikli ziadne nove konfiguracie
            currentNode = generatedNotExpandedNodes.get()[1] #vyberieme prvy uzol z prioritneho radu
        else: #ak vznikla aspon jedna nova konfiguracia
            currentNode = onlyNewNodes[0] #uzol obsahujuci konfiguraciu s najmensou heuristickou hodnotou budeme v nasledujucom cykle rozvijat
            allConfigurations.append(currentNode.state.configuration) #prida aktualnu konfiguraciu do zoznamu vsetkych konfiguracii
            for c in range(1, len(onlyNewNodes)): #ostatne uzly odlozime do prioritneho radu a ulozime ich konfiguracie
                generatedNotExpandedNodes.put((onlyNewNodes[c].heuristic, onlyNewNodes[c]))
                allConfigurations.append(onlyNewNodes[c].state.configuration)


def convertInputIntoArray(str, rows, columns):
    state = []
    for r in range(0,rows):
        state.append([])
        for c in range(0,columns):
            state[r].append(int(str[r*columns+c]))
    return state
        

def main():
    filename = "./tests/3x3.txt"
    name = os.path.basename(filename)
    name = name.split(".", 1)
    name = name[0].split("x")
    rows = int(name[0])
    columns = int(name[1])

    repeats = 0

    with open(filename) as file:
        while(line := file.readline().rstrip()):
            (initial, goal) = line.split("_")
            initialState = convertInputIntoArray(initial, rows, columns)
            goalState = convertInputIntoArray(goal, rows, columns)
            print("INITIAL STATE:")
            for row in range(0, rows): 
                print(*initialState[row])
            print("GOAL STATE:")
            for row in range(0, rows): 
                print(*goalState[row])

            t1 = timer()
            res = greedySearch(initialState, goalState, 2)#2 pre heuristiku_2, 1 je pre heuristiku_1
            t2 = timer()
            print("CAS:")
            print(t2-t1)
            if res is not None:
                repeats += 1
                print("VYSLEDOK:")
                res.state.printConfiguration()
                print("HLBKA RIESENIA")
                print(res.depth)
                path = ""
                while res is not None:
                    path += res.operator
                    res = res.parent
                path = path[::-1]
                print("CESTA:")
                print(path)
            else:
                print("unsolvable")
     
            #print(repeats)
            
main()
    