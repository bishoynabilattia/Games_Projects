from tkinter import *
import random 
import string
import time
import heapq
window=Tk() # instantiate an instance of a window
window.geometry("1920x1080") # set the size
window.title("WordQuest AI")
# icon=PhotoImage(file="A:\downloads\Gemini_Generated_Image_pmv7hkpmv7hkpmv7.png")
# window.iconphoto(True,icon)

window.config(background="#232424",)

# potoim=PhotoImage(file="A:\downloads\gjh.png")
# photolabel=Label(window,im=potoim)
# photolabel.place(x=0,y=0)

labtitl=Label(window,text="WordQuest AI",
              background="#084a52",
                font=('Ink Free',15,'bold'),
                fg="#85F8F8",
                relief=RAISED,
                bd=20,
                padx=11
                )
labtitl.place(x=9,y=10)
# %%%%%%%%%%%%%%%%%%%Words%%%%%%%%%%%%%%%%%%%%
lab=Label(window,text="Mansoura, Bishoy, Emad, Cat, Car \n \n Abdelrhman, Fifia, Man, Wordquest, AI "
          ,fg="#99f0ea", bg="#084a52",font=('Arial',12,'bold'),
          )
lab.place(x=950,y=200)


#label copy right
labelprogrmers=Label(window,text='By:Bishoy Nabil & Emad Shokry ',
                 relief=RIDGE,bd=13,background="#063F3A",
                 fg="#99f0ea",
                 font=('Arial',12,'bold'))
labelprogrmers.place(x=950,y=590)
#==================================
#label1
expl=Label(window,text='Enter the word',font=('Ink Free',12,'bold'),
           fg="#8df2f2",background="#08495d",
           relief=RAISED,bd=10)
expl.place(x=20,y=140)
#-------------------------
# click button
# def clic():
#     print('test')
#     expl.config(bg="#10365D")
#     expl.config(fg="#6eddf1")
#     find.config(state=DISABLED)#to disable the button 
#-----------------------------------

#-----------------------------------------
#entery widget


entword=Entry()
entword.config(font=('Ink free',14,'bold'))
entword.config(width=14)
entword.place(x=40,y=190)

# labels of letters
left_frame=Frame(window,bg="#105A62",width="600",height="600",
                        bd="2",relief=RIDGE)
left_frame.place(x=350,y=50)
# left_frame.pack_propagate(False)
def on_click(event):
    event.widget.config(fg="Green",bg="Orange")
def reset(event):
    event.widget.config(fg="#E9F1F2",bg="#040D0E")


def random_maze(maze):

    let_lab = [[0 for _ in range(10)] for _ in range(10)]


    for i in range(10):
        for n in range(10):
            # letter=random.choice(string.ascii_uppercase)
            letter=maze[i][n]
            lab_grid=Label(left_frame,bd=3,bg="#040D0E",fg="#E9F1F2",
                      text=letter.upper(),width=4,height=2,relief=RIDGE,  font=("bold", 15))
            let_lab[i][n]=lab_grid
            lab_grid.bind("<Button-1>",on_click)
            lab_grid.bind("<Button-3>",reset)# تغير اللون عند النقر 
            lab_grid.grid(row=i,column=n)
    return let_lab
           

maze = [
     ["c", "a", "t","b","o","b", "f", "k","s","b"],
     ["w", "o", "r","d","q","u","e","s","t","y"],
     ["a", "u", "b","m","a","d", "a", "f","t","e"],
     ["a", "i", "o","i","u","o", "v", "s","i","b"], 
     ["s", "w", "t","a","s","g", "k", "y","o","h"],
     ["a", "l", "d","e","l","h", "h", "m","a","n" ],
     ["a", "b", "f","i","f","d","o","s","h","u" ],
     ["o", "n", "r","o","c","z", "y", "s","h","e"],
     ["o", "h", "w","z","a","p", "h", "e","r","a"], 
     ["m", "a", "n","s","o","u" ,"r", "a","c","s"]
     
     ]
            
m=random_maze(maze)


class Node():
    def __init__(self, state, word, parent, action,explored):
        self.state = state      # (row, col)
        self.word = word        # "c", "ca", "cat", etc.
        self.parent = parent
        self.action = action
        self.explored=list(explored)

class Stack:
    def __init__(self):
      self.forinter=[]

    def add(self,node):
       self.forinter.append(node)

    def remove(self):
       if self.empty():
          return print("is empty") 
       else:
        current =self.forinter.pop()
       return current
    
    def empty(self):
       return len(self.forinter)==0


class Queue:
    def __init__(self):
      self.forinter=[]

    def add(self,node):
       self.forinter.append(node)

    def remove(self):
       if self.empty():
          return print("is empty") 
       else:
        current =self.forinter.pop(0)
       return current
    
    def empty(self):
       return len(self.forinter)==0

class prioQueue:
    def __init__(self):
        self.frontier=[]
        self.count=0

    def add(self, node,prio):
        heapq.heappush(self.frontier, (prio,self.count,node))
        self.count+=1
    def remove(self):
        if self.empty():
            return None
        return heapq.heappop(self.frontier)[2]
    def empty(self):
        return len(self.frontier)==0
    

