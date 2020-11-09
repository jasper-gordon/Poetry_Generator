"""
Name: Jasper Gordon
Course: CSCI 3725
Assignment: PQ3
Date: 11/8/20
escription: This file takes in user input to make calls to the Poem class to generate poems. Once generated, this file serves to sort,
    format, and output the poems both on the screen and through audible projection. The purpose of this file is 
    to orgnaize the execution and presnetation tasks involving the Poem and Positivity_Score classes.
"""
from state_of_union_practice import Poem
from positivity_checker import Positivity_Score
import pyttsx3
#Global variables to limit input
WORD_LIMIT = 10
WORD_MINIMUM = 3
LINE_LIMIT = 30
LINE_MINIMUM = 1
SPPECH_SPEED = 150
#How many poems are generated and evaluated to find the best
NUM_GENERATIONS = 4
def test(poem, engine):
    '''
    Method to output and pronounce the given poem arugment with the given engine argument
    '''
    test_poem = poem.get_poem()
    for line in test_poem:
        poem_string = poem.line_to_string(line)
        print(poem_string)
        engine.say(poem_string)
    
def speaker(engine):
    '''
    Method to speak using the given engine argument
    '''
    engine.runAndWait()

def get_words():
    '''
    Prompts user for the int number of words they want per line in a poem. 
        If not given proper input, propmts user again. Returns an int.
    '''
    words = 0
    while True:
        try:
            words = int(input())
            #Ensuring the int is in between the min and max limit.
            if words < WORD_MINIMUM or words > WORD_LIMIT:
                print("Invalid input, please give an int value between 3 and 10.")
                continue
        except ValueError:
            print("Invalid input, please give an int value like '3' or '4'")
            continue
        else:
            break
    return words


def get_lines():
    '''
    Prompts user for the int number of lines in the poem they want. If not given proper input, 
        propmts user again. Returns an int.
    '''
    lines = 0
    while True:
        try:
            lines = int(input())
            #Ensuring the int is between the min and the max limit.
            if lines < LINE_MINIMUM or lines > LINE_LIMIT:
                print("Invalid input, please give an int value between 1 and 50.")
                continue
        except ValueError:
            print("Invalid input, please give an int value like '8' or '4'")
            continue
        else:
            break
    return lines


def generate_poems(num_poems, subject, words_per_line, num_lines):
    '''
    Method to generate a list of Poem objects.
        Takes number of poems (int), subject of poem (str),
        number of words per line (int) and number of lines (int)
        as arguments. Returns a list of Poem objects
    '''
    poem_list = []
    poem_counter = 0
    while poem_counter < num_poems:
        poem = Poem(subject, words_per_line, num_lines)
        poem.poem_generator()
        poem_list.append(poem)
        poem_counter += 1
    return poem_list

def best_poem(poem_list):
    '''
    Method that generates multiple poems and then chooses the best given postive/negative 
        preference input. Takes an int desired number of poems to generate and a boolean
        where True is positive and False is negative as arguments. Sets the poem_body
        of the Poem object to be the "best poem".
    '''
    #Sorting the list by positivity rankings
    poem_list.sort(key = lambda x: x.get_score())
    return poem_list[-1]  

def get_subject():
    '''
    Method to get user input for the inspriing subject word to base the
        poem generation off of. Returns value as a string.
    '''
    subject = ''
    #Random Poem object to access the list of all words in corpora
    random_poem_obj = Poem("nothing", 5, 5)
    while True:
        try:
            subject = str(input()).lower()
            #Has more than one word
            if len(subject.split()) > 1: 
                print("Invalid input. Please give a single word string as an input")
                continue
            #Empty input
            if not subject:
                print("Please input something")
                continue
            #If input is not in the corpora
            if  random_poem_obj.in_corpus(subject) == False:
                print("Unfortunately, according to our records a President has never said that word.")
                print("Please input a different word")
                continue
        except TypeError:
            print("Invalid input. Only letters please")
            continue
        else:
            break
    return subject

def main():
    '''
    Main method that runs our Genetic Algorithm system while prompting and outputting information to the user in the terminal shell.
    '''
    engine = pyttsx3.init()
    engine.setProperty('rate', SPPECH_SPEED)
    print ("Welcome to the Executive Poetry system.")
    print("Please give a single word to inspire the poem, think presidential thoughts")
    subject = get_subject()
    print("Please input your desired number of lines in the poem")
    lines = get_lines()
    print("And now please input how many words should be in each line")
    words = get_words()
    print("Please wait as we generate your poem, it may take a few moments...\n")
    poem_list = generate_poems(NUM_GENERATIONS, subject, words, lines)
    best = best_poem(poem_list)
    test(best, engine)
    positivty_obj = Positivity_Score()
    print ("\nThis is its positivity score:", positivty_obj.positivity_runner(best.get_poem()))
    print ("This is its full score:", best.get_score())
    speaker(engine)

if __name__ == "__main__":
    main()


