import random
from tkinter import *
from tkinter import messagebox
from time import sleep

class Connect4():
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.data = []
        
        for row in range(self.height):
            boardRow = []
            for col in range(self.width):
                boardRow += [' ']
            self.data += [boardRow]
        
    def __repr__(self):
        #PRINT THE DATA
        s = ''   # the string to return
        for row in range( self.height ):
            s += '|'   # add the separator character
            for col in range(self.width):
                s += self.data[row][col] + '|'
            s += '\n'
        #print out the horizontal separator
        s += '--'*self.width + '-\n'
        for col in range(self.width):
            s += ' ' + str(col % 10)  # mod 10 for spacing
        s += '\n'
        
        return s       # return string
    
    def addMove(self, col, ox ):
        # ADD IF EMPTY AND CLOSED MOVE TO THE NEXT NUMBER
        for row in reversed(range(0, self.height)):
            if self.data[row][col] == ' ':
                self.data[row][col] = ox
                return self     
              


    def clear(self):
        # CLEAR IF THE HEIGHT AND WIDTH Combined.
        for row in range(self.height):
            for col in range(self.width):
                self.data[row][col] = ' '
        return self        
    
    def delMove(self, col):
        # DELETE A MOVE WHEN ITS NOT EMPTY WHICH MAKES EMPTY
        for row in range(self.height):
            if self.data[row][col] != ' ':
                self.data[row][col] = ' '
                return self
    
    def allowsMove(self, col):
        # ALLOWING THE MOVE IF LESS THAN 0 ITS FALSE AND TRUE
        # IF THE RANGE IS VALUABLE
        if col < 0:
            return False
        elif col >= self.width:
            return False
        else:
            for i in range(self.height):
                if self.data[i][col] == ' ':
                    return True
                else:
                    return False
    
    def isFull(self):
        # WHEN FULL MOVE ON TOP OR NEXT NUMBER
        for col in range(self.width):
            for row in range(self.height):
                if self.data[row][col] == ' ':
                    return False
        return True

    def winsFor(self,ox):
        # HORIZONTAL WIN
        for row in range(self.height):
            for col in range(self.width - 3):
                if self.data[row][col] == ox and \
                   self.data[row][col+1] == ox and \
                   self.data[row][col+2] == ox and \
                   self.data[row][col+3] == ox:
                    return True

        # VERTICAL WIN            
        for row in range(self.height - 3):
            for col in range(self.width):
                if self.data[row][col] == ox and \
                   self.data[row+1][col] == ox and \
                   self.data[row+2][col] == ox and \
                   self.data[row+3][col] == ox:
                    return True   

#diagonal win from the upper side
        for row in range(3,self.height):
            for col in range(self.width - 3):
                if self.data[row][col] == ox and \
                   self.data[row-1][col+1] == ox and \
                   self.data[row-2][col+2] == ox and \
                   self.data[row-3][col+3] == ox:
                    return True  

#diagonal win from the lower side
        for row in range(self.height - 3):
            for col in range(self.width - 3):
                if self.data[row][col] == ox and \
                   self.data[row+1][col+1] == ox and \
                   self.data[row+2][col+2] == ox and \
                   self.data[row+3][col+3] == ox:
                    return True                      

        
       
        
        return False
    
    def hostGame(self):
        while True:
            print(self.__repr__()) # Hosts the game under Repr
            player1 = int(input('Player 1 put your input \n')) # Player 1 Enter a number from 1-6
            if self.allowsMove(player1):
                self.addMove(player1, 'X')
                print(self.__repr__())
            else:
                player1 = int(input('Invalid, try again \n')) # If 7+ then its invalid
            if self.isFull() == True:
                print(self.__repr__())
                print('Draw, the game is over') # When board is full its a draw.
                break
            if self.winsFor('X') == True:
                print(self.__repr__())
                print('player 1 won the game') #Player 1 wins under X 
                break 
            player2 = int(input('Player 2 put your input \n')) # Player 2 put a number 1-6
            if self.allowsMove(player2):
                self.addMove(player2, 'O') # Player 2 is O
                print(self.__repr__())
            else:
                player2 = int(input('Invalid, try again \n')) #If 7+ its invalid
            if self.isFull() == True:
                print(self.__repr__())
                print('Draw, the game is over') # If board is full its a draw.
                break

            if self.winsFor('O') == True:
                print(self.__repr__())
                print('Player 2 won') # Player 2 won under O.
                break

    def playgamewith(self,aiPlayer):
        while True:
            print(self.__repr__())
            player1 = int(input('Player 1 put your input \n')) # Player 1 enter a number.
            if self.allowsMove(player1):
                self.addMove(player1,'X')
                print(self.__repr__())
            else:
                player1 = int(input('Invalid, try again \n')) # If 7+ its invalid
            if self.isFull() == True:
                print(self.__repr__())
                print('Draw, the game is over') #  If draw game is over.
                break 
            if self.winsFor('X') == True:
                print(self.__repr__())
                print('player 1 won the game') # Player 1 won the game
                break

            computer = aiPlayer.nextMove(self)
            if self.allowsMove(computer):
                self.addMove(computer, 'O') # The computer is O
                print(self.__repr__())
            if self.isFull() == True:
                print(self.__repr__())
                print('Draw, the game is over') # If full the game is a draw.
                break
            if self.winsFor('O') == True:
                print(self.__repr__())
                print('Player 2 won') # Player 2 won as O
                break 
