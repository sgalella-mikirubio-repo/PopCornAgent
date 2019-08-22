"""
Project: PopCornAgent
Name: speechGenerator.py
Authors: mikirubio & sgalella
Description: generate different answers according to the dialogue manager
"""

from ontology import *
from speechRecognition import speechRecognizer
from speechSynthesis import speechSynthesizer
from IMDbCrawler import retrieveData
import nltk

def responseGenerator(film_frame, to_ask):
    
    from ontology import ontologyConsulting
    try:
        movie_list = ontologyConsulting(film_frame)
    except:
        movie_list = 'Unrecognized'
        
    for attr, value in film_frame.__dict__.items():
        if value !=[]:
            if attr in to_ask:
                to_ask.remove(attr)

    
    if len(to_ask) == 0:
        idx = idx = randint(0,len(movie_list)-1)
        string = 'You haven\'t given me enought information. I would give you a personal recommendation then :). Have you seen '+ movie_list[idx] + '?'
        print("\nPopCorn: "+string)
        speechSynthesizer(string)
        print("\nListening...",end = "\r")
        audio_recorded = speechRecognizer()
        tokens = nltk.word_tokenize(audio_recorded)
        if 'yes' in tokens:
            string = "Such a great movie, right? If you want to look for another film, let me know. See you!"
            print("\nPopCorn: "+string)
            speechSynthesizer(string)
            end = True
        elif 'no' in tokens:
            string = "Nice! I retrieved information about the film. Read the description. I hope you like it! If you need a recommendation for another film, you know where to find me."
            print("\nPopCorn: "+string)
            speechSynthesizer(string)
            retrieveData(movie_list[idx])
            end = True
    else:
        if len(movie_list) == 0:
            string = 'I\'m sorry! There is no movie with the data provided. See you next time!'
            print("\nPopCorn: "+string)
            speechSynthesizer(string)
            end = True
        elif len(movie_list) == 1:
            string = 'I propose you to watch '+movie_list[0]+'! Have you watched it?'
            print("\nPopCorn: "+string)
            speechSynthesizer(string)
            print("\nListening...",end = "\r")
            audio_recorded = speechRecognizer()
            tokens = nltk.word_tokenize(audio_recorded)
            print('\rUser: '+audio_recorded[0].upper() + audio_recorded[1:]+ '.    ')
            if 'no' in tokens:
                string = "Perfect! I hope you enjoy it. I leave you some information. See you next time!"
                print("\nPopCorn: "+string)
                speechSynthesizer(string)
                retrieveData(movie_list[0])
                end = True
            elif 'yes' in tokens:
                string = 'I\'m sorry, I don\'t have any other film. If you want to see a different movie, you know where to find me. See you!'
                print("\nPopCorn: "+string)
                speechSynthesizer(string)
                end = True
        elif len(movie_list) == 2:
            string = 'I have a couple of recommendations. Have you seen '+movie_list[0]+'?'
            print("\nPopCorn: "+string)
            speechSynthesizer(string)
            print("\nListening...",end = "\r")
            audio_recorded = speechRecognizer()
            tokens = nltk.word_tokenize(audio_recorded)
            print('\rUser: '+audio_recorded[0].upper() + audio_recorded[1:]+ '.    ')
            if 'no' in tokens:
                string = "Perfect! I hope you enjoy it. I leave you some information. See you next time!"
                print("\nPopCorn: "+string)
                speechSynthesizer(string)
                retrieveData(movie_list[0])
                end = True
            elif 'yes' in tokens:
                string = 'And..., what about '+movie_list[1]+'?'
                print("\nPopCorn: "+string)
                speechSynthesizer(string)
                print("\nListening...",end = "\r")
                audio_recorded = speechRecognizer()
                tokens = nltk.word_tokenize(audio_recorded)
                print('\rUser: '+audio_recorded[0].upper() + audio_recorded[1:]+ '.    ')
                if 'yes' in tokens:
                    string = "I'm sorry, I don't have any more movies to recommend with your requirements. See you next time!"
                    print("\nPopCorn: "+string)
                    speechSynthesizer(string)
                    end = True
                    '''
                    film_frame.year = []; film_frame.genre = []; film_frame.actor = []; 
                    film_frame.duration = []; film_frame.rate = []; film_frame.undefined1 = [];
                    film_frame.country = []; film_frame.director = []; film_frame.undefined2 = [];
                    '''
                elif 'no' in tokens:
                    string = "Perfect! I hope you enjoy it. I leave you some information. See you next time!"
                    print("\nPopCorn: "+string)
                    speechSynthesizer(string)
                    retrieveData(movie_list[1])
                    end = True
        elif movie_list == 'Unrecognized':
            movie_list = [[]]
            movie_list[0] = randomMovie();
            string = 'I have not understood you. However, I propose you to watch '+movie_list[0]+'!\n.  I leave you some information. Enjoy the movie!'
            end = True
        else:
            idx = randint(0,len(to_ask)-1)
            rand_quest = randint(0,4)
            if rand_quest == 0:
                string = 'Can you tell me anything about the '+ to_ask[idx] + ' of the film?'
                print("\nPopCorn: "+string)
                speechSynthesizer(string)
                to_ask.remove(to_ask[idx])
                end = False
            elif rand_quest == 1:
                string = 'What about the ' + to_ask[idx] + ' of the movie. Do you have something in mind?' 
                print("\nPopCorn: "+string)
                speechSynthesizer(string)
                to_ask.remove(to_ask[idx]) 
                end = False
            elif rand_quest == 2:
                string = 'I need more info! Do you have any preferences regarding the ' + to_ask[idx] + ' of the movie?'
                print("\nPopCorn: "+string)
                speechSynthesizer(string)
                to_ask.remove(to_ask[idx])   
                end = False
            elif rand_quest == 3:
                string = 'Could you give more information of the '+ to_ask[idx] + '?'
                print("\nPopCorn: "+string)
                speechSynthesizer(string)
                to_ask.remove(to_ask[idx])  
                end = False
            elif rand_quest == 4:
                string = 'Do prefer any '+ to_ask[idx] + ' in particular?'
                print("\nPopCorn: "+string)
                speechSynthesizer(string)
                to_ask.remove(to_ask[idx]) 
                end = False
            elif rand_quest == 5:
                string = 'I see. Then, can you say say something about '+ to_ask[idx]+ ' of the film?'
                print("\nPopCorn: "+string)
                speechSynthesizer(string)
                to_ask.remove(to_ask[idx]) 
                end = False
            elif rand_quest == 6:
                string = 'Aha. In that case, I will ask you about '+ to_ask[idx] + ' of the movie?'
                print("\nPopCorn: "+string)
                speechSynthesizer(string)
                to_ask.remove(to_ask[idx]) 
                end = False

        
    
    return movie_list, end, film_frame, to_ask

