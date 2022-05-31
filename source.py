from copy import deepcopy

#Calculates if the Starting State can reach the Goal State 
# by using parity + row with the blank tile (from the bottom)  
def check_parity(st, en):
    st_par = 0
    en_par = 0
    for num in st:
        if num != 0:
            for x in range(len(st) - st.index(num ) - 1):
                if(st[st.index(num) + x + 1] < num and st[st.index(num) + x + 1] != 0):
                    st_par += 1

    for num in en:
        if num != 0:
            for x in range(len(en) - en.index(num ) - 1):
                if(en[en.index(num) + x + 1] < num and en[en.index(num) + x + 1] != 0):
                    en_par += 1

    st_par = st_par % 2
    st_blankspace = (3 - int(st.index(0) / 4)) % 2 
    
    if(st_par == st_blankspace):
        st_bool = True
    else:
        st_bool = False

    en_par = en_par % 2
    en_blankspace = (3 - int(en.index(0) / 4)) % 2 
    
    if(en_par == en_blankspace):
        en_bool = True
    else:
        en_bool = False

    if(st_bool == en_bool):
        return True
    else: 
        return False    

#Given a queue with Node type objects, the function prints the lists in the node object in the form of a grid
def print_queue(prio_q):
    print("[")
    for item in prio_q:
        print(item, end = ",\n")

    print("\n]")
    
#Returns a list with the elements on the specified positions swapped
def swapPositions(board, pos1, pos2):
        temp = deepcopy(board)
        temp[pos1], temp[pos2] = temp[pos2], temp[pos1]
        return temp

#All four functions below calculate what element to swap with based on the direction of movement
#Returns Node Type Objects
#Returns a None Node if the movement is blocked (for eg cant go down if on the bottom row)
def move_left(board):
    index_from = board.data.index(0)
    if (index_from % 4 == 0):
        return Node(None)
    else:
        return Node(swapPositions(board.data, index_from, index_from-1), parent = board)

def move_right(board):
    index_from = board.data.index(0)
    if ((index_from+1) % 4 == 0):
        return Node(None)
    else:
        return Node(swapPositions(board.data, index_from, index_from+1), parent = board)

def move_down(board):
    index_from = board.data.index(0)
    if (index_from / 4 >= 2):
        return Node(None)
    else:
        return Node(swapPositions(board.data, index_from, index_from+4), parent = board)

def move_up(board):
    index_from = board.data.index(0)
    if (index_from / 4 < 1):
        return Node(None)
    else:
        return Node(swapPositions(board.data, index_from, index_from-4), parent = board)

#Given a node, this functions generates child nodes and assigns them to the node's pointers
def generate_children(node):
    node.down = move_down(node)
    node.up = move_up(node)
    node.left = move_left(node)
    node.right = move_right(node)


class Node:

    def __init__(self, data, parent = None):
        self.left = None
        self.right = None
        self.down = None
        self.up = None
        self.data = data
        self.parent = parent
    
    def __str__(self):
        ret_str = " __ __ __ __\n|"
        if self.data is None:
            ret_str += "  |  |  |  |\n|"*2
            ret_str += "  |  |  |  |\n"

        else:    
            for i in range(3):
                for j in range(4):
                    if(self.data[(4*i)+j] == 0):
                        ret_str += " " + ' |'
                    elif (self.data[(4*i)+j] != 10 and self.data[(4*i)+j] != 11): 
                        ret_str += str(self.data[(4*i)+j]) + ' |'
                    else: 
                        ret_str += str(self.data[(4*i)+j]) + '|'

                if(i != 2):
                    ret_str += "\n|"
        
        return ret_str

class Tree:
    def __init__(self, data):
        self.state = Node(data)


class IDDFS:
    def __init__(self, st, en):
        self.start = Tree(st)
        self.goal = Node(en)
        self.goal_found = False
        self.q = []
        self.final = None
        self.visited = []
        self.path_cost = 0

    #Given a node, this function pushes all its child nodes into the class's shared queue 
    def add_children_to_queue(self,node):
        if(node.up.data is not None and node.up.data not in self.visited):
            self.q.append(node.up)
            self.visited.append(node.up)
        if(node.down.data is not None and node.down.data not in self.visited):
            self.q.append(node.down)
            self.visited.append(node.down)
        if(node.left.data is not None and node.left.data not in self.visited):
            self.q.append(node.left)
            self.visited.append(node.left)
        if(node.right.data is not None and node.right.data not in self.visited):
            self.q.append(node.right)
            self.visited.append(node.right)

    #Start of the Iterative Deepening Algorithm
    def execute(self):
        if(check_parity(self.start.state.data, self.goal.data)):
            depth = 0

            while(not self.goal_found):
                print("Depth =", depth)
                self.q = []
                self.q.append(self.start.state)
                self.search(depth)
                if(not self.goal_found):
                    print("--------------------------------------------------Increasing Depth--------------------------------------------------")
                depth+=1
            
        else:
            print("The goal is unreachable.")

    #Depth First Search
    def search(self, depth, curr_depth = 0):
        if(self.goal_found):
            return

        curr = self.q[-1]
        print("Current Node = ")
        print(curr, end = "\n\n")

        #Goal Test
        if(curr.data == self.goal.data):
            self.goal_found = True
            self.final = curr
            self.path_cost = curr_depth
        else:
            print("Current Queue = ")
            print_queue(self.q)
            if(depth == curr_depth):
                return

            generate_children(curr)
            self.add_children_to_queue(curr)
        
            curr_depth += 1
            while(self.q[-1] != curr):
                self.search(depth, curr_depth)
                if(self.goal_found):
                    return
                self.q.remove(self.q[-1])
                
            curr_depth -= 1

            
# start = [0,9,8,1,4,5,6,7,2,3,10,11]
goal = [0,1,2,3,4,5,6,7,8,9,10,11]
start = [1,5,2,3,4,6,10,7,8,9,0,11]

puzzle = IDDFS(start,goal)
puzzle.execute()

#Finds the path from goal node to start node using parent pointers
if(puzzle.goal_found):
    x = puzzle.final
    path_list = []
    while(x is not None):
        path_list.insert(0,x)
        x = x.parent
    
    print("Final Path  = ")
    print_queue(path_list)
    print("Total Path Cost =", puzzle.path_cost)


