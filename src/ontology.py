import rdflib
# import rdflib.plugins.sparql as sparql
from random import randint


def undefined_managing(film_frame):
    g = rdflib.Graph()
    g.parse("../PopCornAgent/data/PopCornOntology.owl")
    row = []
    actor = []
    director = []
    if film_frame.undefined1 != []:
        q = g.query("""
        PREFIX mov:
        <http://www.semanticweb.org/sgalella/ontologies/2018/11/movieAgent#>
        SELECT ?director
        WHERE {?director mov:directs ?movie .
               ?director mov:Name ?name .
               FILTER (str(?name) = '"""+film_frame.undefined1+"""')}
        """)
        for row in q:
            director = row[0].rsplit('#')[-1]
        if director != []:
            film_frame.director = film_frame.undefined1
            film_frame.undefined1 = []
    row = []
    actor = []
    director = []
    if film_frame.undefined1 != []:
        q = g.query("""
        PREFIX mov:
        <http://www.semanticweb.org/sgalella/ontologies/2018/11/movieAgent#>
        SELECT ?actor
        WHERE {?actor mov:acts ?movie .
               ?actor mov:Name ?name .
               FILTER (str(?name) = '"""+film_frame.undefined1+"""')}
        """)
        for row in q:
            actor = row[0].rsplit('#')[-1]
        if actor != []:
            film_frame.actor = film_frame.undefined1
            film_frame.undefined1 = []
    row = []
    actor = []
    director = []
    if film_frame.undefined2 != []:
        q = g.query("""
        PREFIX mov:
        <http://www.semanticweb.org/sgalella/ontologies/2018/11/movieAgent#>
        SELECT ?director
        WHERE {?director mov:directs ?movie .
               ?director mov:Name ?name .
               FILTER (str(?name) = '"""+film_frame.undefined2+"""')}
        """)
        for row in q:
            director = row[0].rsplit('#')[-1]
        if director != []:
            film_frame.director = film_frame.undefined2
            film_frame.undefined2 = []
    row = []
    actor = []
    director = []
    if film_frame.undefined2 != []:
        q = g.query("""
        PREFIX mov:
        <http://www.semanticweb.org/sgalella/ontologies/2018/11/movieAgent#>
        SELECT ?actor
        WHERE {?actor mov:acts ?movie .
               ?actor mov:Name ?name .
               FILTER (str(?name) = '"""+film_frame.undefined2+"""')}
        """)
        for row in q:
            actor = row[0].rsplit('#')[-1]
        if actor != []:
            film_frame.actor = film_frame.undefined2
            film_frame.undefined2 = []
    return film_frame


def ontology_consulting(film_frame):
    g = rdflib.Graph()
    g.parse("../PopCornAgent/data/PopCornOntology.owl")
    string = []
    if film_frame.duration != []:
        string.append("(?duration) < %d" % film_frame.duration)
    else:
        string.append("")
    if film_frame.country != []:
        string.append("str(?country) = '%s'" % film_frame.country)
    else:
        string.append("")
    if film_frame.genre != []:
        string.append("str(?genre) = '%s'" % film_frame.genre)
    else:
        string.append("")
    if film_frame.rate != []:
        string.append("str(?rate) > '%s'" % film_frame.rate)
    else:
        string.append("")
    if film_frame.director != []:
        string.append("str(?name_director) = '%s'" % film_frame.director)
    else:
        string.append("")
    if film_frame.actor != []:
        string.append("str(?name_actor) = '%s'" % film_frame.actor)
    else:
        string.append("")
    if film_frame.year != []:
        string.append("str(?year) >= '%d'" % (film_frame.year-4))
        string.append("str(?year) <= '%d'" % (film_frame.year+4))
    else:
        string.append("")
    str_general = """
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
               FILTER ("""
    j = 0
    str_suppl = ''
    for i in range(len(string)):
        if string[i] != "" and j == 0:
            str_suppl = str_suppl + string[i]
            j = 1
        elif string[i] != "":
            str_suppl = str_suppl + " &&\n\t       " + string[i]
    # str_suppl
    str_query = str_general + str_suppl + ")}"
    q = g.query(str_query)
    movie_list = []
    for row in q:
        movie_list.append(row[0].rsplit('#')[-1])
    return movie_list


def random_movie():
    g = rdflib.Graph()
    g.parse("../PopCornAgent/data/PopCornOntology.owl")
    str_general = """
        PREFIX mov:
        <http://www.semanticweb.org/sgalella/ontologies/2018/11/movieAgent#>
        SELECT ?movie_name
        WHERE {?movie mov:Name ?movie_name .
               ?movie mov:Year ?year}
        """
    q = g.query(str_general)
    movie_list = []
    for row in q:
        movie_list.append(row[0].rsplit('#')[-1])
    index = randint(0, len(movie_list) - 1)
    return movie_list[index]
