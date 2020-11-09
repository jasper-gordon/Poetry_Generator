# Poetry_Generator

Title: Executive Poetry System
Author: Jasper Gordon
Date: 11/8/2020

Project Description:
    The goal of this project was to create a poetry generator that utilized presidential speeches, in this case
    innaugral addresses and state of the union speeches, as inspriation for an n-gram system of language generation
    in the form of poetry. On the most braod level, the system works by breaking down the speeches using NLTK to
    build n-gram-utuilizng text generation systems. These systems then generate text into a given poetic format
    partially chosen by the user. The user can control (within some limits) the number of wors per line, and
    number of lines per poem. Addiitonally, the user chooses a single word to base the poem on, and that word
    appears at the beggining of the poem. In theory every two lines of the poems should rhyme as cuplets,
    although it is often depednent on the input givne to the system. When run, the system generates numerous
    different poems based on the given subject input, and then returns what it evaluates as the best poem,
    which is defined as the poem that most frequently rhymes while also maintaing the syntatical structure
    provided by the n-gram probabilities.

Challenges:
    I spent a long time during this process reading through various library and module documentations,
    testing out systems, and seeing how things worked. The NLTK platform is quite helpful, but also
    dense and quite confusing to work through. One of the most difficult challenges for me was to
    define what "poetry" is in terms of form, and then try and put my own personal spin on it.
    Rhyming prooved to be the most difficult task, as the many rhyming modules out there are too
    precise in classifying a rhyme, and thus I was often left with poems that read more like
    run-on sentences. There was also a great deal here that I was not able to accomplish. As you'll
    see looking through the positivity_score class, I worked hard to create systems to evaluate how
    positive or negative a line of poetry or an entire poem was. The goal of this was to create a 
    generator called "A Somber President" which would takes these commonly magestic, uplifting
    speeches, and turn them into sorrowful tales, to add an unusual tone to them. My plan was to 
    identify the most positive words in a line, and then swap them out with their antonyms to
    flip the tone. I got everything working exept the antonyms so I decided I would put that on hold
    and finish at a later time if I could. So it is left now as an unfinished, yet achievable final goal.
    This project challenged me to truly work independently, and to think about orginization and plamning.
    I wish, in retrospect, that I had planned the layout of the classes more, as I don't think they are as
    clean as I would like them to be.

Code setup/execution:
    Below please find a list of modules to import through your temrinal shell. For the "import nltk -->" lines
    you must first type "python3" into terminal to enter a python3 shell, type "import nltk," press enter,
    and then add the module (exp: "nltk.download('inaugural')").
    
    To run the program, cd into the project directory and type "python3 file_runner.py" and follow the prompts
    on the screen. Beware it is currently a little slow, so be paitent with it :)


Left To Do
1. Improve output (appearence of poems, pronunciations, syntax of poem)
2. Engage sentiment switching (making happy words sad and vice versa)
3. Reduce runtime
4. Perhaps implement something to limit what type of words can be inputted? (Nouns only?)


Things to install:
pip3 install nltk
import nltk --> nltk.download('inaugural')
import nltk --> nltk.download('state_of_union')
import nltk --> nltk.download('sentiwordnet')
import nltk --> nltk.download('universal_tagset')
pip3 install pyttsx3


Scholarlary Articles:

http://computationalcreativity.net/iccc2018/sites/default/files/papers/ICCC_2018_paper_59.pdf
    This article gave me good ideas on how to tackle the rhyming, as well as the structure of poetry itself. They
    look at breaking down words by pronunciation, using the CMU dict which, while I did not end up using it, got me
    thinking about how I would tackle analyzing words. Additioally, this article gave me the idea to have the number
    of lines and words per line be somewhat fluid, giving the user a little more control.

https://www.aclweb.org/anthology/P17-4008.pdf 
    While deciding on how to generate text, I went back and forth about n-gram probabilities
    which have the bag of words issue (you can only generate what you have) vs. using a neural net system.
    I was fascinated reading this article, learning about neural nets and their applications with text
    generation, escpecially with poetry. I really love the idea of a system that is cosntantly learning
    from itself and adapting, and I think neural nets would be a great challenge for my next project. I also
    went back to this article when dealing with generation speed issues, although I wasn't able to implement
    any pruning techniques with my system.

https://www.aclweb.org/anthology/D18-1353.pdf
    I read this article and immmidietly realized I wouldn't be able to use it for much in my own work,
    but found it interesting nonetheless with this idea of mutual reinforcement learning with the two
    learner (generator) systems. This article did mention a cohenerce rewarding system, alluding to
    the fact that coherence is so important in these poems, and while I did try to reward coherence
    with my rhyming point adding system, I did not do anything this complex. Origionally I had
    each line of poetry base itself off the last word of the previous line, but I found it
    sounded like one giant run-on sentence so instead each line is based soley on the subject
    word.

Sources:
https://stackoverflow.com/questions/35722185/to-find-the-opinion-of-a-sentence-as-positive-or-negative
https://stackoverflow.com/questions/38263039/sentiwordnet-scoring-with-python 
https://www.geeksforgeeks.org/part-speech-tagging-stop-words-using-nltk-python/
https://towardsdatascience.com/basic-binary-sentiment-analysis-using-nltk-c94ba17ae386
http://www.nltk.org/book/ch05.html 