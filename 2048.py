from tkinter import *
from tkinter import messagebox
import random

class Board:
    bg_color = {
        '2' : '#eee4da',
        '4' : '#ede0c8',
        '8' : '#edc850',
        '16' : '#edc53f',
        '32' : '#f67c5f',
        '64' : '#f65e3b',
        '128' : '#edcf72',
        '256' : '#edcc61',
        '512' : '#f2b179',
        '1024' : '#f59563',
        '2048' : '#edc22e',
        '4096' : '#bef00a',
        '8192' : '#07e83f',
        '16384' : '#04b831',
        '32768' : '#000000',
        '65536' : '#000000',
        '131072' : '#000000',
        '262144' : '#000000',
        '524288' : '#000000',
        '1048576' : '#000000',
        '2097152' : '#000000',
        '4194304' : '#000000'
    }
    color = {
        '2' : '#776e65',
        '4' : '#f9f6f2',
        '8' : '#f9f6f2',
        '16' : '#f9f6f2',
        '32' : '#f9f6f2',
        '64' : '#f9f6f2',
        '128' : '#f9f6f2',
        '256' : '#f9f6f2',
        '512' : '#776e65',
        '1024' : '#f9f6f2',
        '2048' : '#f9f6f2',
        '4096' : '#776e65',
        '8192' : '#776e65',
        '16384' : '#776e65',
        '32768' : '#f9f6f2',
        '65536' : '#f9f6f2',
        '131072' : '#f9f6f2',
        '262144' : '#f9f6f2',
        '524288' : '#f9f6f2',
        '1048576' : '#f9f6f2',
        '2097152' : '#f9f6f2',
        '4194304' : '#f9f6f2'
    }

    def __init__(self):
        self.n=8
        self.window=Tk()
        self.window.title("William's 8192")
        self.scoreFrame = Frame(self.window,bg = "azure3")
        self.scoreFrame.grid(row=0,column=0,columnspan=self.n,pady=(10,20))
        self.scoreLabel = Label(self.scoreFrame,text="Score:0",
                                font=('arial',18,'bold'),bg='azure3')
        self.scoreLabel.pack()
        self.gameArea=Frame(self.window,bg= 'azure3')
        self.board=[]
        self.gridCell=[[0]*self.n for i in range(self.n)]
        self.compress=False
        self.merge=False
        self.moved=False
        self.score=0
        for i in range(self.n):
            rows=[]
            for j in range(self.n):
                l=Label(self.gameArea,text='',bg='azure4',
                font=('arial',22,'bold'),width=4,height=2)
                l.grid(row=i,column=j,padx=7,pady=7)
                rows.append(l);
            self.board.append(rows)
        self.gameArea.grid()
    def reverse(self):
        for ind in range(self.n):
            i=0
            j=self.n-1
            while(i<j):
                self.gridCell[ind][i],self.gridCell[ind][j]=self.gridCell[ind][j],self.gridCell[ind][i]
                i+=1
                j-=1
    def transpose(self):
        self.gridCell=[list(t)for t in zip(*self.gridCell)]
    def compressGrid(self):
        self.compress=False
        temp=[[0] *self.n for i in range(self.n)]
        for i in range(self.n):
            cnt=0
            for j in range(self.n):
                if self.gridCell[i][j]!=0:
                    temp[i][cnt]=self.gridCell[i][j]
                    if cnt!=j:
                        self.compress=True
                    cnt+=1
        self.gridCell=temp
    def mergeGrid(self):
        self.merge=False
        for i in range(self.n):
            for j in range(self.n - 1):
                if self.gridCell[i][j] == self.gridCell[i][j + 1] and self.gridCell[i][j] != 0:
                    self.gridCell[i][j] *= 2
                    self.gridCell[i][j + 1] = 0
                    self.score += self.gridCell[i][j]
                    self.merge = True
    def random_cell(self):
        cells=[]
        for i in range(self.n):
            for j in range(self.n):
                if self.gridCell[i][j] == 0:
                    cells.append((i, j))
        curr=random.choice(cells)
        i=curr[0]
        j=curr[1]
        self.gridCell[i][j]=2
    
    def can_merge(self):
        for i in range(self.n):
            for j in range(self.n-1):
                if self.gridCell[i][j] == self.gridCell[i][j+1]:
                    return True
        
        for i in range(self.n-1):
            for j in range(self.n):
                if self.gridCell[i+1][j] == self.gridCell[i][j]:
                    return True
        return False
    def paintGrid(self):
        for i in range(self.n):
            for j in range(self.n):
                if self.gridCell[i][j] == 0:
                    self.board[i][j].config(text='',bg='azure4')
                else:
                    self.board[i][j].config(text=str(self.gridCell[i][j]),
                        bg = self.bg_color.get(str(self.gridCell[i][j])),
                        fg = self.color.get(str(self.gridCell[i][j])))
        self.updateScore()

    def restart_game(self):
        self.gridCell = [[0] * self.n for _ in range(self.n)]
        self.score = 0
        self.compress = False
        self.merge = False
        self.moved = False
        self.random_cell()
        self.random_cell()
        self.paintGrid()
        self.updateScore()
    
    def updateScore(self):
        self.scoreLabel.config(text=f"Score: {self.score}")
            

class Game:
    def __init__(self,gamepanel):
        self.gamepanel=gamepanel
        self.end=False
        self.won=False
    def start(self):
        self.gamepanel.random_cell()
        self.gamepanel.random_cell()
        self.gamepanel.paintGrid()
        self.gamepanel.window.bind('<Key>', self.link_keys)
        self.gamepanel.window.mainloop()
    
    

    def link_keys(self,event):
        if self.end or self.won:
            return
        self.gamepanel.compress = False
        self.gamepanel.merge = False
        self.gamepanel.moved = False
        pressed_key=event.keysym
        if pressed_key=='Up':
            self.gamepanel.transpose()
            self.gamepanel.compressGrid()
            self.gamepanel.mergeGrid()
            self.gamepanel.moved = self.gamepanel.compress or self.gamepanel.merge
            self.gamepanel.compressGrid()
            self.gamepanel.transpose()
        elif pressed_key=='Down':
            self.gamepanel.transpose()
            self.gamepanel.reverse()
            self.gamepanel.compressGrid()
            self.gamepanel.mergeGrid()
            self.gamepanel.moved = self.gamepanel.compress or self.gamepanel.merge
            self.gamepanel.compressGrid()
            self.gamepanel.reverse()
            self.gamepanel.transpose()
        elif pressed_key=='Left':
            self.gamepanel.compressGrid()
            self.gamepanel.mergeGrid()
            self.gamepanel.moved = self.gamepanel.compress or self.gamepanel.merge
            self.gamepanel.compressGrid()
        elif pressed_key=='Right':
            self.gamepanel.reverse()
            self.gamepanel.compressGrid()
            self.gamepanel.mergeGrid()
            self.gamepanel.moved = self.gamepanel.compress or self.gamepanel.merge
            self.gamepanel.compressGrid()
            self.gamepanel.reverse()
        elif pressed_key == 'r':
            self.gamepanel.restart_game()
            self.end = False
            self.won = False
            return
        else:
            pass

        self.gamepanel.paintGrid()

        

        if self.gamepanel.moved:
            self.gamepanel.random_cell()
        
        self.gamepanel.paintGrid()
    
gamepanel =Board()
game2048 = Game( gamepanel)
game2048.start()