class Wordgame():
    def __init__(self, maze):
        self.maze = maze
        self.height =len(maze[0])
        self.width = len(maze)

    def neighbors(self, state):
        row, col = state
        directions = [
            ("up", (row - 1, col)),
            ("down", (row + 1, col)),
            ("left", (row, col - 1)),
            ("right", (row, col + 1)),
            ("r_up", (row - 1, col + 1)),
            ("r_down", (row + 1, col + 1)),
            ("l_up", (row - 1, col - 1)),
            ("l_down", (row + 1, col - 1))
        ]

        result = []
        for action, (r, c) in directions:
            if 0 <= r < self.height and 0 <= c < self.width:
                result.append((action, (r, c)))

        return result


class wordsolver():

    def __init__(self,m,type):
        
        self.maze =m
        self.game = Wordgame(self.maze)
        self.goal=""
        self.type=type
        
    def heuristic(self, current_state, next_char):
        r_c, c_c = current_state
        min_dist = 100
        
        for r in range(10):
            for c in range(10):
                if self.maze[r][c].cget("text") == next_char:
                    dist = abs(r - r_c) + abs(c - c_c)
                    if dist < min_dist:
                        min_dist = dist
        return min_dist if min_dist !=100 else 0

    def solve(self):
        

        Q_step=[]
        if self.type=="DFS":
            frontier = Stack()
        elif self.type=="BFS":
            frontier=Queue()
        else:#ِِA*
            frontier=prioQueue()
            
        for i in range(len(self.maze[0])):
            for j in range(len(self.maze)):
                if self.maze[i][j].cget("text") == self.goal[0]:
                    # self.maze[i][j].config(fg="Green",bg="Orange")

                    
                    start_node = Node(
                    state=(i, j),
                    word=self.maze[i][j].cget("text"),
                    parent=None,
                    action=None,
                    explored=[(i,j)]
                    )

                    if self.type == "A*":
                        h = self.heuristic((i, j), self.goal[1] if len(self.goal)>1 else self.goal[0])
                        frontier.add(start_node, h)
                    else:
                        frontier.add(start_node)
                    Q_step.append(start_node)
                    print((i, j))


        for i in range(len(Q_step)):
            if self.type == "DFS":
                v=Q_step.pop()
                frontier.add(v)
            elif self.type=="BFS":
                v=Q_step.pop(0)
                frontier.add(v)

            else:
                v=Q_step.pop(0)
                frontier.add(v,h)


        # explored = set()
        solutions=[]

        while True:
           

            if frontier.empty():
                # print("No solution")
                return None

            node = frontier.remove()
            print("Current:", node.word, node.state)
            r,c=node.state
            if self.type=="DFS":
                self.maze[r][c].config(fg="Green",bg="Orange")
            elif self.type=="BFS":
                self.maze[r][c].config(fg="Red",bg="White")
            else:#A*
                self.maze[r][c].config(fg="Cyan",bg="Green")

            window.update()
            time.sleep(0.3)
            if node.word == self.goal:
                # print("Found:", node.word)
                # self.maze[r][c].config(fg="Red",bg="Orange")
                solutions.append(node)
                curr = node
                while curr is not None:
                    curr_r, curr_c = curr.state
                    self.maze[curr_r][curr_c].config(bg="#FFD700", fg="black") 
                    curr = curr.parent
                
                window.update()
                break 
            

            # node.explored.add(node.state)

            for action, state in self.game.neighbors(node.state):

                if state not in node.explored:
                    new_explored = node.explored.copy()
                    new_explored.append(state)
                    r, c = state
                    new_word = node.word + self.maze[r][c].cget("text")

                    if not self.goal.startswith(new_word):
                        continue

                    child = Node(
                        state=state,
                        word=new_word,
                        parent=node,
                        action=action,
                        explored=new_explored
                    )
                    if self.type == "A*":
                            g = len(new_word)
                            next_char_idx = len(new_word)
                            target_char = self.goal[next_char_idx] if next_char_idx < len(self.goal) else self.goal[-1]
                            h = self.heuristic(state, target_char)
                            frontier.add(child, g + h)
                    else:
                            frontier.add(child)
                
                # self.maze[r][c].config(fg="Cyan",bg="Red")
                    

                
    
def finword(type): # dfs
    search_word=entword.get().upper() #= retrive the text in entword\
    if len(search_word)>0:
        print("*"*20)
        solver = wordsolver(m,type)
        solver.goal=search_word
        solver.solve()


find=Button(window,text='DFS',command=lambda: finword("DFS"),fg="Green")
find.place(x=40,y=240)
find.bind("<Button-3>",reset)
# find.config(command=clic) #to perform a task
find.config(font=('Ink Free',16,'bold'))
find.config(bg="#dbe60e")
find.config(activebackground="#499399")
find.config(activeforeground="#6ce3e1")

bfs= Button(window,text="BFS",command=lambda: finword("BFS"),fg="Red")
bfs.place(x=40,y=300)

bfs.config(bg="#ebf2f4")
bfs.config(font=('Ink Free',16,'bold'))
bfs.config(activebackground="#E4E718")
bfs.config(activeforeground="#6ce3e1")

A_star= Button(window,text="A*",command=lambda: finword("A*"),fg="#06e5e9")
A_star.config(bg="#2b842a")
A_star.config(font=('Ink Free',16,'bold'))
A_star.config(activebackground="#E4E718")
A_star.config(activeforeground="#6ce3e1")

A_star.place(x=40,y=370)


window.mainloop()



# تشغيل

