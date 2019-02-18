import pyttsx3

def speechSynthesizer(sentence):
    engine = pyttsx3.init()
    engine.setProperty('voice', 'com.apple.speech.synthesis.voice.moira')
    engine.say(sentence)
    engine.runAndWait()
    
    
"""    
for voice in voices:
    print(voice, voice.id)
    engine.setProperty('voice', voice.id)
    engine.say("Hello World!")
    engine.runAndWait()
    engine.stop()
    """