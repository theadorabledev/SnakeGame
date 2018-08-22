from Tkinter import *
from random import randrange
import json
HEIGHT = 20
WIDTH = 40
FOOD = "()"
SPACE = "  "
SEGMENT = "[]"
class Application(Frame): 
    def getGameData(self):
        """ Gets the saved game data at the beggining of the game. """
        try:
            dataJSON = open("snakeGameData.json","r")
            self.dataJSON = json.loads(dataJSON.read())      
        except IOError:
            gameData = {"highScore":0, "width":0, "height":0}
            dataJSON = open('snakeGameData.json', 'w')
            json.dump(gameData,dataJSON)
            self.dataJSON = gameData
           
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
        try:
            if self.snakeHeadPosition[0] < 0 or self.snakeHeadPosition[1] < 0:
                raise IndexError
            if self.grid[self.snakeHeadPosition[1] - self.snakeDirection[1]][self.snakeHeadPosition[0] + self.snakeDirection[0]] == SEGMENT:
                raise IndexError  
            

            self.grid = [[SPACE] * WIDTH for i in  range(HEIGHT)]
            self.grid[self.foodPosition[1]][self.foodPosition[0]] = FOOD
            self.snakeHeadPosition[0] += self.snakeDirection[0] 
            self.snakeHeadPosition[1] -= self.snakeDirection[1] 
            self.snakeMoves.insert(0, self.snakeHeadPosition[:])
            self.snakeMoves = self.snakeMoves[0:self.snakeLength]
            for i in range(self.snakeLength-1, 0, -1):
                self.grid[self.snakeMoves[i][1]][self.snakeMoves[i][0]] = SEGMENT
            if self.grid[self.snakeHeadPosition[1]][self.snakeHeadPosition[0]] == FOOD:
                self.snakeLength += 1
                self.foodEaten = True   
                self.addFood()
            
            self.grid[self.snakeHeadPosition[1]][self.snakeHeadPosition[0]] = SEGMENT
            self.updateWidgets()
            if not self.paused:
                self.master.after(1000/self.speed, self.moveSnake)

        except IndexError:
            self.playerAlive = False
            self.game["text"] = "GAME OVER!"
            self.game["bg"] = "red"  
            gameData = {"highScore":0, "width":WIDTH, "height":HEIGHT}
            if self.dataJSON["highScore"] < self.snakeLength:
                gameData["highScore"] = self.snakeLength
            dataJSON = open('snakeGameData.json', 'w')
            json.dump(gameData,dataJSON)

    def changeSnakeDirection(self, event):
        """ Changes the direction the snake is moving. """
        move = {"Left":[-1, 0], "Right":[1, 0], "Up":[0, 1], "Down":[0, -1]}[event.keysym][:]
        
        if move != self.snakeDirection and [-i for i in move] != self.snakeDirection:
            self.snakeDirection = move[:]
    def updateGridAsText(self):
        """ Turns the grid matrix into a printable string. """
        self.gridAsText = ""
        for row in self.grid:
            self.gridAsText += "".join(row) + "\n"
    def changeSpeed(self, event):
        """ Changes the speed of the snake. """
        self.speed = 2 ** self.scaleSpeed.get()
    def pauseGame(self, event):
        """ Pauses the game. """
        self.paused = not self.paused
        if self.paused == False:
            self.moveSnake()
        else:
            self.playerInfo["text"] = "GAME PAUSED!"
        
        
    def createWidgets(self):        
        """ Creates the widgets. """
        self.updateGridAsText()
        self.game = Label(self, text=self.gridAsText, font='TkFixedFont', borderwidth=4, relief="groove")
        self.game.grid(row=1, column=1)
        self.playerInfo = Label(self, text="PRESS ANY KEY TO BEGIN!", font='TkFixedFont', borderwidth=4, relief="groove")
        self.playerInfo.grid(row=2, column=1)
        self.speedScale = Scale(self, from_=1, to=5, orient=HORIZONTAL, label="SPEED: ", variable = self.scaleSpeed, command=self.changeSpeed)
        self.speedScale.set(3)
        self.speedScale.grid(row=3, column=1)
    def updateWidgets(self):
        """ Updates the widgets. """
        self.updateGridAsText()
        self.playerInfoText = "High Score : " + str(self.dataJSON["highScore"]) + "\nLength : " + str(self.snakeLength)
        self.game["text"] = self.gridAsText
        self.game.grid(row=1, column=1)
        self.playerInfo["text"] = self.playerInfoText  
    def startGame(self, event):
        """ Starts the game after a key has been pressed. """
        self.unbind("<Key>")
        self.bind("<Left>", self.changeSnakeDirection)
        self.bind("<Right>", self.changeSnakeDirection)
        self.bind("<Up>", self.changeSnakeDirection)
        self.bind("<Down>", self.changeSnakeDirection)        
        self.bind("<space>", self.pauseGame)  
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
        self.snakeMoves = [self.snakeHeadPosition, self.snakeSeg1, self.snakeSeg2, self.snakeSeg3, self.snakeSeg4]
        self.playerAlive = True
        self.snakeLength = 5
        self.scaleSpeed = IntVar()
        self.speed = 2
        self.paused = False
        self.playerInfoText = "Length : " + str(self.snakeLength)
        self.getGameData()
        self.createWidgets()

        
        

        
        

def main():
    root = Tk()   
    app = Application(master=root)
    app.mainloop()
    root.destroy()    
if __name__ == "__main__":
    main()
