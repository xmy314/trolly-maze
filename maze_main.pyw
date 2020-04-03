from tkinter import *
from random import random,randint
import keyboard
from time import sleep
# pyinstaller.exe --onefile maze_main.pyw
# four direction N E S W dont want to repeat
dirs=[[0,-1],[1,0],[0,1],[-1,0]]

def is_in_map(pos,dimensions):
    if pos[0]>=0 and pos[1]>=0 and pos[0]<dimensions[0] and pos[1]<dimensions[1]:
        return True
    else:
        return False




class MazeGame(object):
    def __init__(self,w=20,h=20):
        def callback():
            self.root.destroy()
        self.root=Tk()
        self.root.title("Escape Maze")
        self.root.protocol("WM_DELETE_WINDOW", callback)
        self.canvas=Canvas(master=self.root,height=h*20+1,width=w*20+1)
        self.canvas.pack()
        self.w=w
        self.h=h
        self.pos=[0,0]
        self.map=MazeGame.make_maze(self.w,self.h)
        self.drawn_maze=False
        self.message_history=[]
        self.message=0
        self.message_time=False
    
    @staticmethod
    def make_maze(w=20,h=20):
        def find_root(id_lst,n):
            id_lst[n]=id_lst[ id_lst[n] ]
            if id_lst[n]==n:
                return n
            else:
                return find_root(id_lst,id_lst[n])

        def is_connected(pos1,pos2,id_lst):
            if find_root(id_lst , pos1[1]*w+pos1[0])==find_root(id_lst , pos2[1]*w+pos2[0]):
                return True
            else:
                return False
        
        # the list being returned
        maze=[]
        # a number to keep track of to stop breaking walls
        sets_left=w*h
        # a list for union find algorithum
        id_lst=list(range(w*h))
        for y in range(h):
            maze.append([])
            for x in range(w):
                maze[y].append([1,1,1,1])
        while sets_left>1:
            for y in range(h):
                for x in range(w):
                    # check four walls
                    for i in range(4):
                        # try not to break every wall
                        if is_in_map([x+dirs[i][0],y+dirs[i][1]],[w,h]) and (random()<0.1 or sets_left<max(w*h/10,10) ):
                            # avoid index error
                                if not is_connected([x,y],[x+dirs[i][0],y+dirs[i][1]],id_lst):
                                    maze[y][x][i]=0
                                    maze[y+dirs[i][1]][x+dirs[i][0]][(i+2)%4]=0
                                    id_lst[find_root(id_lst,(y+dirs[i][1])*w+x+dirs[i][0])]=find_root(id_lst,y*w+x)
                                    sets_left+=-1
        maze[0][0][3]=0
        maze[-1][-1][1]=0
        return maze
     
    def detection(self):
        temp=-1
        if   keyboard.is_pressed("w"):
            temp=0
        elif keyboard.is_pressed("d"):
            temp=1
        elif keyboard.is_pressed("s"):
            temp=2
        elif keyboard.is_pressed("a"):
            temp=3

        if temp!=-1:
            new_pos=[self.pos[0]+dirs[temp][0],self.pos[1]+dirs[temp][1]]
            if is_in_map(new_pos,[self.w,self.h]) and self.map[self.pos[1]][self.pos[0]][temp]==0:
                self.pos=new_pos
                if self.map[self.pos[1]][self.pos[0]].count(1)==3:
                    self.map=MazeGame.make_maze(self.w,self.h)
                    self.drawn_maze=False
                    if self.message_history.count(4)==0:
                        self.message=4
                    elif self.message_history.count(5)<=5:
                        self.message=5
                    elif self.message_history.count(6)<=5:
                        self.message=6
                    else:
                        self.map[self.pos[1]][self.pos[0]]=[1,1,1,1]
                        self.message=7
            elif self.pos[0]==self.w-1 and self.pos[1]==self.h-1 and temp==1:
                self.message_time=0
                self.message=1
            elif self.pos[0]==0 and self.pos[1]==0 and temp==3:
                self.message_time=0
                if not 1 in self.message_history:
                    self.message=2
                else:
                    self.message=3
            elif self.map[self.pos[1]][self.pos[0]].count(1)==4:
                self.pos=[0,0]
                self.message_history=[]
                self.message_time=0
                self.root.title("Cheating Simulator")

    def update(self):
        self.detection()
        if self.canvas!=None:
            if self.drawn_maze==False:
                self.canvas.delete(ALL)
                for y in range(self.h):
                    for x in range(self.w):
                        for i in range(4):
                            if self.map[y][x][i]==1:
                                if i%2==0:
                                    self.canvas.create_line(2+x*20,
                                                            12+y*20+dirs[i][1]*10,
                                                            22+x*20,
                                                            12+y*20+dirs[i][1]*10, 
                                                            fill="#333333")
                                else:
                                    self.canvas.create_line(12+x*20+dirs[i][0]*10,
                                                            2+y*20,
                                                            12+x*20+dirs[i][0]*10,
                                                            22+y*20, 
                                                            fill="#333333")
                self.drawn_maze=True
            self.player = self.canvas.create_oval(12+self.pos[0]*20-6,
                                    12+self.pos[1]*20-6,
                                    12+self.pos[0]*20+6,
                                    12+self.pos[1]*20+6,
                                    fill="#FF00FF")
            if self.message!=0:
                if hasattr(self, 'shown_text'):
                    self.canvas.delete(self.shown_text)
                self.message_history.append(self.message)
                if self.message==1:
                    self.shown_text=self.canvas.create_text(self.w*10,self.h*10,fill="#c72b50",font="Times 20 italic bold",
                            text="You won!!\n (づ￣3￣)づ╭❤～")
                elif self.message==2:
                    self.shown_text=self.canvas.create_text(self.w*10,self.h*10,fill="#c72b50",font="Times 20 italic bold",
                            text="Finding cheese, smart girl.")
                elif self.message==3:
                    self.shown_text=self.canvas.create_text(self.w*10,self.h*10,fill="#c72b50",font="Times 20 italic bold",
                            text="you won and came back??\nI ❤ U\n❤❤❤❤❤\nThanks for playing")
                elif self.message==4:
                    self.shown_text=self.canvas.create_text(self.w*10,self.h*10,fill="#8a0303",font="devil-breeze 20 italic bold",
                            text="Game starts now\nψ(｀∇´)ψ~hh~")
                elif self.message==5:
                    self.shown_text=self.canvas.create_text(self.w*10,self.h*10,fill="#9400D3",font="devil-breeze 20 italic bold",
                            text="once more.\n(=ↀωↀ=)meow~")
                elif self.message==6:
                    self.shown_text=self.canvas.create_text(self.w*10,self.h*10,fill="#9400D3",font="devil-breeze 20 italic bold",
                            text="stop cheating\n(◣_◢)")
                elif self.message==7:
                    self.shown_text=self.canvas.create_text(self.w*10,self.h*10,fill="#9400D3",font="devil-breeze 20 italic bold",
                            text="this is what you deserve\ntry again?")
                    self.message_time=-1
                self.message=0
                if self.message_time>=0:
                    self.message_time=10
        self.canvas.update()
        self.canvas.delete(self.player)
        if self.message_time>0:
            self.message_time+=-1
        if self.message_time==0 and hasattr(self, 'shown_text'):
            self.canvas.delete(self.shown_text)
        sleep(0.05)
        
if __name__ =="__main__":
    game=MazeGame(20,20)

    while True:
        game.update()
