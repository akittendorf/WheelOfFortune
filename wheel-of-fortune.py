# import modules
import random # to select random items from lists
import time # to enhance user experience
import webbrowser # to link to the game instructions

# initialize variables
players_started = [] # to keep track of who's already started a round

# define functions
def get_players(): # takes no arguments, returns a list of player dictionaries
    players = []
    for i in range(0, 3):
        d = {}
        d['player'] = i + 1
        d['temp_bank'] = 0
        d['perm_bank'] = 0
        players.append(d)
    return players
        
def get_words(file): # takes one file, returns a list of the file contents delimited by newline 
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
    chosen_index = random.randrange(0, len(words))
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

def only_vowels(guessed, chosen_word): # takes list of guessed and chosen_word, returns boolean
    vowels = ['a', 'e', 'i', 'o', 'u']
    remaining = [letter for letter in chosen_word if letter not in guessed]
    all_vowels = True
    for letter in remaining:
        if letter in vowels:
            continue
        else:
            all_vowels = False
            break
    return all_vowels
    

def get__consonant_guess(guessed, player): # takes one list, one player dictionary, returns one char
    consonants = ['b', 'c', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'm', 'n', 'p', 'q', 'r', 's', 't', 'v', 'w', 'x', 'y', 'z']
    invalid_guess = True
    while invalid_guess == True:
                        guess = input('Please guess a consonant: ').lower()
                        if guess.isalpha() != True or guess not in consonants:
                            print('Hmmm. It looks like you entered an invalid guess. Please guess a consonant letter.')
                            time.sleep(2)
                            continue 
                        elif len(guess) > 1:
                            print('Hmmm. You guessed more than 1 letter. Please guess 1 letter.')
                            time.sleep(2)
                            continue
                        elif guess in guessed:
                            print('Hmmm. It looks like this has already been guessed. Try something else.')
                            time.sleep(2)
                            continue
                        else:
                            return guess
                            
def get_vowel_guess(guessed, player, free_vowels): # takes one list, one player dictionary, one boolean, returns one char
    vowels = ['a', 'e', 'i', 'o', 'u']
    invalid_guess = True
    while invalid_guess == True:
        guess = input('Please guess a vowel: ').lower()
        if guess.isalpha() != True:
            print('Hmmm. It looks like you entered an invalid guess. Please guess a letter or the word itself.')
            time.sleep(2)
            continue 
        elif len(guess) > 1:
            print('Hmmm. You guessed more than 1 letter. Please guess 1 letter.')
            time.sleep(2)
            continue                
        elif guess in guessed:
            print('Hmmm. It looks like this has already been guessed. Try something else.')
            time.sleep(2)
            continue      
        elif free_vowels == True:
            return guess 
        else:
            player['temp_bank'] -= 250
            return guess 

def get_word_guess(guessed, chosen_word): # takes one list, one string, returns one string
    invalid_guess = True
    while invalid_guess == True:
        guess = input('Please enter your guess for the word: ').lower()
        if len(guess) != len(chosen_word):
            print('Hmmm. The length of your guess needs to match the length of the word. Try something else.')
            print(len(guess))
            print(guess)
            print(len(chosen_word))
            print(chosen_word)
            time.sleep(2)
            continue
        elif guess in guessed:
            print('Hmmm. That word has already been guessed. Try again.')
            time.sleep(2)
            continue
        else:
            return guess        
                    
def check_guess(guess, chosen_word): # takes two strings/chars, returns one boolean
    if guess in chosen_word:
        return True
    elif guess not in chosen_word:
        return False

