import curses
import sys
import hangman_m
import hangman_v

"""
Author: Leah Hackman
Date: April 2, 2014
"""


def hangman_c(game, stdscr):
    #this is the "contorller" part of our hangman game.
    
    #create our game "view"
    #create view for handling updating the screen
    view = hangman_v.Hangman_v(game,curses.COLS-1, curses.LINES -1, stdscr)
    stdscr.addstr("Press Any Key to Begin")
    stdscr.getkey()
    
    while 1:
        #redraw the screen
        view.draw_screen()
        #Ask user for a guess
        c = stdscr.getkey().lower()
        game.guess_letter(c)

   
#the user can input a secret word as the first arguement into our program. 
#Otherwise use the word giraffe.
secret_word = sys.argv[1].strip().lower() if len(sys.argv) >1 else "giraffe"

#create our game "model"
game = hangman_m.Hangman_m(secret_word)

curses.wrapper(lambda screen: hangman_c(game, screen))