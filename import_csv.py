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


if __name__ == '__main__':

    set_working_directory()

    graph = Graph(password='test')
    tx = graph.begin()

    with open('Film_Locations_In_San_Francisco.csv') as csv_file:
        reader = DictReader(csv_file)

