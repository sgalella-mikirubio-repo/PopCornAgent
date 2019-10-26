import nltk


def parser_system(audio_to_parse, film_frame):
    """Parser of the audio. This function receives the audio from the speaker to
    tokenize and lookup to find information necessary for the agent.
    Args:
        audio_to_parse ([type]): [description]
        film_frame ([type]): [description]
    Returns:
        film_frame: [description]
    """
    sentence = audio_to_parse
    tokens = nltk.word_tokenize(sentence)
    tagged = nltk.pos_tag(tokens)
    tagged.append(['.', 'END'])
    if len(tokens) > 1:
        for i in range(1, len(tagged)):
            # Look for the word minutes or film
            if tagged[i][0] == 'movie' or tagged[i][0] == 'film':
                if tagged[i-1][1] == 'JJ':  # Look for an adjective before
                    film_frame.genre = tagged[i-1][0]  # If its a genre
                if tagged[i-1][1] == 'NN':  # If its a name, it's also a genre
                    if tagged[i-1][0] == 'terror':
                        film_frame.genre = 'horror'
                    elif tagged[i-1][0] == 'fiction':
                        film_frame.genre = 'sci-fi'
                    else:
                        film_frame.genre = tagged[i-1][0]
            elif tagged[i][1] == 'CD':
                if tagged[i][0] == "60s":
                    film_frame.year = 1960
                elif tagged[i][0] == "70s":
                    film_frame.year = 1970
                elif tagged[i][0] == "80s":
                    film_frame.year = 1980
                elif tagged[i][0] == "90s":
                    film_frame.year = 1990
                elif float(tagged[i][0]) > 1000:
                    film_frame.year = int(tagged[i][0])
                elif float(tagged[i][0]) < 10:
                    film_frame.rate = tagged[i][0]
                else:
                    film_frame.duration = int(tagged[i][0])
            elif tagged[i][1] == 'NNP':
                if film_frame.undefined1 == []:
                    if tagged[i+1][1] == 'NNP':
                        if tagged[i][0] == 'United' and \
                                tagged[i+1][0] == 'Kingdom':
                            film_frame.country = 'UK'
                        else:
                            film_frame.undefined1.append(tagged[i][0])
                            film_frame.undefined1.append(tagged[i+1][0])
                            film_frame.undefined1 = film_frame.undefined1[0]
                            + ' ' + film_frame.undefined1[1]
                    elif tagged[i-1][1] != 'NNP' and tagged[i+1][1] != 'NNP':
                        if tagged[i][0] == 'America':
                            film_frame.country = 'USA'
                        else:
                            film_frame.country = tagged[i][0]
                elif film_frame.undefined1 != []:
                    if tagged[i+1][1] == 'NNP':
                        if tagged[i][0] == 'United' and \
                                tagged[i+1][0] == 'Kingdom':
                            film_frame.country = 'UK'
                        else:
                            film_frame.undefined1.append(tagged[i][0])
                            film_frame.undefined1.append(tagged[i+1][0])
                            film_frame.undefined1 = film_frame.undefined1[0]
                            + ' ' + film_frame.undefined1[1]
                    elif tagged[i-1][1] != 'NNP' and tagged[i+1][1] != 'NNP':
                        if tagged[i][0] == 'America':
                            film_frame.country = 'USA'
                        else:
                            film_frame.country = tagged[i][0]
            elif tagged[i][0] == "sixties":
                film_frame.year = 1960
            elif tagged[i][0] == "seventies":
                film_frame.year = 1970
            elif tagged[i][0] == "eighties":
                film_frame.year = 1980
            elif tagged[i][0] == "nineties":
                film_frame.year = 1990
    return film_frame
