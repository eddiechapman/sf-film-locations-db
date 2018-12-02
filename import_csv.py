"""
import_csv.py
Eddie Chapman

This script creates a Neo4j graph database for the "Film Locations in
San Francisco" dataset using a CSV file.

Dataset:
https://data.sfgov.org/Culture-and-Recreation/Film-Locations-in-San-Francisco/yitu-d5am
"""

from csv import DictReader
import os
from py2neo import Graph, Node, NodeMatcher, Relationship


def set_working_directory():
    """
    Set the working directory to the location of the Python script.
    """
    abs_path = os.path.abspath(__file__)
    dir_name = os.path.dirname(abs_path)
    os.chdir(dir_name)


def find_node(label, value):
    """
    Attempt to return a node that matches the specified values.

    The if/else statements address confusing difficulties
    passing the attribute key name to the match argument.
    """
    if label is 'film':
        return matcher.match(label, title=value).first()
    elif label is 'fun_facts':
        return matcher.match(label, fun_facts=value).first()
    else:
        return matcher.match(label, name=value).first()


def create_node(label, value):
    """
    Create a new node using the specified values.

    The if/else statements address confusing difficulties
    passing the attribute key name to the match argument.
    """
    if label is 'film':
        return Node(label, title=value)
    elif label is 'fun_facts':
        return Node(label, fun_facts=value)
    else:
        return Node(label, name=value)


def find_or_create_node(label, value):
    """
    Return a node by retrieving or creating one using CSV values.

    Returns none when CSV cell value is blank.
    New nodes are merged with the database.
    """
    if value in (None, ''):
        return None
    node = find_node(label, value)
    if node is None:
        node = create_node(label, value)
        transaction.create(node)
    return node


def add_label(node, label):
    """
    Add a secondary label to an existing node.
    """
    if node is None or label in node.labels:
        return
    node.add_label(label)
    transaction.merge(node, primary_label=label)


def create_relationship(node1, relationship_type, node2):
    """
    Add a relationship to two nodes as long as neither are null.
    """
    if node1 is None or node2 is None:
        return
    relationship = Relationship(node1, relationship_type, node2)
    transaction.merge(relationship)


if __name__ == '__main__':
    set_working_directory()

    # Database authentication
    graph = Graph("bolt://000000", auth=('neo4j', 'test'))

    # Use to retrieve existing nodes
    matcher = NodeMatcher(graph)

    with open('Film_Locations_in_San_Francisco.csv') as csv_file:

        fieldnames = ['title', 'release_year', 'location', 'fun_facts', 'producer', 'distributor', 'director', 'writer', 'actor_1', 'actor_2', 'actor_3']
        reader = DictReader(csv_file, fieldnames=fieldnames)
        for row in reader:

            transaction = graph.begin()

            film = find_or_create_node('film', row['title'])
            location = find_or_create_node('location', row['location'])
            fun_facts = find_or_create_node('fun_facts', row['fun_facts'])
            producer = find_or_create_node('organization', row['producer'])
            distributor = find_or_create_node('organization', row['distributor'])
            director = find_or_create_node('person', row['director'])
            writer = find_or_create_node('person', row['writer'])
            actor_1 = find_or_create_node('person', row['actor_1'])
            actor_2 = find_or_create_node('person', row['actor_2'])
            actor_3 = find_or_create_node('person', row['actor_3'])

            add_label(producer, 'producer')
            add_label(distributor, 'distributor')
            add_label(director, 'director')
            add_label(writer, 'writer')
            add_label(actor_1, 'actor')
            add_label(actor_2, 'actor')
            add_label(actor_3, 'actor')

            create_relationship(director, 'directed', film)
            create_relationship(film, 'directed_by', director)
            create_relationship(distributor, 'distributed', film)
            create_relationship(film, 'distributed_by', distributor)
            create_relationship(writer, 'wrote', film)
            create_relationship(film, 'written_by', writer)
            create_relationship(actor_1, 'starred_in', film)
            create_relationship(film, 'starring', actor_1)
            create_relationship(actor_2, 'starred_in', film)
            create_relationship(film, 'starring', actor_2)
            create_relationship(actor_3, 'starred_in', film)
            create_relationship(film, 'starring', actor_3)
            create_relationship(producer, 'produced', film)
            create_relationship(film, 'produced_by', producer)
            create_relationship(location, 'location_for', film)
            create_relationship(film, 'filmed_at', location)
            create_relationship(fun_facts, 'happened_at', location)
            create_relationship(fun_facts, 'happened_during', film)
            create_relationship(film, 'has_fact', fun_facts)
            create_relationship(location, 'has_fact', fun_facts)

            transaction.commit()