def choice(player, free_vowels): # takes player dictionary and returns a char
    print('You get the chance to spin again and guess a consonant, purchase a vowel, or guess the word itself!')
    invalid_choice = True
    while invalid_choice == True:
        choice = input('Enter "s" to spin the wheel, "v" to purchase a vowel, or "w" to guess the word').lower()
        if choice == 's':
            if free_vowels == True:
                print('Hmmm. It looks like there are no more consonants left. You can guess a vowel or the word itself.')
                continue
            else:
                return 's'
        elif choice == 'v':
            if free_vowels == False and player['temp_bank'] < 250:
                print('Hmmm. Unfortunately you cannot afford to purchase any vowels at this time. Pick something else.')
                continue   
            else:
                return 'v'
        elif choice == 'w':
            return 'w'
        else:
            print('Hmmm. That was not a valid entry. Please enter "s", "v", or "w"')
            continue
                                  
def round1or2(chosen_word, starter, players): # takes one word, list of player dictionaries, and starter, returns None, has side effects on players
    wheel = ['bankrupt', 'lose a turn', 100, 150, 200, 250, 300, 350, 400, 450, 500, 550, 
             600, 650, 700, 750, 800, 850, 900, 100, 150, 200, 250, 300]
    correct_guessed = []
    guessed = []
    order(starter, players)
    word_guessed = False
    while word_guessed == False:
        print('The word is {} letter(s) long.'.format(len(chosen_word)))
        time.sleep(2)
        hidden_word(correct_guessed, chosen_word)
        time.sleep(2)
        for player in players:
            i = 0
            turn_ended = False
            path = 's'
            while turn_ended == False:
                print('Player {}, it is your turn.'.format(player['player']))
                time.sleep(2)
                print('You have ${} to use for this round and ${} total.'.format(player['temp_bank'], player['perm_bank']))
                time.sleep(2)
                free_vowels = only_vowels(guessed, chosen_word)
                if free_vowels == True:
                    print('There are only vowels remaining. Vowels are now free and available for anyone to guess.')
                    can_pick_vowels = True
                    i = 1
                else:
                    can_pick_vowels = False
                time.sleep(2)
                if i > 0:
                    path = choice(player, free_vowels)
                if i == 0 or path == 's':
                    print('The wheel is spinning!')
                    time.sleep(1)
                    for j in range (0, 3):
                        print('...')
                        time.sleep(1)
                    wheel_option = random.choice(wheel)
                    if wheel_option == 'bankrupt':
                        print('Oh no! You landed on bankrupt. Lose your turn and your cash for this round :(')
                        time.sleep(2)
                        player['perm_bank'] = 0
                        turn_ended = True
                        continue
                    elif wheel_option == 'lose a turn':
                        print('Oh no! You landed on lose a turn. You lose your turn :(')
                        time.sleep(2)
                        turn_ended = True 
                        continue
                    else:
                        print('You landed on ${}'.format(wheel_option))
                        time.sleep(2)
                        guess = get__consonant_guess(guessed, player)
                        guessed.append(guess)
                        result = check_guess(guess, chosen_word)
                        if result == True:
                            print('Nice job! {} is in the word {} time(s).'.format(guess, chosen_word.count(guess)))
                            time.sleep(2)
                            print('You win ${}!'.format(wheel_option*chosen_word.count(guess)))
                            time.sleep(2)
                            player['temp_bank'] += wheel_option*chosen_word.count(guess)
                            correct_guessed.append(guess)
                            hidden_word(correct_guessed, chosen_word)
                            time.sleep(2)
                            i += 1
                            continue       
                        else:
                            print('Sorry - {} is not in the word.'.format(guess))
                            time.sleep(2)
                            turn_ended = True
                            continue    
                elif path == 'v':
                    can_pick_vowels = True
                    guess = get_vowel_guess(guessed, player, free_vowels)
                    guessed.append(guess)
                    result = check_guess(guess, chosen_word)
                    if result == True:
                        print('Nice job! {} is in the word {} time(s).'.format(guess, chosen_word.count(guess)))
                        time.sleep(2)
                        correct_guessed.append(guess)
                        hidden_word(correct_guessed, chosen_word)
                        time.sleep(2)
                        i += 1
                        continue
                    else:
                        print('Sorry - {} is not in the word.'.format(guess))
                        time.sleep(2)
                        turn_ended = True
                        continue
                else:
                    guess = get_word_guess(guessed, chosen_word)
                    guessed.append(guess)
                    result = check_guess(guess, chosen_word)
                    if result == True:
                        print('Congratulations - {} is the word!'.format(chosen_word))
                        time.sleep(2)
                        player['perm_bank'] = player['temp_bank']
                        word_guessed = True
                        return
                    else:
                        print('Sorry, that is incorrect.')
                        time.sleep(2)
                        turn_ended = True
                        continue
                    
        
