from Tkinter import *
from random import randrange
import json
FOOD = "()"
SPACE = "  "
SEGMENT = "[]"

#Reset: \u001b[0m
class Application(Frame): 
    def getGameData(self):
        """ Gets the saved game data at the beggining of the game. """
        try:
            dataJSON = open("snakeGameData.json","r")
            self.dataJSON = json.loads(dataJSON.read())      
        except IOError:
            gameData = {"highScore":0, "width":40, "height":20, "speed":3}
            dataJSON = open('snakeGameData.json', 'w')
            json.dump(gameData,dataJSON)
            self.dataJSON = gameData
           
    def addFood(self):
        """ Adds the food in a random location. """
        if self.foodEaten:
            while True:
                randHeight = randrange(5, self.height - 5)
                randWidth = randrange(5, self.width - 5)
                if self.grid[randHeight][randWidth] == SPACE:
                    self.foodPosition = [randWidth, randHeight]
                    self.foodEaten = False
                    break
    def moveSnake(self):
        """ Updates the snakes positions on the screen every specified time interval. """
        try:
            print self.snakeHeadPosition
            print self.snakeDirection
            if self.snakeHeadPosition[0] < 0 or self.snakeHeadPosition[1] < 0:
                raise IndexError
            if self.grid[self.snakeHeadPosition[1] - self.snakeDirection[1]][self.snakeHeadPosition[0] + self.snakeDirection[0]] == SEGMENT:
                raise IndexError  
            

            self.grid = [[SPACE] * self.width for i in  range(self.height)]
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
            #self.game.delete("1.0", END)
            #self.game.insert("1.0", "GAME OVER!")
            self.playerInfoText += "\nGAME OVER!"
            self.playerInfo["text"] = self.playerInfoText
            self.game["bg"] = "red"  
            
            
            if self.dataJSON["highScore"] < self.snakeLength:
                self.dataJSON["highScore"] = self.snakeLength
            self.dataJSON["speed"] = self.scaleSpeed.get()
            self.dataJSON["width"] = self.width
            self.dataJSON["height"] = self.height
            dataJSON = open('snakeGameData.json', 'w')
            json.dump(self.dataJSON,dataJSON)

    def changeSnakeDirection(self, event):
        """ Changes the direction the snake is moving. """
        move = {"Left":[-1, 0], "Right":[1, 0], "Up":[0, 1], "Down":[0, -1]}[event.keysym][:]
        
        if move != self.snakeDirection and [-i for i in move] != self.snakeDirection:
            self.snakeDirection = move[:]
    def updateGridAsText(self):
        """ Turns the grid matrix into a printable string. """
        self.gridAsText = u""
        for row in self.grid:
            self.gridAsText += u"".join(row) + "\n"
    def changeSpeed(self, event):
        """ Changes the speed of the snake. """
        self.speed = 2 ** self.scaleSpeed.get()
    def changeDimension(self, event):
        self.game.width = (self.scaleWidth.get()/2)*2*len(SPACE)
        self.game.height = (self.scaleHeight.get()/2)*2
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
        self.game = Text(self, font='TkFixedFont', borderwidth=4, relief="groove", height=self.dataJSON["height"], width=(self.dataJSON["width"]*len(SPACE)))
        self.game.insert(END, self.gridAsText)
        self.game.grid(row=1, column=1, columnspan=3)
        self.playerInfo = Label(self, text="PRESS ANY KEY TO BEGIN!", font='TkFixedFont', borderwidth=4, relief="groove")
        self.playerInfo.grid(row=2, column=2)
        
        
        self.heightScale = Scale(self, from_=20, to=40, orient=HORIZONTAL, resolution=5, label="HEIGHT: ", variable = self.scaleHeight,  command=self.changeDimension)
        self.heightScale.set(self.dataJSON["height"])
        self.heightScale.grid(row=3, column=1)
        
        self.widthScale = Scale(self, from_=20, to=80, orient=HORIZONTAL, resolution=10, label="WIDTH: ", variable = self.scaleWidth, command=self.changeDimension)
        self.widthScale.set(self.dataJSON["width"])
        self.widthScale.grid(row=3, column=2) 
        
        self.speedScale = Scale(self, from_=1, to=5, orient=HORIZONTAL, label="SPEED: ", variable = self.scaleSpeed, command=self.changeSpeed)
        self.speedScale.set(self.dataJSON["speed"])
        self.speedScale.grid(row=3, column=3)
        self.game.tag_config("foodTag", foreground="red")
        self.game.tag_config("snakeTag", background="forest green")   
        self.game.tag_config("snakeHeadTag", background="green")          
    def updateWidgets(self):
        """ Updates the widgets. """
        self.updateGridAsText()

        self.playerInfoText = "High Score : " + str(self.dataJSON["highScore"]) + "\nLength : " + str(self.snakeLength)
        self.game.delete("1.1",END)
        self.game.insert("1.0", self.gridAsText)
        
        
        
        start = 1.0
        while 1:
            pos = self.game.search("[]", start, stopindex=END)
            if not pos:
                break
            
            self.game.tag_add("snakeTag", pos, pos + "+"+str(len(SPACE))+"c")

            start = pos + "+1c"        
        
        headPos = str(self.snakeHeadPosition[1]+1) + "." + str(self.snakeHeadPosition[0]*2)
        self.game.tag_add("snakeHeadTag", headPos, headPos + "+"+str(len(SPACE))+"c")
        
        foodPos = str(self.foodPosition[1]+1) + "." + str(self.foodPosition[0]*2)
        self.game.tag_add("foodTag", foodPos, foodPos + "+"+str(len(SPACE))+"c")
 
        
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
        self.width = 40
        self.height = 20
        self.grid = [[SPACE] * self.width for i in  range(self.height)]
        self.bind("<Key>", self.startGame)
        self.focus_set()
        self.gridAsText = ""
        self.snakeHeadPosition = [self.width/2, self.height/2]
        self.snakeSeg1 = [self.width/2, self.height/2 + 1]
        self.snakeSeg2 = [self.width/2, self.height/2 + 2]
        self.snakeSeg3 = [self.width/2, self.height/2 + 3]
        self.snakeSeg4 = [self.width/2, self.height/2 + 4]
        self.snakeDirection = [0, 1]
        self.foodEaten = True
        self.foodPosition = []
        self.addFood()
        self.snakeMoves = [self.snakeHeadPosition, self.snakeSeg1, self.snakeSeg2, self.snakeSeg3, self.snakeSeg4]
        self.playerAlive = True
        self.snakeLength = 5
        self.scaleSpeed = IntVar()
        self.scaleHeight = IntVar()
        self.scaleWidth = IntVar()
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
