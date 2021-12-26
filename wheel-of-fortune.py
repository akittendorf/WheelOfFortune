# import modules
import random # to select random items from lists
import time # to enhance user experience
import webbrowser # to link to the game instructions
# initialize variables
players_started = []

# define functions
def initialize_game(): # takes no arguments, returns a list of player dictionaries
    players = []
    for i in range(0, 3):
        d = {}
        d['player'] = i + 1
        d['temp_bank'] = 0
        d['perm_bank'] = 0
        players.append(d)
    return players
        
def get_word(file): # takes one file, returns a list of the file contents delimited by newline 
    with open(file) as infile:
        words = infile.read().splitlines()
        return words

def starting_player(lst): # takes one list, returns one random item in list
    already_picked = True
    while already_picked == True:
        starter = random.choice(lst)
        if starter in players_started:
            continue
        else: 
            already_picked = False
            players_started.append(starter)
    return starter

def choose_word(words): # takes one list, returns random element from list
    chosen_index = random.randrange(0, len(words)+1)
    chosen_word = words.pop(chosen_index)
    return chosen_word

def hidden_word(correct_guessed, chosen_word): # takes one list and one word, returns one string
    hidden_word = [letter if letter in correct_guessed else '-' for letter in chosen_word]
    print(*hidden_word)
    
def order(starter, players): # takes one list and one element from the list, returns ordered list based on the element
    temp = [0, 0, 0]
    for player in players:
        if starter == player:
            temp[0] = starter
        elif temp[1] == 0:
            temp[1] = player
        else:
            temp[2] = player
    players[0] = temp[0]
    players[1] = temp[1]
    players[2] = temp[2]
    return players

def richest(players): # takes one list of player dictionaries, returns player dictionary with highest perm_bank
    total = 0
    for player in players:
        if player['perm_bank'] > total:
            total = player['perm_bank']
            richest = player
        else:
            continue
    return richest

def get_guess(guessed, player, can_pick_vowels): # takes one list, one player dictionary, one boolean, returns one string/char
    consonants = ['b', 'c', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'm', 'n', 'p', 'q', 'r', 's', 't', 'v', 'w', 'x', 'y', 'z']
    vowels = ['a', 'e', 'i', 'o', 'u']
    invalid_guess = True
    while invalid_guess == True:
                        guess = input('Please guess a letter or the word itself: ').lower()
                        if guess.isalpha() != True:
                            print('Hmmm. It looks like you entered an invalid guess. Please guess a letter or the word itself.')
                            continue 
                        elif guess in guessed:
                            print('Hmmm. It looks like this has already been guessed. Try something else.')
                            continue
                        elif guess in vowels:
                            if can_pick_vowels == False:
                                print('Hmmm. It looks like you cannot pick a vowel at this time. Guess a consonant or the word itself.')
                                continue
                            elif can_pick_vowels == True and player['temp_bank'] < 250:
                                print('Hmmm. It looks like you cannot afford any vowels at this time. Try guessing a consonant or the word itself.')
                                continue
                            else:
                                player['temp_bank'] -= 250
                                return guess
                        elif guess in consonants:
                            return guess
                        else:
                            return guess
                        
def check_guess(guess, chosen_word): # takes two strings/chars, returns one boolean
    if guess in chosen_word:
        return True
    elif guess not in chosen_word:
        return False
                                
