# main

from speechRecognition import speechRecognizer
from POSParser import parserSystem
from ontology import *
from speechGenerator import responseGenerator
from speechSynthesis import speechSynthesizer
from IMDbCrawler import retrieveData
import nltk
#import numpy as np
#from collections import namedtuple


#print("Hi, I'm PopCorn. What kind of film do you want to watch?\n")
# Corresponding to: Film Year, Duration, Country, Genre, Rate

class struct:
    def __init__(self,**kwds):
        self.__dict__.update(kwds)
    def length(self):
        for attr, value in self.__dict__.items():
            print(attr, value)
        
film_frame = struct(year = [], duration = [], country = [], genre = [], rate = [], director = [],
                    actor = [], undefined1 = [],undefined2 = [])

string = "Hi, I'm PopCorn. What kind of film do you want to watch?"
print("\nPopCorn: "+string)
speechSynthesizer(string)

to_ask = ['year', 'duration','country','genre','rate','director','actor']

while True:    
    try:
        print("\nListening...",end = "\r")
        audio_recorded = speechRecognizer()
    except:
        string = "I'm sorry. I couldn't listen anything. If you need something call me again."
        print("\nPopCorn: "+string)
        speechSynthesizer(string)
        break;
    print('\rUser: '+audio_recorded+ '    ')
    #audio_recorded = input()
    #audio_recorded = 'I want to watch a Sci-Fi movie from UK with a rate of 7.9 that lasts more than 169 minutes and from 2014 and directed by Christopher Nolan with Matthew McConaughey'
    #audio_recorded = "I want to watch a Sci-Fi movie"
    film_frame = parserSystem(audio_recorded, film_frame)
    film_frame = undefinedManaging(film_frame)
    movie_list, end, film_frame, to_ask = responseGenerator(film_frame, to_ask)
    if end == True:
        break


