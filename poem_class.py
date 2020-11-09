'''
Name: Jasper Gordon
Course: CSCI 3725
Assignment: PQ3
Date: 11/8/20
Description: This file handles the processing of NLTK corpora as well as the creation of Poem objects. The corpora 
    are used to create n-gram text generation in the Poem class. The purpose here is to use presidential addresses 
    as the inspiring set of words and phrasing to teach the systme how presidents speak, and then to output the text
    into a more poetic form which includes rhyme. Among a Poem object's inputs is the subject, which is a string
    that dictates the theme of the entire poem. Poem's also have an eternal evaluation system which prioritize
    poems that rhyme while maintaining their structure and clarity. Not all poems will rhyme perfectly.
'''
import nltk
from nltk.corpus import state_union
from nltk.corpus import inaugural
from nltk import ngrams
from collections import Counter, defaultdict
from nltk import bigrams, trigrams
from positivity_checker import Positivity_Score
import random
import string

#Global variable that controls how accurate a rhyme should be
RHYME_LEVEL = 2 
inaugural_words = inaugural.words()
words = [word.lower() for word in state_union.words()] + [word.lower() for word in inaugural_words]
#Removing punctuation
unwanted_characters = [",", ".", ";", ":", "?", "!", '"', "(", ")", "$", "-", "[", "]", "'"]
words = [''.join(c for c in s if c not in unwanted_characters) for s in words]
#Removing spaces
words = [s for s in words if s]
acceptable_letters = ["a", "i", "I"]
words = [s for s in words if len(s) > 1 or s in acceptable_letters]
unique_words = list(set(words))


