from models.film import Film
from py2neo.ogm import Property, GraphObject, Label, RelatedTo


class Actor(GraphObject):
    '''
    Represents a film in the San Francisco Film Locations dataset.
    '''
    __primarykey__ = 'name'

    name = Property()
    person = Label()
    actor = Label()

    person = True
    actor = True

    starred_in = RelatedTo(Film)
