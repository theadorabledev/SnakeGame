from Tkinter import *
from random import randrange
HEIGHT = 40
WIDTH = 40
SPEED = 8
FOOD = "()"
SPACE = "  "
SEGMENT = "[]"
class Application(Frame): 
    def addFood(self):
        """ Adds the food in a random location. """
        if self.foodEaten:
            while True:
                randHeight = randrange(5, HEIGHT - 5)
                randWidth = randrange(5, WIDTH - 5)
                if self.grid[randHeight][randWidth] == SPACE:
                    self.foodPosition = [randWidth, randHeight]
                    self.foodEaten = False
                    break
    def moveSnake(self):
        """ Updates the snakes positions on the screen every specified time interval. """
        if self.snakeHeadPosition[0] >= WIDTH or self.snakeHeadPosition[0] < 0 or self.snakeHeadPosition[1] >= HEIGHT or self.snakeHeadPosition[1] < 0:
            self.playerAlive = False
        if self.grid[self.snakeHeadPosition[1] - self.snakeDirection[1]][self.snakeHeadPosition[0] + self.snakeDirection[0]] == SEGMENT:
            self.playerAlive = False      
        if self.playerAlive:
            self.grid = [[SPACE] * WIDTH for i in  range(HEIGHT)]
            self.grid[self.foodPosition[1]][self.foodPosition[0]] = FOOD
            self.snakeHeadPosition[0] += self.snakeDirection[0] 
            self.snakeHeadPosition[1] -= self.snakeDirection[1] 
            if self.grid[self.snakeHeadPosition[1]][self.snakeHeadPosition[0]] == FOOD:
                self.snakeLength += 1
                self.foodEaten = True
                lastTail = self.snake[-1]
                newPos = [lastTail["position"][0] - lastTail["direction"][0], lastTail["position"][1] + lastTail["direction"][1]]
                self.snake.append({"position":newPos, "direction":lastTail["direction"]})
                
                self.addFood()
            self.grid[self.snakeHeadPosition[1]][self.snakeHeadPosition[0]] = SEGMENT
            
            for snakeSeg in self.snake:
                for pos in self.snakeHeadMoves:
                    
                    if pos["position"] == snakeSeg["position"]:
                        snakeSeg["direction"] = pos["direction"][:]
                        pos["piecesThrough"] += 1
                        break
                    if pos["piecesThrough"] == len(self.snake):

                        self.snakeHeadMoves.remove(pos)
                        
                snakeSeg["position"][0] += snakeSeg["direction"][0] 
                snakeSeg["position"][1] -= snakeSeg["direction"][1]                
                self.grid[snakeSeg["position"][1]][snakeSeg["position"][0]] = SEGMENT
                self.updateWidgets()            
            self.master.after(1000/SPEED, self.moveSnake)
        else:
            self.game["text"] = "GAME OVER!"
            self.game["bg"] = "red"
    def changeSnakeDirection(self, event):
        """ Changes the direction the snake is moving. """
        move = {"Left":[-1, 0], "Right":[1, 0], "Up":[0, 1], "Down":[0, -1]}[event.keysym][:]
        
        if move != self.snakeDirection and [-i for i in move] != self.snakeDirection:
            self.snakeHeadMoves.append({"position":self.snakeHeadPosition[:], "direction":move, "piecesThrough":0, "snakeLen": len(self.snake)})
            self.snakeDirection = move[:]
    def updateGridAsText(self):
        """ Turns the grid matrix into a printable string. """
        self.gridAsText = ""
        for row in self.grid:
            self.gridAsText += "".join(row) + "\n"
    def createWidgets(self):        
        """ Creates the widgets. """
        self.updateGridAsText()
        self.game = Label(self, text=self.gridAsText, font='TkFixedFont', borderwidth=4, relief="groove")
        self.game.grid(row=1, column=1)
        self.playerInfo = Label(self, text="PRESS ANY KEY TO BEGIN!", font='TkFixedFont', borderwidth=4, relief="groove")
        self.playerInfo.grid(row=2, column=1)
    def updateWidgets(self):
        """ Updates the widgets. """
        self.updateGridAsText()
        self.playerInfoText = "Length : " + str(self.snakeLength)
        self.game["text"] = self.gridAsText
        self.game.grid(row=1, column=1)
        self.playerInfo["text"] = self.playerInfoText  
    def startGame(self, event):
        self.bind("<Left>", self.changeSnakeDirection)
        self.bind("<Right>", self.changeSnakeDirection)
        self.bind("<Up>", self.changeSnakeDirection)
        self.bind("<Down>", self.changeSnakeDirection)        
        
        self.focus_set()        
        self.moveSnake()
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
                
        self.grid = [[SPACE] * WIDTH for i in  range(HEIGHT)]
        
        self.bind("<Key>", self.startGame)

        
        self.focus_set()
        self.gridAsText = ""
        

        self.snakeHeadPosition = [WIDTH/2, HEIGHT/2]
        self.snakeSeg1 = [WIDTH/2, HEIGHT/2 + 1]
        self.snakeSeg2 = [WIDTH/2, HEIGHT/2 + 2]
        self.snakeSeg3 = [WIDTH/2, HEIGHT/2 + 3]
        self.snakeSeg4 = [WIDTH/2, HEIGHT/2 + 4]
        self.snakeDirection = [0, 1]
        self.foodEaten = True
        self.foodPosition = []
        self.addFood()
        self.snakeHeadMoves = []
        self.snake = [{"position":self.snakeSeg1, "direction":self.snakeDirection[:]}, {"position":self.snakeSeg2, "direction":self.snakeDirection[:]}, {"position":self.snakeSeg3, "direction":self.snakeDirection[:]}, {"position":self.snakeSeg4, "direction":self.snakeDirection[:]}]        
        self.playerAlive = True
        self.snakeLength = len(self.snake) + 1
        self.playerInfoText = "Length : " + str(self.snakeLength)
        self.createWidgets()

        
        

        
        


if __name__ == "__main__":
    root = Tk()   
    root.geometry = "2000x1500"
    app = Application(master=root)
    app.mainloop()
    root.destroy()