class Player:
    def __init__(self,ox,tbt,ply):
        self.checker = ox
        self.tieBreakerType = tbt
        self.ply = ply

    def scoreFor(self,b,ox,ply): #Score Method for everyone (determine the best way to win) 
        score = []
        #list for scores for player ox
        for col in range(b.width): # each column of board
            if b.allowsMove(col):
                b.addMove(col, ox)
                if b.winsFor(ox) == True:
                    score.append(100) # if 100 one player wins
                else:
                    if ply > 1:
                        if ox == 'X':
                            opponentscore = self.scoreFor(b, 'O',ply-1)
                        else:
                            opponentscore = self.scoreFor(b, 'X', ply-1)
                        score.append(100-max(opponentscore)) # if 100 one player wins
                    else:
                        score.append(50) # If 50 its a tie
                b.delMove(col)
            else:
                score.append(-1) # Invalid Input
        return score

    def nextMove(self, board):
        score = self.scoreFor(board, self.checker, self.ply) # Player selects the next move.
        bestscore = max(score)
        newlist = []
        for i in range(len(score)):
            if score[i] == bestscore:
                newlist.append(i)
        if self.tieBreakerType == 'Left': # Tie breaker on left is sudden death
            return newlist[0]
        elif self.tieBreakerType == 'Right': # RIght for Sudden death
            return newlist[-1]
        elif self.tieBreakerType == 'Random':
            return random.choice(newlist) # Randomize in sudden death.

class TkC4:
    def __init__(self, window, board, player):
        self.window = window
        self.board = board
        self.player = player

        self.diameter = 100
        self.height = self.board.height * self.diameter + 50
        self.width = self.board.width * self.diameter

        frame = Frame(window)
        frame.pack()

        quitbutton = Button(frame, text="Quit", command=self.quitGame)
        quitbutton.pack()

        
        self.canvas = Canvas(frame, height=self.height, width=self.width, background='#CCFFFF')
        self.canvas.bind('<Button-1>', self.mouseInput)
        self.canvas.pack()


        self.circles = []
        for row in range(self.board.height):
            circleRow = []
            for col in range(self.board.width):
                x = col * self.diameter
                y = row * self.diameter
                circle = self.canvas.create_oval(x, y, x + self.diameter, y + self.diameter)
                circleRow.append(circle)
            self.circles.append(circleRow)


        self.message = self.canvas.create_text(self.width/2, self.height-25, text="Click in the circle to specify your next move", fill='black')

    def quitGame(self):
        self.window.destroy()

    def mouseInput(self, event):
        col = int(event.x / self.diameter)
        row = int(event.y / self.diameter)
        print(event.x, event.y, row, col)

        if self.board.allowsMove(row) != True:
            return

        self.board.addMove(row,'X')

        self.canvas.itemconfig(self.circles[row][col], fill='red')
        self.canvas.update()

        if self.board.winsFor('X'):
            messagebox.showinfo('Connect 4', 'GAME OVER!, Human Wins!')
            self.quitGame()
            return

        elif self.board.isFull():
            messagebox.showinfo('Connect 4', 'GAME OVER!, ITS A TIE!')
            self.quitGame()
            return

        (col) = self.player.nextMove(self.board)

        self.board.addMove(col,'O')

        for i in range(200, -1, -20):
            color = '#{:02x}{:02x}{:02x}'.format(i,i,i)
            self.canvas.itemconfig(self.circles[row][col], fill=color)
            self.canvas.update()
            sleep(0.05)

        if self.board.winsFor('O'):
            messagebox.showinfo('Connect 4', 'GAME OVER!, AI Wins!')
            self.quitGame()
            return

def main():
    b = Connect4(7,6)
    #b.clear()
    #b.hostGame()
    p = Player('O', 'Random', 2)
    #print(p.scoreFor(b, 'O',2))
    #b.playgamewith(p)
    root = Tk()
    root.title('Connect 4')
    game = TkC4(root, b, p)
    root.mainloop()

if __name__ == '__main__':
    main()
