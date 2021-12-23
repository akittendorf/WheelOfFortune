# import modules
import random

# initialize variables
players_started = []

def initialize_game():
    players = []
    for i in range(0, 3):
        d = {}
        d['player'] = i + 1
        d['temp_bank'] = 0
        d['perm_bank'] = 0
        players.append(d)
    return players
        
def get_word(file):
    with open(file) as infile:
        words = infile.read().splitlines()
        return words

def starting_player(lst):
    already_picked = True
    while already_picked == True:
        starter = random.choice(lst)
        if starter in players_started:
            continue
        else: 
            already_picked = False
            players_started.append(starter)
    return starter

def choose_word(words):
    chosen_index = random.randrange(0, len(words)+1)
    chosen_word = words.pop(chosen_index)
    return chosen_word

def hidden_word(correct_guessed, chosen_word):
    hidden_word = [letter if letter in correct_guessed else '-' for letter in chosen_word]