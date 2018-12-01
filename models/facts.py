from py2neo.ogm import Property, GraphObject, Label, RelatedTo

from models.film import Film
from models.locations import Location


class FunFact(GraphObject):
    '''
    Represents a fun fact about a film in the San Francisco Film Locations dataset.
    '''
    __primarykey__ = 'fun_fact'

    fun_fact = Property()
    fact = Label()

    fact = True

    happened_during = RelatedTo(Film)
    happened_at = RelatedTo(Location)
