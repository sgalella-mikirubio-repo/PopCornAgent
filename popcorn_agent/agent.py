import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import nltk
import os
import pyttsx3
import random
import rdflib
import speech_recognition as sr
from bs4 import BeautifulSoup
from urllib.request import urlopen
from urllib.request import urlretrieve


class PopCornAgent:
    """Create a PopCornAgent. The agent interacts with the user to provide
       recommendations about movies.
    """

    def __init__(self, voice=True, voice_type='moira', keyboard=False):
        """
        __init__ Constructor of the class PopCornAgent
        Args:
            voice (bool, optional): Determines if the agent uses the voice to
                communicate or uses just text. Defaults to True.
            voice_type (str, optional): Voice type of the agent. To hear
                the different voices available, look the method list_voices().
                Defaults to 'Moira'.
            keyboard (bool, optional): If false, the user interacts with
                the agent using the voice. Uses the keyboard otherwise.
                Defaults to False.
        """
        self.year = []
        self.duration = []
        self.country = []
        self.genre = []
        self.rate = []
        self.director = []
        self.actor = []
        self.name1 = []
        self.name2 = []
        self.movie_list = []
        self.to_ask = ['genre', 'actor', 'director']
        self.ontology = "../PopCornAgent/data/PopCornOntology.owl"
        self.voice = voice
        self.voice_type = voice_type
        self.keyboard = keyboard
        self.end = False

    def __repr__(self):
        """
        __repr__ Printable information of the PopCornAgent class.
        Returns:
            [str]: Movie information detected by the agent.
        """
        return ("Year: {}\nDuration: {}\nCountry: {}\nGenre: {}\nRate: {}\n"
                "Director: {}\nActor: {}\nname1: {}\n"
                "name2: {}\n".format(self.year, self.duration,
                                     self.country, self.genre, self.rate,
                                     self.director, self.actor,
                                     self.name1, self.name2))

    def speak(self, message):
        """
        speak Reproduces agent information by text and voice, if applicable.
        Args:
            message (str): Message from the agent.
        """
        print("PopCorn: {}".format(message))
        if self.voice:
            engine = pyttsx3.init()
            engine.setProperty("voice",
                               "com.apple.speech.synthesis"
                               ".voice.{}".format(self.voice_type))
            engine.say(message)
            engine.runAndWait()

    def listen(self):
        """
        listen Reproduces user information introduced by text or voice.
        """
        if self.keyboard:
            user_message = input("> User: ")
        else:
            print("Listening...", end="\r")
            r = sr.Recognizer()
            mic = sr.Microphone()
            with mic as source:
                audio = r.listen(source)
            user_message = r.recognize_google(audio)
            print("> User: {}".format(user_message[0].upper()
                                      + user_message[1:]))
        return user_message

    def parser(self, user_message):
        """
        parser This function receives the audio from the speaker to
        tokenize and lookup to find information necessary for the agent.
        Args:
            user_message (str): Audio received by the speech recognizer.
        Returns:
            tokens (list): Tokenized message from the user.
        """
        sentence = user_message
        tokens = nltk.word_tokenize(sentence)
        tagged = nltk.pos_tag(tokens)
        tagged.append(['.', 'END'])
        if len(tokens) > 1:
            for i in range(1, len(tagged)):
                # Look for the word minutes or film
                if tagged[i][0] == 'movie' or tagged[i][0] == 'film':
                    if tagged[i-1][1] == 'JJ':  # Look for an adjective before
                        self.genre = tagged[i-1][0]  # If its a genre
                    if tagged[i-1][1] == 'NN':  # If its a name, it's a genre
                        if tagged[i-1][0] == 'terror':
                            self.genre = 'horror'
                        elif tagged[i-1][0] == 'fiction':
                            self.genre = 'sci-fi'
                        else:
                            self.genre = tagged[i-1][0]
                elif tagged[i][1] == 'CD':
                    if tagged[i][0] == "60s":
                        self.year = 1960
                    elif tagged[i][0] == "70s":
                        self.year = 1970
                    elif tagged[i][0] == "80s":
                        self.year = 1980
                    elif tagged[i][0] == "90s":
                        self.year = 1990
                    elif float(tagged[i][0]) > 1000:
                        self.year = int(tagged[i][0])
                    elif float(tagged[i][0]) < 10:
                        self.rate = tagged[i][0]
                    else:
                        self.duration = int(tagged[i][0])
                elif tagged[i][1] == 'NNP':
                    if self.name1 == []:
                        if tagged[i+1][1] == 'NNP':
                            if (tagged[i][0] == 'United' and
                                    tagged[i+1][0] == 'Kingdom'):
                                self.country = 'UK'
                            else:
                                self.name1.append(tagged[i][0])
                                self.name1.append(tagged[i+1][0])
                                self.name1 = (self.name1[0]
                                              + ' ' + self.name1[1])
                        elif (tagged[i-1][1] != 'NNP' and
                                tagged[i+1][1] != 'NNP'):
                            if tagged[i][0] == 'America':
                                self.country = 'USA'
                            else:
                                self.country = tagged[i][0]
                    elif self.name1 != []:
                        if tagged[i+1][1] == 'NNP':
                            if (tagged[i][0] == 'United' and
                                    tagged[i+1][0] == 'Kingdom'):
                                self.country = 'UK'
                            else:
                                self.name2.append(tagged[i][0])
                                self.name2.append(tagged[i+1][0])
                                self.name2 = (self.name2[0]
                                              + ' ' + self.name2[1])
                        elif (tagged[i-1][1] != 'NNP' and
                                tagged[i+1][1] != 'NNP'):
                            if tagged[i][0] == 'America':
                                self.country = 'USA'
                            else:
                                self.country = tagged[i][0]
                elif tagged[i][0] == "sixties":
                    self.year = 1960
                elif tagged[i][0] == "seventies":
                    self.year = 1970
                elif tagged[i][0] == "eighties":
                    self.year = 1980
                elif tagged[i][0] == "nineties":
                    self.year = 1990
        return tokens
        # self.name_managing()  # TODO: Send parsed string to manage query

    def name_managing(self):
        """
        name_managing Manages names and possible questions to ask to the user.
        """
        g = rdflib.Graph()
        g.parse(self.ontology)
        for field in self.to_ask:
            if eval('self.{}'.format(field)):
                self.to_ask.remove(field)
        while self.name1:
            # Check if name 1 is a director
            q_director = g.query("""
            PREFIX mov:
            <http://www.semanticweb.org/sgalella/ontologies/2018/11/movieAgent#>
            SELECT ?director
            WHERE {?director mov:directs ?movie .
                ?director mov:Name ?name .
                FILTER (str(?name) = '"""+self.name1+"""')}
            """)
            if q_director:
                self.director, self.name1, self.name2 = \
                    self.name1, self.name2, []
            # Check if name 1 is an actor
            if self.name1:  # If name1 is not empty, it might be an actor
                q_actor = g.query("""
                PREFIX mov:
                <http://www.semanticweb.org/sgalella/ontologies/2018/11/movieAgent#>
                SELECT ?actor
                WHERE {?actor mov:acts ?movie .
                    ?actor mov:Name ?name .
                    FILTER (str(?name) = '"""+self.name1+"""')}
                """)
                if q_actor:
                    self.actor, self.name1, self.name2 = \
                        self.name1, self.name2, []
            # If name1 is not a director nor an actor
            if not q_director and not q_actor:
                self.speak("Sorry, we could not find any information about {}"
                           ". Please, try again.".format(self.name1))
                self.name1, self.name2 = [], []
                break

    def consult_ontology(self):
        """
        consult_ontology Consultes the ontology from the .owl fiel.
        """
        # TODO: Correct error when there is no filled field
        g = rdflib.Graph()
        g.parse(self.ontology)
        fields = []
        if self.duration:
            fields.append("(?duration) < {}".format(self.duration))
        if self.country:
            fields.append("str(?country) = '{}'".format(self.country))
        if self.genre:
            fields.append("str(?genre) = '{}'".format(self.genre))
        if self.rate:
            fields.append("str(?rate) > '{}'".format(str(self.rate)))
        if self.director:
            fields.append("str(?name_director) = '{}'".format(self.director))
        if self.actor:
            fields.append("str(?name_actor) = '{}'".format(self.actor))
        if self.year:
            fields.append("str(?year) >= '{}'".format(self.year-4))
            fields.append("str(?year) <= '{}'".format(self.year+4))
        queries_blueprint = ("""
            PREFIX mov:
            <http://www.semanticweb.org/sgalella/ontologies/2018/11/movieAgent#>
            SELECT ?movie_name
            WHERE {?movie mov:Name ?movie_name .
                ?movie mov:Year ?year .
                ?movie mov:Duration ?duration .
                ?movie mov:Genre ?genre .
                ?movie mov:Country ?country .
                ?movie mov:Rate ?rate .
                ?director mov:directs ?movie .
                ?director mov:Name ?name_director .
                ?actor mov:acts ?movie .
                ?actor mov:Name ?name_actor .
                FILTER (""")
        for idx, field in enumerate(fields):
            if idx == len(fields) - 1:
                queries_blueprint += field + ")}"
            else:
                queries_blueprint += field + " &&\n\t       "
        queries = g.query(queries_blueprint)
        for query in queries:
            self.movie_list.append(query[0].rsplit('#')[-1])
        # TODO: If the same query is done twice, the films in movie list are
        # duplicated

    def response_generator(self):
        """
        response_generator Dialogue manager of the agent. Depending on the
        information from the film, it will ask for another information or
        it will recommend a film.
        """
        if not len(self.to_ask):
            idx = random.randint(0, len(self.movie_list)-1)
            self.speak("Okay! I would give you a personal recommendation. "
                       "Have you seen {}?".format(self.movie_list[idx]))
            user_message = self.listen()
            tokens = self.parser(user_message)
            tokens = [token.lower() for token in tokens]
            if 'yes' in tokens:
                self.speak("Such a great movie, right? If you want to "
                           "look for another film, let me know. See you!")
                self.end = True
            elif 'no' in tokens:
                self.speak("Nice! I retrieved information of the "
                           "film. Read the description. I hope you like it! "
                           "If you need a recommendation for another film, "
                           "you know where to find me.")
                self.retrieve_data(self.movie_list[idx])
                self.end = True
        else:
            if len(self.movie_list) == 0:
                self.speak("I\'m sorry! There is no movie with the data "
                           "provided. See you next time!")
                self.end = True
            elif len(self.movie_list) == 1:
                self.speak("I propose you to watch {}! "
                           "Have you watched it?".format(self.movie_list[0]))
                user_message = self.listen()
                tokens = self.parser(user_message)
                tokens = [token.lower() for token in tokens]
                if 'no' in tokens:
                    self.speak("Perfect! I hope you enjoy it. I leave "
                               "you some information. See you next time!")
                    self.retrieve_data(self.movie_list[0])
                    self.end = True
                elif 'yes' in tokens:
                    self.speak("I\'m sorry, I don\'t have any other "
                               "film. If you want to see a different movie, "
                               "you know where to find me. See you!")
                    self.end = True
            elif len(self.movie_list) == 2:
                self.speak("I have a couple of recommendations. Have "
                           "you seen {}?".format(self.movie_list[0]))
                user_message = self.listen()
                tokens = self.parser(user_message)
                tokens = [token.lower() for token in tokens]
                if 'no' in tokens:
                    self.speak("Perfect! I hope you enjoy it. I leave you "
                               "some information. See you next time!")
                    self.retrieve_data(self.movie_list[0])
                    self.end = True
                elif 'yes' in tokens:
                    self.speak("And..., "
                               "what about {}?".format(self.movie_list[1]))
                    user_message = self.listen()
                    tokens = self.parser(user_message)
                    tokens = [token.lower() for token in tokens]
                    if 'yes' in tokens:
                        self.speak("I'm sorry, I don't have any more "
                                   "movies to recommend with your "
                                   "requirements. See you next time!")
                        self.end = True
                    elif 'no' in tokens:
                        self.speak("Perfect! I hope you enjoy it. "
                                   "I leave you some information. "
                                   "See you next time!")
                        self.retrieve_data(self.movie_list[1])
                        self.end = True
            else:
                idx = random.randint(0, len(self.to_ask)-1)
                rand_quest = random.randint(0, 4)
                if rand_quest == 0:
                    self.speak("Can you tell me anything about the {} "
                               "of the film?".format(self.to_ask[idx]))
                    self.to_ask.remove(self.to_ask[idx])
                elif rand_quest == 1:
                    self.speak("What about any {} of the movie. "
                               "Do you have something "
                               "in mind?".format(self.to_ask[idx]))
                    self.to_ask.remove(self.to_ask[idx])
                elif rand_quest == 2:
                    self.speak("I need more info! Do you have any "
                               "preferences regarding the {} of "
                               "the movie?".format(self.to_ask[idx]))
                    self.to_ask.remove(self.to_ask[idx])
                elif rand_quest == 3:
                    self.speak("Could you give more information of "
                               "the {}?".format(self.to_ask[idx]))
                    self.to_ask.remove(self.to_ask[idx])
                elif rand_quest == 4:
                    self.speak("Do prefer any {} in "
                               "particular?".format(self.to_ask[idx]))
                    self.to_ask.remove(self.to_ask[idx])
                elif rand_quest == 5:
                    self.speak("I see. Then, can you say say something "
                               "about {} of the "
                               "film?".format(self.to_ask[idx]))
                    self.to_ask.remove(self.to_ask[idx])
                elif rand_quest == 6:
                    self.speak("Aha. In that case, I will ask you "
                               "about {} of the "
                               "movie?".format(self.to_ask[idx]))
                    self.to_ask.remove(self.countryto_ask[idx])

    def retrieve_data(self, movie):
        """
        retrieve_data When a movie is selected, the agent retrieves information
        from the IMDb webpage.
        Args:
            movie (str): Movie selected by the agent to recommend.
        """
        g = rdflib.Graph()
        g.parse("../PopCornAgent/data/PopCornOntology.owl")
        # Get the movie URL
        query_url = g.query("""
            PREFIX mov:
            <http://www.semanticweb.org/sgalella/ontologies/2018/11/movieAgent#>
            SELECT ?code
            WHERE {?movie mov:URLcode ?code .
                ?movie mov:Name ?name .
                FILTER (str(?name) = '"""+movie+"""')}
            """)
        for query in query_url:
            URLcode = query[0].rsplit('#')[-1]
        # Get if the movie is available on Netflix
        query_Netflix = g.query("""
            PREFIX mov:
            <http://www.semanticweb.org/sgalella/ontologies/2018/11/movieAgent#>
            SELECT ?netflix
            WHERE {?movie mov:inNetflix ?netflix .
                ?movie mov:Name ?name .
                FILTER (str(?name) = '"""+movie+"""')}
            """)
        for query in query_Netflix:
            in_Netflix = query[0].rsplit('#')[-1]
        quote_page = 'https://www.imdb.com/title/tt' + URLcode
        page = urlopen(quote_page)
        soup = BeautifulSoup(page, 'html.parser')
        # Retrieve image from IMDb
        imgs = soup.findAll("div", {"class": "poster"})
        for img in imgs:
            for a in img.find_all('img', alt=True):
                link = a['src']
        urlretrieve(link, "image.png")
        image_movie = mpimg.imread("image.png", 0)
        plt.imshow(image_movie)
        plt.axis('off')
        plt.show()
        # Find different information of the film
        tdTags = soup.find_all("div", {"class": "title_wrapper"})
        for tag in tdTags:
            a = tag.find_all("h1")
            for i in a:
                name = i.text
        name = name.split()
        name = ' '.join(name[0:len(name)-1])
        print("\nName: {}\n".format(name))
        rate_box = soup.find('span', attrs={'itemprop': 'ratingValue'})
        rate = rate_box.text.strip()
        year_box = soup.find('span', attrs={'id': 'titleYear'})
        year = year_box.text.strip()
        print("Rate: \n".format(rate))
        print("Year: {}\n".format(year[1:5]))
        labels = ['Director: ', 'Writers: ', 'Actors: ']
        tdTags = soup.find_all("div", {"class": "credit_summary_item"})
        idx1 = 0
        for tag in tdTags:
            tdTags = tag.find_all("a", href=True)
            if idx1 == 0:
                print(labels[idx1], end="")
            else:
                print("\n\n"+labels[idx1], end="")
            idx1 += 1
            idx2 = 0
            for tag in tdTags:
                if tag.text == 'See full cast & crew' or \
                        tag.text == '1 more credit' or \
                        tag.text == '2 more credit' or \
                        tag.text == '3 more credits':
                    continue
                if idx2 == 0:
                    print(tag.text, end="")
                    idx2 += 1
                else:
                    print(", "+tag.text, end="")
        tdTags = soup.find_all("div", {"class": "inline canwrap"})
        for tag in tdTags:
            a = tag.find_all("span")
            for i in a:
                description = i.text
        print("\nAvailable in Netflix: Yes") if in_Netflix \
            else print("Available in Netflix: No")
        print("\nDescription: "+' '.join(description.split()))
        print("\nIf you want more information, you can go to "+quote_page+'\n')
        os.remove("image.png")

    def list_voices(self):
        """
        list_voices Displays the different available voices for the agent.
        """
        engine = pyttsx3.init()
        voices = engine.getProperty('voices')
        for voice in voices:
            print(voice, voice.id)
            engine.setProperty('voice', voice.id)
            engine.say("Hello World!")
            engine.runAndWait()
            engine.stop()