class Poem:


    def __init__(self, subject, words_per_line, lines):
        '''
        An initializing method that takes a string subject, a int number of words per line of poetry, and an int number of lines
            as arguemnts. This method helps generate a Poem object.
        '''
        self.bi_dict = self.bi_gram()
        self.tri_dict = self.tri_gram()
        self.first_line = True
        self.subject = subject
        self.num_lines = lines
        self.num_words = words_per_line
        #The poem words itself
        self.poem_body = []
        #The positivity score of the poem
        self.posi_score = 0.0
        self.posi_obj = Positivity_Score()
        #Keeps track of how well the poem rhymes
        self.rhyme_score = 0.0
        #Used to determine in a line should rhyme or not
        self.rhyme_bool = False
        self.prev_last_word = ""
        self.poem_score = 0.0

    def __lt__(self, other):
        '''
        A comparison method to the current Poem object to another using their respective scores
        Returns a boolean
        '''
        return self.poem_score < other.poem_score

    def get_poem(self):
        '''
        Getter method to retrieve the lines of the poem itself as a list of lists.
        '''
        return self.poem_body

    def tri_gram(self):
        '''
        Creates/returns a tri-gram dicitonary that takes a pair of words as a key
            and the value are words that have followed that pair in the corpus.
            Repeats are allowed as they simply increase the probability of that 
            value word.
        '''
        probs_dict = {}
        for word, word1, word2 in trigrams(words):
            sequence = (word, word1)
            if sequence not in probs_dict.keys():
                probs_dict[sequence] = []
            probs_dict[sequence].append(word2)
        return probs_dict

    def bi_gram(self):
        '''
        Similar to the tri_gram method, this bi_gram method creates/returns a dictionary
            with a key being a string word, and the value is a list of string words
            that in the corpora have followed that word.
        '''
        probs_dict = {}
        for word, word1 in bigrams(words):
            if word not in probs_dict.keys():
                probs_dict[word] = []
            probs_dict[word].append(word1)
        return probs_dict
        
    def line_generator(self, first_word, word_limit):
        '''
        Method to generate a single line of poetry. It takes as arguments
            a string word to inspire the generation, as well as an int
            limit on the number of words that will be in the line.
            Generates the line using the bi-gram and tri-gram methods
            and ensures that if it's the first line in the poem that the 
            subkect word will be included. Returns the line as a list of strings
        '''
        #List of words that will be outputted
        text = []
        word_count = 0
        if word_limit > 0:
            #Checking to see if this is the first line of the poem
            if self.first_line:
                text.append(first_word)
                word_count += 1
                self.first_line = False
            #Getting one more word using bigram to have two for trigram
            helper_word = random.choice(self.bi_dict[first_word])
            text.append(helper_word)
            text_tuple = (first_word, helper_word)
            word_count += 1
            while word_count < word_limit:
                #Looking to rhyme the last word with the previous line
                if word_count == word_limit - 1:
                    conjunction = True
                    while conjunction:
                        last_word = self.line_rhymer(text_tuple)
                        if self.conjunction_test(last_word) == False:
                            conjunction = False
                    self.prev_last_word = last_word
                    word_count += 1
                    text.append(last_word)
                #If not last word in the line, generate normally
                else:
                    new_word = random.choice(self.tri_dict[text_tuple])
                    text.append(new_word)
                    previous_second_word = text_tuple[1]
                    text_tuple = (previous_second_word, new_word)
                    word_count += 1
        return text

    def line_rhymer(self, text_tuple):
        '''
        Method to determine the last word in a line, with the goal of making it rhyme with
            the previous line if it's the second line in a cuplet. Takes a tuple of string words
            as an arguemnt to generate the last word. Looks for rhymes within tri_grams
            before moving on to any rhymes within the corpora. If no matches found, or if not
            supposed to be a rhyming line, returns a non-rhyming string word.
        '''
        #This covers first line and all non-rhyme reliant lines
        if self.rhyme_bool == False:
            new_word = random.choice(self.tri_dict[text_tuple])
            self.rhyme_bool = True
            return new_word
        self.rhyme_bool = False
        #Check to see if any tri-gram options rhyme
        rhyme_list = self.rhyme(self.prev_last_word, RHYME_LEVEL)
        output = []
        for word in self.tri_dict[text_tuple]:
            #Checks to see if any of the tri_gram words rhyme with the previous line's last word
            if word in rhyme_list:
                output.append(word)
        #If a rhyme is found, add it and add a point to score
        if output:
            new_word = random.choice(output)
            self.rhyme_score += 1
            self.poem_score += 1
            return new_word
        other_rhymes = self.corpus_rhymer(self.prev_last_word)
        #Case of no tri_gram rhymes so instead searchs entire corpus
        if other_rhymes:
            new_word = random.choice(other_rhymes)
            self.rhyme_score += .5
            self.poem_score += .5
            return new_word
        #Case where the system doesn't know any rhymes with the previous word, just generate a word
        else:
            new_word = random.choice(self.tri_dict[text_tuple])
            return new_word

    def corpus_rhymer(self, word):
        '''
        Method to search for any rhymes in the total corpus given a base word.
            Returns a list of all the rhyme strings found
        '''
        rhyme_list = self.rhyme(self.prev_last_word, RHYME_LEVEL)
        output = []
        for word in unique_words:
            if word in rhyme_list:
                output.append(word)
        return output      
    
    def poem_generator(self):
        '''
        Method to generate an entire poem. Returns the poem as a list of lists of strings
            that are constructed using the line_generator method above.
        '''
        line_counter = 0
        output = []
        starting_word = self.subject
        while line_counter < self.num_lines:
            output.append(self.line_generator(starting_word, self.num_words))
            line_counter += 1
        #Resetting first line variable
        self.first_line = True
        self.poem_body = output
    
    def line_to_string(self, line):
        '''
        Joins a list of strings into one single list and returns the string.
            Takes a list of strings as an argument. 
        '''
        str_line = " ".join(line)
        return str_line

    def rhyme(self, base_word, level):
        '''
        Methodd that searches for words that rhyme with a given base inspiring word.
            Takes the string word and an int level that controls the strictness of
            what is defined as a "rhyme".  Larger numbers = more strict.
            Returns a set of the rhyming words.
        '''
        entries = nltk.corpus.cmudict.entries()
        syllables = [(word, syl) for word, syl in entries if word == base_word]
        rhymes = []
        for (word, syllable) in syllables:
            #Uses the level to match final syllables. The higher the level, the more syllables need to match
            rhymes += [word for word, pron in entries if pron[-level:] == syllable[-level:]]
        return set(rhymes)

    def set_positivity(self):
        '''
        Method to set the positivity score of the poem
        '''
        self.poem_score += self.posi_obj.positivity_runner(self.poem_body)

    def get_score(self):
        '''
        Method to get the poem score of the poem. Returns score.
        '''
        return self.poem_score

    def conjunction_test(self, word):
        '''
        Method that checks if a given word is a conjunction.
            Returns boolean, takes a string word as arguemnt.
        '''
        word_list = [word]
        word_tag = nltk.pos_tag(word_list, tagset='universal')
        bad_tags = ['CONJ']
        if word_tag[0][1] in bad_tags:
            return True
        return False

    def in_corpus(self, word):
        '''
        Method to see if a given word is in the corpus.
            Takes a string as an argument, returns boolean
        '''
        if word in unique_words:
            return True
        return False