def round1or2(chosen_word, starter, players): # takes one word, list of player dictionaries, and starter, returns None, has side effects on players
    wheel = ['bankrupt', 'lose a turn', 100, 150, 200, 250, 300, 350, 400, 450, 500, 550, 
             600, 650, 700, 750, 800, 850, 900, 100, 150, 200, 250, 300]
    incorrect_guessed = []
    correct_guessed = []
    guessed = incorrect_guessed + correct_guessed
    order(starter, players)
    word_guessed = False
    while word_guessed == False:
        print('These are instructions')
        for player in players:
            turn_ended = False
            can_pick_vowels = False
            while turn_ended == False:
                print('Player {}, it is your turn.'.format(player['player']))
                print('Spin the wheel!')
                wheel_option = random.choice(wheel)
                if wheel_option == 'bankrupt':
                    print('Oh no! You landed on bankrupt. Lose your turn and your cash for this round :(')
                    player['perm_bank'] = 0
                    turn_ended = True
                    continue
                elif wheel_option == 'lose a turn':
                    print('Oh no! You landed on lose a turn. You lose your turn :(')
                    turn_ended = True 
                    continue
                else:
                    print('You landed on ${}'.format(wheel_option))
                    guess = get_guess(guessed, chosen_word, can_pick_vowels)
                    result = check_guess(guess)
                    if result == True:
                       if len(guess) == len(chosen_word):
                           print('Congratulations - {} is the word!'.format(chosen_word))
                           player['perm_bank'] = player['temp_bank']
                           word_guessed = True
                           break
                       else:
                           print('Nice job! {} is in the word {} time(s).'.format(guess, chosen_word.count(guess)))
                           print('You win ${}!'.format(wheel_option*chosen_word.count(guess)))
                           player['temp_bank'] += wheel_option*chosen_word.count(guess)
                           correct_guessed.append(guess)
                           hidden_word(correct_guessed, chosen_word)
                           print('You get the chance to guess another letter or the word itself!')
                           can_pick_vowels = True
                           continue       
                    else:
                           print('Sorry - {} is not in the word.'.format(guess))
                           incorrect_guessed.append(guess)
                           turn_ended = True
                           continue
    for player in players:
        player['temp_bank'] = 0
    
def round3(richest, chosen_word): # takes one player and one word, returns None, has side effects on the player
    print('The player with the highest bank is Player {} with ${}.'.format(richest['player'], richest['perm_bank']))
    print('Player {}, you have the opportunity to win an extra $100,000.')
    print('''Provided are the letters: R-S-T-L-N-E. You may guess 3 more consonants and 1 vowel. 
          You will guess the final word for the chance to win an extra $100,000.''')
    print('Are you ready? Go.')
    consonants = ['b', 'c', 'd', 'f', 'g', 'h', 'j', 'k', 'm', 'p', 'q', 'v', 'w', 'x', 'y', 'z']
    vowels = ['a', 'i', 'o', 'u']
    provided = ['r', 's', 't', 'l', 'n', 'e']
    hidden_word(provided, chosen_word)
    invalid_guess = True
    while len(provided) < 9:
        guess = input('Please enter a consonant: ').lower()
        if guess not in consonants or guess in provided:
            print('''Hmmm. That's not a consonant or the letter is already provided. Try something else.''')
            continue 
        else:
            provided.append(guess)
    while len(provided) < 10:
        guess = input('Please enter a vowel: ').lower()
        if guess not in vowels or guess in provided:
            print('''Hmmm. That's not a vowel or the letter is already provided. Try something else.''')
            continue
        else:
            provided.append(guess)
    hidden_word(provided, chosen_word)
    invalid_word = True
    while invalid_word == True:
        guess = input('Please enter the final word: ').lower()
        if guess.isalpha != True:
            print('Please enter a valid word')
        elif guess.isalpha == True and guess != chosen_word:
            invalid_word = False
            print('Sorry, that is incorrect. No bonus for you :(')
            continue
        elif guess.isalpha == True and guess == chosen_word:
            invalid_word = False
            print('Congratulations! You guessed the word correctly and the bonus $100,000 has been added to your bank!')
            richest['perm_bank'] += 100000
            continue

# The Game # 
print('Welcome to Wheel of Fortune! Compete against two other players in this word game for the chance to win cash prizes.')
print('Review the game rules at {}'.format(webbrowser.open("https://stage3talent.brightspace.com/d2l/le/content/6771/viewContent/9188/View?ou=6771")))
    

    
        
    
    
        
                   
                               
                            
                        
                        
                          
                
        