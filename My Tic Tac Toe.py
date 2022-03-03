# imports
import tkinter as tk
import functools as fs
import random as rm
from tkinter import messagebox as mx
from copy import deepcopy as dc

global board
board = [[" " for x in range(3)] for y in range(3)]


def thank_you(gboard):
    gboard.destroy()
    ty = tk.Tk()
    ty.geometry('380x340')
    ty.title('Thank You')
    ty.resizable(False, False)
    ty.overrideredirect(True)

    background = tk.PhotoImage
    # photo for background
    background = tk.PhotoImage(file='thank-you-6.gif')

    # labels
    label1 = tk.Label(ty, image=background)
    label1.place(x=0, y=10)

    ty.after(5000, lambda: ty.destroy())  # Destroy the widget after 30 seconds

    ty.mainloop()


def replay(gboard, box):
    global board
    if box == 'yes':
        gboard.destroy()
        board = [[" " for x in range(3)] for y in range(3)]
        main()
    else:
        thank_you(gboard)


def winner(gboard, token):
    return ((gboard[0][0] == token and gboard[0][1] == token and gboard[0][2] == token) or
            (gboard[1][0] == token and gboard[1][1] == token and gboard[1][2] == token) or
            (gboard[2][0] == token and gboard[2][1] == token and gboard[2][2] == token) or
            (gboard[0][0] == token and gboard[1][0] == token and gboard[2][0] == token) or
            (gboard[0][1] == token and gboard[1][1] == token and gboard[2][1] == token) or
            (gboard[0][2] == token and gboard[1][2] == token and gboard[2][2] == token) or
            (gboard[0][0] == token and gboard[1][1] == token and gboard[2][2] == token) or
            (gboard[0][2] == token and gboard[1][1] == token and gboard[2][0] == token))


# Check if the player can push the button or not
def isfree(i, j):
    return board[i][j] == " "


def isfull():
    flag = True
    for i in board:
        if i.count(' ') > 0:
            flag = False
    return flag


def pc():
    moves = []
    for x in range(len(board)):
        for y in range(len(board[x])):
            if board[x][y] == ' ':
                moves.append([x, y])
    if moves == []:
        return
    else:
        for letter in ['O', 'X']:
            for i in moves:
                bcopy = dc(board)
                bcopy[i[0]][i[1]] = letter
                if winner(bcopy, letter):
                    return i
        corners = []
        for x in moves:
            if x in [[0, 0], [0, 2], [2, 0], [2, 2]]:
                corners.append(x)
            if len(corners) > 0:
                move = rm.randint(0, len(corners) - 1)
                return corners[move]
        edges = []
        for x in moves:
            if x in [[0, 1], [1, 0], [1, 2], [2, 1]]:
                edges.append(x)
        if len(edges) > 0:
            move = rm.randint(0, len(edges) - 1)
            return edges[move]


def get_text(x, y, gboard, player1, player2, player):
    global sign
    global button
    if player == 'Computer':
        if board[x][y] == ' ':
            if sign % 2 == 0:
                player1.config(state=tk.DISABLED)
                player2.config(state=tk.ACTIVE)
                board[x][y] = 'X'
            else:
                button[x][y].config(state=tk.ACTIVE)
                player1.config(state=tk.ACTIVE)
                player2.config(state=tk.DISABLED)
                board[x][y] = 'O'
            sign += 1
            button[x][y].config(text=board[x][y])
        x = True
        if winner(board, 'X'):
            x = False
            box = mx.askquestion('Play Again', 'Player has won the match! \n Would you like to play again?')
            replay(gboard, box)
        elif winner(board, 'O'):
            x = False
            box = mx.askquestion('Play Again', 'The Computer has won the match! \n Would you like to play again?')
            replay(gboard, box)
        elif isfull():
            x = False
            box = mx.askquestion('Play Again', 'The game is Tied! \n Would you like to play again?')
            replay(gboard, box)
        if x:
            if sign % 2 != 0:
                move = pc()
                button[move[0]][move[1]].config(state=tk.DISABLED)
                get_text(move[0], move[1], gboard, player1, player2, player)
    else:
        if board[x][y] == ' ':
            if sign % 2 == 0:
                player1.config(state=tk.DISABLED)
                player2.config(state=tk.ACTIVE)
                board[x][y] = 'X'
            else:
                player1.config(state=tk.ACTIVE)
                player2.config(state=tk.DISABLED)
                board[x][y] = 'O'
            sign += 1
            button[x][y].config(text=board[x][y])
        if winner(board, 'X'):
            x = False
            box = mx.askquestion('Play Again', 'Player 1 has won the match! \n Would you like to play again?')
            replay(gboard, box)
        elif winner(board, 'O'):
            x = False
            box = mx.askquestion('Play Again', 'The Player 2 has won the match! \n Would you like to play again?')
            replay(gboard, box)
        elif isfull():
            x = False
            box = mx.askquestion('Play Again', 'The game is Tied! \n Would you like to play again?')
            replay(gboard, box)


def game_board(gboard, player1, player2, player):
    global button
    button = []
    for x in range(3):
        m = 2 + x
        button.append(x)
        button[x] = []
        for y in range(3):
            n = y
            button[x].append(y)
            get_t = fs.partial(get_text, x, y, gboard, player1, player2, player)
            button[x][y] = tk.Button(gboard, command=get_t, height=4, width=8)
            button[x][y].grid(row=m, column=n)
    gboard.mainloop()


def play(gboard, player):
    # destroy menu and create new window
    gboard.destroy()
    gboard = tk.Tk()
    gboard.title('Tic Tac Toe')

    # label players
    if player == 'Computer':
        player1 = tk.Label(gboard, text='Player: X', width=10)
        player1.grid(row=1, column=0)

        player2 = tk.Label(gboard, text=player + ': O', width=10, state=tk.DISABLED)
        player2.grid(row=1, column=2)
    else:
        player1 = tk.Label(gboard, text='Player 1: X', width=10)
        player1.grid(row=1, column=0)

        player2 = tk.Label(gboard, text=player + ': O', width=10, state=tk.DISABLED)
        player2.grid(row=1, column=2)

    game_board(gboard, player1, player2, player)


def main():
    # global variables
    global sign
    sign = 0

    # create window
    menu = tk.Tk()
    menu.geometry('220x300')
    menu.title('Tic Tac Toe')
    menu.resizable(False, False)

    # variables calling functions
    pc = fs.partial(play, menu, player='Computer')
    pl = fs.partial(play, menu, player='Player 2')
    stop = fs.partial(thank_you, menu)

    # photo for background
    background = tk.PhotoImage(file='cereal-tic-tac-toe.gif')

    # labels
    label1 = tk.Label(menu, image=background)
    label1.place(x=0, y=10)

    label2 = tk.Label(menu, text='Welcome to Tic Tac Toe', font=('Verdana', 12), width=50)
    label2.pack()

    # buttons
    single = tk.Button(menu, text='Single Player', command=pc, fg='white', bg='green', font=('Verdana', 12), width=50)
    multi = tk.Button(menu, text='Multi-Player', command=pl, fg='white', bg='green', font=('Verdana', 12), width=50)
    gquit = tk.Button(menu, text='Exit Game', command=stop, fg='white', bg='green', font=('Verdana', 12), width=50)

    gquit.pack(side='bottom')
    multi.pack(side='bottom')
    single.pack(side='bottom')

    menu.mainloop()


if __name__ == '__main__':
    main()
