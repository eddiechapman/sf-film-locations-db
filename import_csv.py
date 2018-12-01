from csv import DictReader
import os

from py2neo import Graph
from .film import Film
from .people import Actor, Director, Writer
from .organizations import Producer, Distributor
from .locations import Location
from .facts import FunFact


def set_working_directory():
    """
    Set the working directory to the location of the Python script.
    """
    abs_path = os.path.abspath(__file__)
    dir_name = os.path.dirname(abs_path)
    os.chdir(dir_name)


def list_films(reader):
    """
    Create a dictionary of unique film titles and their release years.
    Avoids cases where a film is associated with multiple release years.
    """
    films = {}
    for row in reader:
        title, release_year = row[:3]
        if title not in films:
            films[title] = {'title': title, 'release_year': release_year}

    return films


def create_films(films):
    """
    Create node objects for the deduplicated films.
    """
    film_nodes = []

    for film_info in films.keys:
        film = Film(film_info)
        film.title = films['title']
        film.release_year = int(films['release_year'])
        film.film = True
        film_nodes.append(film)

    return film_nodes



def list_film_location_and_fact(reader):
    film_location_and_fact = {}



if __name__ == '__main__':

    set_working_directory()

    graph = Graph(password='test')
    tx = graph.begin()

    with open('Film_Locations_In_San_Francisco.csv') as csv_file:
        reader = DictReader(csv_file)
        films = list_films(reader)

