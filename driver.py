import argparse
import time
import timeit
from collections import deque


#Information *****************************************************
class PuzzleState:
    def __init__(self, state, parent, move, depth, cost, key):
        self.state = state
        self.parent = parent
        self.move = move
        self.depth = depth
        self.cost = cost
        self.key = key
        if self.state:
            self.map = ''.join(str(e) for e in self.state)
    def __eq__(self, other):
        return self.map == other.map
    def __lt__(self, other):
        return self.map < other.map
    def __str__(self):
        return str(self.map)    

#Global variables***********************************************
GoalState = [0, 1, 2, 3, 4, 5, 6, 7, 8]
GoalNode = None # at finding solution
NodesExpanded = 0 #total nodes visited
MaxSearchDeep = 0 #max deep
MaxFrontier = 0 #max frontier


#BFS**************************************************************
def bfs(startState):

    global MaxFrontier, GoalNode, MaxSearchDeep

    # nanaxi simreavellebis ismravle
    boardVisited = set()
    # deki siwyisi mniSvnelobebisTvis
    Queue = deque([PuzzleState(startState, None, None, 0, 0, 0)])

    # sanam dekidan ar amoviRebT yvela wveros
    while Queue:
        # amoviRoT dekis pirveli elementi, mdgomarieba grafis wveroSi
        node = Queue.popleft()
       
        # Cavagdot es elementi nanaxi wveroebis simravleSi
        boardVisited.add(node.map)
       
        # Tu amoRebuli wveros mdgomareoba saboloo mdgomareobaa
        # daabrune deki da daamTavre
        if node.state == GoalState:
            GoalNode = node
            return Queue

        # SesaZlo svlebi
        posiblePaths = subNodes(node)
        for path in posiblePaths:
            # Tu aRmoCenilebSi araa
            if path.map not in boardVisited:
                # Caamate dekSi
                Queue.append(path)
                # da daamate nanax wveroebSi
                boardVisited.add(path.map)
                # rodes yvela SesaZlo wvero gamokvleulia `posiblePath`-dan
                # axali shesaZlo wveroebisTvis `depth` izrdeba erTiT
                # da Sesamabisad maqsimarul siRmesad vzrdiT
                if path.depth > MaxSearchDeep:
                    MaxSearchDeep = MaxSearchDeep + 1
        

    
#Obtain Sub Nodes********************************************************
def subNodes(node):

    global NodesExpanded # gakeTebuli svlebis raodenoba
    NodesExpanded = NodesExpanded+1

    # yvela mimartulebis gadasvlis mcdelobebi
    nextPaths = []
    nextPaths.append(PuzzleState(move(node.state, 1), node, 1, node.depth + 1, node.cost + 1, 0))
    nextPaths.append(PuzzleState(move(node.state, 2), node, 2, node.depth + 1, node.cost + 1, 0))
    nextPaths.append(PuzzleState(move(node.state, 3), node, 3, node.depth + 1, node.cost + 1, 0))
    nextPaths.append(PuzzleState(move(node.state, 4), node, 4, node.depth + 1, node.cost + 1, 0))
    
    # Tu Sesabamisi mimarTulebiT gadasvla SasaZlebelia
    # Caamatos Sesabamisi gadasvliT miRebuli mdomareoba masivSi 
    nodes=[]
    for procPaths in nextPaths:
        if(procPaths.state!=None):
            nodes.append(procPaths)
    return nodes


