from csv import DictReader
import os

from py2neo import Graph
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
    Create a list of unique film titles and their release years.
    Avoids cases where a film is associated with multiple release years.
    """
    films = {}
    for row in reader:
        title, release_year = row[:3]
        if title not in films:
            films[title] = release_year

    return films


if __name__ == '__main__':

    set_working_directory()

    graph = Graph(password='test')
    tx = graph.begin()

    with open('Film_Locations_In_San_Francisco.csv') as csv_file:
        reader = DictReader(csv_file)

