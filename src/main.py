"""
Project: PopCornAgent
Name: main.py
Authors: mikirubio & sgalella
Description: main of the program
"""

from speechRecognition import speechRecognizer
from POSParser import parserSystem
from ontology import *
from speechGenerator import responseGenerator
from speechSynthesis import speechSynthesizer
from IMDbCrawler import retrieveData
import nltk


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


if __name__ == "__main__":

    while True:
        try:
            print("\nListening...",end = "\r")
            audio_recorded = speechRecognizer()
        except:
            string = "I'm sorry. I couldn't hear anything. If you need something call me back."
            print("\nPopCorn: "+string)
            speechSynthesizer(string)
            break
        print('\rUser: '+audio_recorded[0].upper() + audio_recorded[1:]+ '.    ')
        film_frame = parserSystem(audio_recorded, film_frame)
        film_frame = undefinedManaging(film_frame)
        movie_list, end, film_frame, to_ask = responseGenerator(film_frame, to_ask)
        if end:
            break


