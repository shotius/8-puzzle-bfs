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

    # დახურული სიმრავლის ინიციალიზაცია
    listClosed  = set()
    # რიგის ინიციალიზაცია
    Queue = deque([PuzzleState(startState, None, None, 0, 0, 0)])

    # სანამ რიგიდან არ გამოვა ყველა მონაცემი
    while Queue:
        # ვიღებთ რიგის პირველ ელემენტს
        node = Queue.popleft()
       
        # Cavagdot es elementi nanaxi wveroebis simravleSi
        # ვინახავთ მას დახურულ სიაში
        listClosed.add(node.map)
       
        # თუ ამოღებული წვეროს მდგომარებოა საბოლოო მდგომარეობა
        # დააბრუნე რიგი და დაამთავრე
        if node.state == GoalState:
            GoalNode = node
            return Queue

        # შესაძლო სვლების დადგენა
        posiblePaths = subNodes(node)
        # გასინჯე ყველა შესაძლო გადასვლაზე მდგომი წვერო
        for path in posiblePaths:
            # თუ წვერო არაა დახურულ სიაში 
            if path.map not in listClosed :
                # ჩაამატე რიგში
                Queue.append(path)
                # da daamate nanax wveroebSi
                listClosed .add(path.map)
                # rodes yvela SesaZlo wvero gamokvleulia `posiblePath`-dan
                # axali shesaZlo wveroebisTvis `depth` izrdeba erTiT
                # da Sesamabisad maqsimarul siRmesad vzrdiT
                if path.depth > MaxSearchDeep:
                    MaxSearchDeep = MaxSearchDeep + 1    

#AST**************************************************************
def ast(startState):
    
    global MaxFrontier, MaxSearchDeep, GoalNode
    
    # გარდავქმნათ საწყისი მდგომარეობა ევრისტყული ფუნქციისთვის
    node1 = ""
    for poss in startState:
        node1 = node1 + str(poss)

    # გამოვთვალოთ ევრისტიკული ფუნქცია და დავნიშნოთ საწყისი წვერო
    key = Heuristic(node1)
    # შეიქნა დახურული სიმრავლე რიგი და რიქში პირველი შედის საწყისი მნიშვნელობა
    listClosed = set()
    Queue = []
    Queue.append(PuzzleState(startState, None, None, 0, 0, key)) 
    # დახურულ სიაში შედის საწყისი წვერო
    listClosed.add(node1)
    
    while Queue:
        # რიგის სორტირება ხდება ევრისტიკური ფუნქციის მნიშვნელობის მიხედვით
        Queue.sort(key=lambda o: o.key) 
        # ვიღებთ წვეროს და ვამოწმებთ არის თუ არა ის საბოლოო მდგომარება
        node = Queue.pop(0)
        if node.state == GoalState:
            GoalNode = node
            return Queue
        # ვარკვევთ ყველა შესაძლო გადაადგილებებს
        posiblePaths = subNodes(node)
        # ვამოწმებთ ყველა შესაძლო გადაადგილებას
        for path in posiblePaths:      
            # გარდავქმნათ შესაბამის მონაცემად string
            thisPath = path.map[:]
            # შევამოწმოთ თუ შეტანილია უკვე დახურულ სიაში 
            if thisPath not in listClosed :
                # გამოვთვალოთ ევრისტიკული გასაღები მისთვის
                key = Heuristic(path.map)
                path.key = key + path.depth
                # შევიტანოთ რიგის ბოლოში
                Queue.append(path)      
                # დახურულ სიში შევიტანოთ         
                listClosed .add(path.map[:])
                # თუ წვეროს მომელსაც ვამოწმებთ უფრო ღრმადაა წინაზე 
                # გავზარდოთ მაქსიმალური სიღრმე 
                if path.depth > MaxSearchDeep:
                    MaxSearchDeep = 1 + MaxSearchDeep
        
        
#Heuristic: distance to root numbers
values_0 = [0,1,2,1,2,3,2,3,4]
values_1 = [1,0,1,2,1,2,3,2,3]
values_2 = [2,1,0,3,2,1,4,3,2]
values_3 = [1,2,3,0,1,2,1,2,3]
values_4 = [2,1,2,1,0,1,2,1,2]
values_5 = [3,2,1,2,1,0,3,2,1]
values_6 = [2,3,4,1,2,3,0,1,2]
values_7 = [3,2,3,2,1,2,1,0,1]
values_8 = [4,3,2,3,2,1,2,1,0]

# A* ის დროს ვიყენებთ მანჰეტენის მანძილს როგორც მიახლოების ფუნქციას მიზნის წვერომდე.
# ყოველი რიცხვისთვის აუროფითი ნიშნის მინიჭებით თუ რამდენი კვადრატი აშორებს მას მიზნამდე 
def Heuristic(node):

    global values_0,values_1,values_2,values_3,values_4,values_5,values_6,values_7,values_8

    v0=values_0[node.index("0")]
    v1=values_1[node.index("1")]
    v2=values_2[node.index("2")]
    v3=values_3[node.index("3")]
    v4=values_4[node.index("4")]
    v5=values_5[node.index("5")]
    v6=values_6[node.index("6")]
    v7=values_7[node.index("7")]
    v8=values_8[node.index("8")]

    valofTotal = v0+v1+v2+v3+v4+v5+v6+v7+v8
    return valofTotal
    
        

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
def move(state, direction):
    #generate a copy
    newState = state[:]
    
    #obtain poss of 0
    index = newState.index(0)

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

    #a = [1,8,2,3,4,5,6,7,0]
    #point=Heuristic(a)
    #print(point)
    #return
    
    #info = "6,1,8,4,0,2,7,3,5" #20
    #info = "8,6,4,2,1,3,5,7,0" #26
    
    #Obtain information from calling parameters
    parser = argparse.ArgumentParser()
    parser.add_argument('method')
    parser.add_argument('initialBoard')
    args = parser.parse_args()
    data = args.initialBoard.split(",")

    #Build initial board state
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

    #Start operation
    start = timeit.default_timer()

    function = args.method
    if(function=="bfs"):
        bfs(InitialState)
    if(function=="ast"):
        ast(InitialState) 

    stop = timeit.default_timer()
    time = stop-start

    if GoalNode:
        #Save total path result
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
        file.write("path_to_goal: " + str(moves) + "\n")
        file.write("cost_of_path: " + str(len(moves)) + "\n")
        file.write("nodes_expanded: " + str(NodesExpanded) + "\n")
        file.write("search_depth: " + str(deep) + "\n")
        file.write("max_search_depth: " + str(MaxSearchDeep) + "\n")
        file.write("running_time: " + format(time, '.8f') + "\n")
        file.close()
        #'''
    else:
        print("note found")


if __name__ == '__main__':
    main()
