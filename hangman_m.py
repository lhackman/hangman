class Hangman_m:
    
    """
    Author: Leah Hackman
    Date: April 2, 2014
    """    
    
    max_guesses = 6
    def __init__(self, secret_word):
        self.secret_word = secret_word
        self.secret_word_letters = set(secret_word)
        self.guesses = set()
        self.most_recent_guess = None
        
    @property
    def num_errors(self):
        return len(self.guesses - self.secret_word_letters)
    @property
    def num_guesses(self):
        return len(self.guesses)
        
        		
    def game_over(self):
        """
        Determine if the player has run out of lives, 
        or has solved the secret_word
        """
        return self.num_errors >= Hangman_m.max_guesses or self.solved()
	    
    def solved(self):
        """
        Determine if the player has solved the secret_word
        """
        return self.secret_word_letters <= self.guesses
        
    def wrong_guesses(self):
        return self.guesses - self.secret_word_letters
	    
    def guess_letter(self, guess):
        if not self.game_over():
            #Should handle if they try to guess the same letter twice
            self.most_recent_guess = guess
            self.guesses.add(guess)
        
    def num_matches(self, letter):
        return sum([1 for l in self.secret_word if l == letter])


	    
	
	    
	
		