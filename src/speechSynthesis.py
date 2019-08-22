"""
Project: PopCornAgent
Name: speechSynthesis.py
Authors: mikirubio & sgalella
Description: generate speech from text
"""

import pyttsx3

def speechSynthesizer(sentence):
    engine = pyttsx3.init()
    engine.setProperty('voice', 'com.apple.speech.synthesis.voice.moira')
    engine.say(sentence)
    engine.runAndWait()
    
    
""" 
Comment out to hear different available voices
for voice in voices:
    print(voice, voice.id)
    engine.setProperty('voice', voice.id)
    engine.say("Hello World!")
    engine.runAndWait()
    engine.stop()
"""