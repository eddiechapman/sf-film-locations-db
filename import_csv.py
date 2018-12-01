from csv import DictReader
import os

from py2neo import Graph
from .film import Film
from .people import Person
from .organizations import Organization
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


def list_people(reader):
    people = set()
    for row in reader:
        people.add(row['director'])
        people.add(row['writer'])
        people.add(row['actor_1'])
        people.add(row['actor_2'])
        people.add(row['actor_3'])

    return list(people)


def list_organizations(reader):
    organizations = set()
    for row in reader:
        organizations.add(row['producer'])
        organizations.add(row['distributor'])

    return list(organizations)


def list_locations(reader):
    locations = set(row['locations'] for row in reader)

    return list(locations)


def list_fun_facts(reader):
    fun_facts = set(row['locations'] for row in reader)

    return list(fun_facts)


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


def create_people(people):
    people_nodes = []

    for name in people:
        person = Person()
        person.name = name
        person.person = True
        people_nodes.append(person)

    return people_nodes


def create_organizations(organizations):
    organization_nodes = []

    for name in organizations:
        organization = Organization()
        organization.name = name
        organization.organization = True
        organization_nodes.append(organization)

    return organization_nodes


def create_locations(locations):
    location_nodes = []

    for name in locations:
        location = Location()
        location.name = name
        location.location = True
        location_nodes.append(location)

    return location_nodes


if __name__ == '__main__':

    set_working_directory()

    graph = Graph(password='test')
    tx = graph.begin()

    with open('Film_Locations_In_San_Francisco.csv') as csv_file:
        reader = DictReader(csv_file)

        films = list_films(reader)
        locations = list_locations(reader)
        producers = list_producers(reader)
        directors = list_directors(reader)
        writers = list_writers(reader)
        actors = list_actors(reader)

        film_nodes = create_films(films)

