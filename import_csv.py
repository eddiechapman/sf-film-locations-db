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


def find_or_create_node(label, key, value):
    """
    Return a node by retrieving or creating one using CSV values.
    Returns none when CSV cell value is blank.
    New nodes are merged with the database.
    """
    if value is None:
        return None
    match = matcher.match(label, key=value)
    if match.first() is None:
        node = Node(label, key=value)
        transaction.merge(node, primary_label=label, primary_key=key)
    else:
        node = match.first()
    return node


def add_label(node, label):
    """
    Add a secondary label to an existing node.

    Check if node is not null from search/creation function and that
    label is not already applied.
    """
    if node is None or label in node.labels:
        return
    node.labels.add(label)
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

    graph = Graph("bolt://localhost:7687", auth=('neo4j', 'test'))

    # Use to retrieve existing nodes
    matcher = NodeMatcher(graph)

    with open('Film_Locations_in_San_Francisco.csv') as csv_file:
        reader = DictReader(csv_file)
        for row in reader:

            transaction = graph.begin()

            film = find_or_create_node('film', 'title', row['title'])
            location = find_or_create_node('location', 'name', row['location'])
            fun_fact = find_or_create_node('fun_fact', 'fun_fact', row['fun_fact'])
            producer = find_or_create_node('organization', 'name', row['producer'])
            distributor = find_or_create_node('organization', 'name', row['distributor'])
            director = find_or_create_node('person', 'name', row['director'])
            writer = find_or_create_node('person', 'name', row['writer'])
            actor_1 = find_or_create_node('person', 'name', row['actor_1'])
            actor_2 = find_or_create_node('person', 'name', row['actor_2'])
            actor_3 = find_or_create_node('person', 'name', row['actor_3'])

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
            create_relationship(fun_fact, 'happened_at', location)
            create_relationship(fun_fact, 'happened_during', film)
            create_relationship(film, 'has_fact', fun_fact)
            create_relationship(location, 'has_fact', fun_fact)

            transaction.commit()

