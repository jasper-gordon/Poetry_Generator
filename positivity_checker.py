"""
Name: Jasper Gordon
Course: CSCI 3725
Assignment: PQ3
Date: 11/8/20
Description: This file holds the Positivity_Score class which deals with rating words and lines based on how positive they are. This positivity
    is calculated with negative numbers meaning a word is relatively negative in its sentiment, and vice versa with posotive. This class uses
    nltk part of speech taging as well as the WordNetLemmatizer to break down words and determine their sentiment scores using SentiWordnet.
    This class can also determine the overall sentiment score of a Poem, defined here as a list of list of strings.
"""
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import sentiwordnet as swn
from nltk.corpus import stopwords 
from nltk.corpus import wordnet as wn
from nltk.tag import pos_tag
from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()


class Positivity_Score:
    
    
    def __init__(self):
        '''
        An initializing method for a Positivity Score object
        '''
        self.score = 0

    def tag_converter(self, tag):
        '''
        Converts the corpus tags to Wordnet tags which are more generalized
            Takes a string tag as an argument. Returns a wordnet tag.
        '''
        if tag.startswith('J'):
            return wn.ADJ
        if tag.startswith('N'):
            return wn.NOUN
        if tag.startswith('R'):
            return wn.ADV
        if tag.startswith('V'):
            return wn.VERB
        return None

    def line_scorer(self, line):
        '''
        Returns the sentiment score of a line. This score is a float value that can be
            postive or negative. These scores reflect the overall sum of the
            sentiments in the given line. The line is a list of strings.
            Returns the float score.
        '''
        sentiment_score = 0.0
        token_counter = 0
        tagged_line = nltk.pos_tag(line)
        #Using SentiWordnet to calculate positivty score of words
        for word, tag in tagged_line:
            #Converting the tags in a given line
            word_tag = self.tag_converter(tag)
            if word_tag not in (wn.NOUN, wn.ADJ, wn.ADV):
                continue
            lemma = lemmatizer.lemmatize(word, pos = word_tag)
            if not lemma:
                continue
            synsets = wn.synsets(lemma, pos = word_tag)
            if not synsets:
                continue
            #Grabs the first word in synsets which is the most commmon one
            synset = synsets[0]
            swn_synset = swn.senti_synset(synset.name())
            #Calculating the overal sentiment score
            sentiment_score += swn_synset.pos_score() - swn_synset.neg_score()
            token_counter += 1
        return sentiment_score

    def poem_scorer(self, poem):
        '''
        Method that given a poem, determines the score of it
            using the sum total of its line scores.
            Takes a poem (list of list of strings) as an argument.
        '''
        local_score = 0.0
        for line in poem:
            local_score += self.line_scorer(line)
        if local_score != 0:
            self.score = local_score / len(poem)

    def positivity_runner(self, poem):
        '''
        Runs the scoring system, taking a poem (list of list of strigns)
            as an argument and returns the overall score of its lines.
        '''
        self.poem_scorer(poem)
        return self.score