#Next step**************************************************************
# gansazRvos gadaadgilebebi
def move(state, direction):
    # gaakeTos mdgomareobis kopireba
    newState = state[:]

    # ipovos nulis pozicia
    index = newState.index(0)

    # da  `direction' cvladis Sesabamisad daabrunos mdgomareoba`
    if(index==0):
        if(direction==1):
            return None
        if(direction==2):
            temp=newState[0]
            newState[0]=newState[3]
            newState[3]=temp
        if(direction==3):
            return None
        if(direction==4):
            temp=newState[0]
            newState[0]=newState[1]
            newState[1]=temp
        return newState      
    if(index==1):
        if(direction==1):
            return None
        if(direction==2):
            temp=newState[1]
            newState[1]=newState[4]
            newState[4]=temp
        if(direction==3):
            temp=newState[1]
            newState[1]=newState[0]
            newState[0]=temp
        if(direction==4):
            temp=newState[1]
            newState[1]=newState[2]
            newState[2]=temp
        return newState    
    if(index==2):
        if(direction==1):
            return None
        if(direction==2):
            temp=newState[2]
            newState[2]=newState[5]
            newState[5]=temp
        if(direction==3):
            temp=newState[2]
            newState[2]=newState[1]
            newState[1]=temp
        if(direction==4):
            return None
        return newState
    if(index==3):
        if(direction==1):
            temp=newState[3]
            newState[3]=newState[0]
            newState[0]=temp
        if(direction==2):
            temp=newState[3]
            newState[3]=newState[6]
            newState[6]=temp
        if(direction==3):
            return None
        if(direction==4):
            temp=newState[3]
            newState[3]=newState[4]
            newState[4]=temp
        return newState
    if(index==4):
        if(direction==1):
            temp=newState[4]
            newState[4]=newState[1]
            newState[1]=temp
        if(direction==2):
            temp=newState[4]
            newState[4]=newState[7]
            newState[7]=temp
        if(direction==3):
            temp=newState[4]
            newState[4]=newState[3]
            newState[3]=temp
        if(direction==4):
            temp=newState[4]
            newState[4]=newState[5]
            newState[5]=temp
        return newState
    if(index==5):
        if(direction==1):
            temp=newState[5]
            newState[5]=newState[2]
            newState[2]=temp
        if(direction==2):
            temp=newState[5]
            newState[5]=newState[8]
            newState[8]=temp
        if(direction==3):
            temp=newState[5]
            newState[5]=newState[4]
            newState[4]=temp
        if(direction==4):
            return None
        return newState
    if(index==6):
        if(direction==1):
            temp=newState[6]
            newState[6]=newState[3]
            newState[3]=temp
        if(direction==2):
            return None
        if(direction==3):
            return None
        if(direction==4):
            temp=newState[6]
            newState[6]=newState[7]
            newState[7]=temp
        return newState
    if(index==7):
        if(direction==1):
            temp=newState[7]
            newState[7]=newState[4]
            newState[4]=temp
        if(direction==2):
            return None
        if(direction==3):
            temp=newState[7]
            newState[7]=newState[6]
            newState[6]=temp
        if(direction==4):
            temp=newState[7]
            newState[7]=newState[8]
            newState[8]=temp
        return newState
    if(index==8):
        if(direction==1):
            temp=newState[8]
            newState[8]=newState[5]
            newState[5]=temp
        if(direction==2):
            return None
        if(direction==3):
            temp=newState[8]
            newState[8]=newState[7]
            newState[7]=temp
        if(direction==4):
            return None
        return newState
    
#MAIN**************************************************************
def main():

    global GoalNode

    #  # User input for initial state 
    # InitialState = []
    # print("-Input numbers from 0-8 for initial state ")
    # for i in range(0,9):
    #     print('')
    #     x = int(input("enter vals :"))
    #     InitialState.append(x)

  
    # argumentebis wakiTxva inputidan
    parser = argparse.ArgumentParser()
    parser.add_argument('initialBoard')
    args = parser.parse_args()
    data = args.initialBoard.split(",")

    # initial state - is ageba
    InitialState = []
    InitialState.append(int(data[0]))
    InitialState.append(int(data[1]))
    InitialState.append(int(data[2]))
    InitialState.append(int(data[3]))
    InitialState.append(int(data[4]))
    InitialState.append(int(data[5]))
    InitialState.append(int(data[6]))
    InitialState.append(int(data[7]))
    InitialState.append(int(data[8]))

    # dro operaciis dawyebisas
    start = timeit.default_timer()

    # bfs algoriTmi
    bfs(InitialState)

    # gaCerebis dro
    stop = timeit.default_timer()
    time = stop-start

    # maqsimaluri siRrme
    deep=GoalNode.depth
    moves = []
    while InitialState != GoalNode.state:
        if GoalNode.move == 1:
            path = 'Up'
        if GoalNode.move == 2:
            path = 'Down'
        if GoalNode.move == 3:
            path = 'Left'
        if GoalNode.move == 4:
            path = 'Right'
        moves.insert(0, path)
        # ava mSobel mdgomareobaSi 
        GoalNode = GoalNode.parent

    #'''
    #Print results
    print("path: ",moves)
    print("cost: ",len(moves))
    print("nodes expanded: ",str(NodesExpanded))
    print("search_depth: ",str(deep))
    print("MaxSearchDeep: ",str(MaxSearchDeep))
    print("running_time: ",format(time, '.8f'))
    #'''

    #Generate output document for grade system
    #'''
    file = open('output.txt', 'w')
    file.write("initial_state: " + args.initialBoard + "\n")
    file.write("path_to_goal: " + str(moves) + "\n")
    file.write("cost_of_path: " + str(len(moves)) + "\n")
    file.write("nodes_expanded: " + str(NodesExpanded) + "\n")
    file.write("search_depth: " + str(deep) + "\n")
    file.write("max_search_depth: " + str(MaxSearchDeep) + "\n")
    file.write("running_time: " + format(time, '.8f') + "\n")
    file.close()
    #'''

if __name__ == '__main__':
    main()
