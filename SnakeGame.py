from Tkinter import *
import time
HEIGHT = 40
WIDTH = 40
SPEED = 4

class Application(Frame): 
         
    def moveSnake(self):
        
        if self.snakeHeadPosition[0] >= WIDTH or self.snakeHeadPosition[0] < 0 or self.snakeHeadPosition[1] >= HEIGHT or self.snakeHeadPosition[1] < 0:
            self.playerAlive = False
        if self.playerAlive:
            self.grid = [["  "] * WIDTH for i in  range(HEIGHT)]
            
            self.snakeHeadPosition[0] += self.snakeDirection[0] 
            self.snakeHeadPosition[1] -= self.snakeDirection[1] 
            self.grid[self.snakeHeadPosition[1]][self.snakeHeadPosition[0]] = "[]"
            
            for snakeSeg in self.snake:
                for pos in self.snakeHeadMoves:
                    
                    if pos["position"] == snakeSeg["position"]:
                        snakeSeg["direction"] = pos["direction"][:]
                        pos["piecesThrough"] += 1
                        break
                    if pos["piecesThrough"] == pos["snakeLen"]:
                        self.snakeHeadMoves.remove(pos)
                snakeSeg["position"][0] += snakeSeg["direction"][0] 
                snakeSeg["position"][1] -= snakeSeg["direction"][1]                
                self.grid[snakeSeg["position"][1]][snakeSeg["position"][0]] = "[]"
              #  print snakeSeg["position"]
                self.createWidgets()            
            self.master.after(1000/SPEED, self.moveSnake)
        else:
            self.game["text"] = "GAME OVER!"
            self.game["bg"] = "red"
    def changeBallDirection(self):
        pass
    def changeSnakeDirection(self,event):
        move = {"Left":[-1, 0],"Right":[1, 0],"Up":[0, 1],"Down":[0, -1]}[event.keysym][:]
        print self.snakeHeadPosition
        print self.snakeDirection
        print move
        
        if move != self.snakeDirection:
            self.snakeHeadMoves.append({"position":self.snakeHeadPosition[:],"direction":move, "piecesThrough":0, "snakeLen": len(self.snake)})
            self.snakeDirection = move[:]
        print self.snakeHeadMoves   
    def updateGridAsText(self):
        self.gridAsText=""
        for row in self.grid:
            self.gridAsText += "".join(row) + "\n"
    def createWidgets(self):        
        self.updateGridAsText()
        self.playerInfo = "Lives : " + str(self.playerAlive) + "\n Points : " + str(self.playerPoints)
        self.game = Label(self, text=self.gridAsText, font='TkFixedFont', borderwidth=4, relief="groove")
        self.game.grid(row=1, column=1)
        self.playerInfo = Label(self, text=self.playerInfo, font='TkFixedFont', borderwidth=4, relief="groove")
        self.playerInfo.grid(row=2, column=1)

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
                
        self.grid = [["  "] * WIDTH for i in  range(HEIGHT)]
        
        
        self.bind("<Left>", self.changeSnakeDirection)
        self.bind("<Right>", self.changeSnakeDirection)
        self.bind("<Up>", self.changeSnakeDirection)
        self.bind("<Down>", self.changeSnakeDirection)        
        
        self.focus_set()
        self.gridAsText=""
        

        self.snakeHeadPosition = [WIDTH/2, HEIGHT/2]
        self.snakeSeg1 = [WIDTH/2, HEIGHT/2 + 1]
        self.snakeSeg2 = [WIDTH/2, HEIGHT/2 + 2]
        self.snakeSeg3 = [WIDTH/2, HEIGHT/2 + 3]
        self.snakeSeg4 = [WIDTH/2, HEIGHT/2 + 4]
        self.snakeDirection = [0, 1]
        self.snakeHeadMoves = []
        self.snake = [{"position":self.snakeSeg1, "direction":self.snakeDirection[:]}, {"position":self.snakeSeg2, "direction":self.snakeDirection[:]}, {"position":self.snakeSeg3, "direction":self.snakeDirection[:]}, {"position":self.snakeSeg4, "direction":self.snakeDirection[:]}]        
        self.playerAlive = True
        self.playerPoints = 0
        
        self.createWidgets()

        self.moveSnake()
        

        
        


if __name__ == "__main__":
    root = Tk()   
    root.geometry="2000x1500"
    app = Application(master=root)
    app.mainloop()
    root.destroy()