def round3(richest, chosen_word): # takes one player and one word, returns None, has side effects on the player
    print('The player with the highest bank is Player {} with ${}.'.format(richest['player'], richest['perm_bank']))
    time.sleep(2)
    print('Player {}, you have the opportunity to win an extra $100,000.'.format(richest['player']))
    time.sleep(2)
    print('Provided are the letters: R-S-T-L-N-E. \nYou may guess 3 more consonants and 1 vowel. \nYou will guess the final word for the chance to win an extra $100,000.')
    time.sleep(2)
    print('Are you ready? Go!')
    time.sleep(2)
    consonants = ['b', 'c', 'd', 'f', 'g', 'h', 'j', 'k', 'm', 'p', 'q', 'v', 'w', 'x', 'y', 'z']
    vowels = ['a', 'i', 'o', 'u']
    provided = ['r', 's', 't', 'l', 'n', 'e']
    hidden_word(provided, chosen_word)
    invalid_guess = True
    while len(provided) < 9:
        guess = input('Please enter a consonant: ').lower()
        if guess not in consonants or guess in provided:
            print('''Hmmm. That's not a consonant or the letter is already provided. Try something else.''')
            time.sleep(2)
            continue 
        else:
            provided.append(guess)
    while len(provided) < 10:
        guess = input('Please enter a vowel: ').lower()
        if guess not in vowels or guess in provided:
            print('''Hmmm. That's not a vowel or the letter is already provided. Try something else.''')
            time.sleep(2)
            continue
        else:
            provided.append(guess)
    hidden_word(provided, chosen_word)
    invalid_word = True
    while invalid_word == True:
        guess = input('Please enter the final word: ').lower()
        if guess.isalpha() != True:
            print('Hmmm. Your entry is invalid. Please enter a valid word')
            time.sleep(2)
        elif guess.isalpha() == True and guess != chosen_word:
            invalid_word = False
            print('Sorry, that is incorrect. No bonus for you :(')
            time.sleep(2)
            continue
        elif guess.isalpha() == True and guess == chosen_word:
            invalid_word = False
            print('Congratulations! You guessed the word correctly and the bonus $100,000 has been added to your bank!')
            time.sleep(2)
            richest['perm_bank'] += 100000
            continue

# execution  
print('Welcome to Wheel of Fortune! Compete against two other players in this word game for the chance to win cash prizes.')
time.sleep(5)
print('The game rules will open in a new window. Please review them prior to starting.')
time.sleep(3)
webbrowser.open("https://github.com/akittendorf/WheelOfFortune/blob/main/README.md")
time.sleep(4)
print('Loading words...')
words = get_words('animals.txt')
time.sleep(4)
print('Finalizing set-up...')
players = get_players()
time.sleep(4)
print('The theme is: Animals')
time.sleep(4)

# rounds 1 and 2
for i in range(0, 2):
    print('Round {}'.format(i+1))
    starter = starting_player(players)
    chosen_word = choose_word(words)
    round1or2(chosen_word, starter, players)
    for player in players:
        player['temp_bank'] = 0

# round 3
richest = richest(players)
chosen_word = choose_word(words)
round3(richest, chosen_word)

# results
print('''Congratulations, Player {}! 
      You won Wheel of Fortune and walked away with ${}!'''.format(richest['player'], richest['perm_bank']))
time.sleep(3)
print('''This game has ended. Goodbye!''')
time.sleep(1)