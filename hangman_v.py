import curses

"""
Author: Leah Hackman
Date: April 2, 2014
"""

class Hangman_v:
    
    
    empty_hangman = [" _______ ",
                    "|/     | ",
                    "|        ",
                    "|        ",
                    "|        ",
                    "|        ",
                    "|        ",
                    "---------"]
                    
    man = [[(2,7, "O")],[(3,7, "|"), (4,7, "|")], [(3,6, "\\")], [(3,8, "/")],  [(5,8, "\\")], [(5,6, "/")]]
    full_hangman= [" _______ ",
                    "|/     | ",
                    "|      O ",
                    "|     \|/",
                    "|      | ",
                    "|     / \\",
                    "|        ",
                    "---------"]
                    
    
    def __init__(self, game, term_width, term_height,stdscr): 
        self.game = game
        self.stdscr = stdscr
        
        """
        break up the screen into four panes:
        ----------------
        | a     |b     |
        |       |      |
        |-------|      |
        | c     |      |
        ----------------
        | d            |
        ----------------
        window a is for drawing the hangman
        window b is for recording the guesses
        window c is for showing the word (blanks and correct letters)
        window d is for communicating with the user
        """
        self.a = curses.newwin(int(term_height*4/6), int(term_width/2), 0,0) 
        self.b = curses.newwin(int(term_height*4/6), int(term_width/2), 
                                0, int(term_width/2)) 
        self.c = curses.newwin(int(term_height*1/6), term_width,
                                int(term_height*4/6), 0) 
        self.d = curses.newwin(int(term_height*1/6), term_width,
                                int(term_height*5/6), 0)

        #initialize magenta colour pairing for printing out guessed letters.
        curses.init_pair(1, curses.COLOR_MAGENTA,curses.COLOR_BLACK)


    def draw_hangman(self): 
        window = self.a
        v_offset = 1
        h_offset = 3
        for line in enumerate(Hangman_v.empty_hangman):
            window.addstr(line[0] +v_offset, h_offset, line[1])
        for i in range(min(self.game.num_errors, self.game.max_guesses)):
           for j in Hangman_v.man[i]:
               window.addstr(j[0]+v_offset, j[1]+h_offset, j[2])
        window.noutrefresh()
        
    def draw_wrong_letters(self): 
        """
        Print out the letters they've guessed wrong
        and information about the number of guesses they've made
        """ 
        window = self.b
        window.addstr(0,0, "You've made {} guesses and {} errors so far".format(self.game.num_guesses, self.game.num_errors))
        window.addstr(1,0, "Wrong Letters Guessed: ")
        window.addstr(2, 0,", ".join(self.game.wrong_guesses()))
        
        #need to put the changes up for drawing but do not redraw them yet.
        window.noutrefresh()
        

    def draw_word_field(self): 
        """
        Print out word field. Print ___ for characters we haven't guessed yet.
        Othewise print the character. If the most recent guessed letter was a 
        hit, print it in MAGENTA :O 
        """
        window= self.c 
        for letter in enumerate(self.game.secret_word): 
            if letter[1] in self.game.guesses:
                window.addstr(0, letter[0]*5 + 1," {} ".format(letter[1]), curses.A_UNDERLINE | (curses.color_pair(0) if letter[1] != self.game.most_recent_guess else curses.color_pair(1)) ) 
            else: window.addstr(0,letter[0]*5 + 1, "   ", curses.A_UNDERLINE)

        #need to put the changes up for drawing but do not redraw them yet.
        window.noutrefresh()

    def draw_ui_field(self): 
        """
        Print some text to communicate with the user.
        Either ask for more input OR let them know the game is over.
        """
        window = self.d 
        if self.game.solved():
            window.clear() 
            window.addstr(0,0, "You've won! Congratulations!") 
        elif self.game.game_over(): 
            window.clear() 
            window.addstr(0,0, "It looks as though you've lost. Sorry!") 
        else: 
            if not self.game.most_recent_guess is None:
                window.addstr(0,0, "You guessed the letter {}. There are {} {}'s in the secret word.".format(self.game.most_recent_guess, self.game.num_matches(self.game.most_recent_guess), self.game.most_recent_guess)) 
            window.addstr(1,0, "Please enter a character to guess")
            
        #need to put the changes up for drawing but do not redraw them yet.
        window.noutrefresh()
        
    def draw_screen(self):
        #each draw command updates what should be drawn and then
        #waits to be drawn. The doupdate call draws all the changes
        #at once.
        self.draw_hangman()
        self.draw_wrong_letters()
        self.draw_word_field()
        self.draw_ui_field()
        curses.doupdate()
