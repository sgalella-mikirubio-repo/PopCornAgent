from speechRecognition import speech_recognizer
from POSParser import parser_system
from ontology import undefined_managing
from speechGenerator import response_generator
from speechSynthesis import speech_synthesizer
# from IMDbCrawler import retrieveData


class PopCorn:
    """Create agent struct with different fields to be filled.
    """
    def __init__(self, voice=True, keyboard=False):
        self.year = []
        self.duration = []
        self.country = []
        self.genre = []
        self.rate = []
        self.director = []
        self.actor = []
        self.undefined1 = []
        self.undefined2 = []
        self.voice = voice
        self.keyboard = keyboard

    def __repr__(self):
        return ("Year: {}\nDuration: {}\nCountry: {}\nGenre: {}\nRate: {}\n"
                "Director: {}\nActor: {}\nUndefined1: {}\n"
                "Undefined2: {}\n".format(self.year, self.duration,
                                          self.country, self.genre, self.rate,
                                          self.director, self.actor,
                                          self.undefined1, self.undefined2))

    def say(self, message):
        print("PopCorn: {}\n".format(message))
        if self.speech:
            speech_synthesizer(message)

    def listen(self):
        if self.keyboard:
            user_message = input()
            print(">User: {}\n".format(user_message))
        else:
            print("Listening...", end="\r")
            user_message = speech_recognizer()
            print(">User: {}".format(audio_recorded[0].upper()
                                     + audio_recorded[1:]))


if __name__ == "__main__":
    film_frame = PopCorn()
    film_frame.say("Hi, I'm PopCorn. What kind of film do you want to watch?")
    to_ask = ['year', 'duration', 'country', 'genre',
              'rate', 'director', 'actor']
    while True:
        try:
            print("\nListening...", end="\r")
            audio_recorded = speech_recognizer()
        except ValueError:
            string = ("I'm sorry. I couldn't hear anything."
                      "If you need something call me back.")
            print("\nPopCorn: "+string)
            speech_synthesizer(string)
            break
        print('\rUser: ' + audio_recorded[0].upper() + audio_recorded[1:]
              + '.    ')
        film_frame = parser_system(audio_recorded, film_frame)
        print(film_frame)
        film_frame = undefined_managing(film_frame)
        movie_list, end, film_frame, to_ask = response_generator(film_frame,
                                                                 to_ask)
        if end:
            break
