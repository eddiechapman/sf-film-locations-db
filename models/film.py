from py2neo.ogm import Property, GraphObject, Label, RelatedTo
from .people import Actor, Director, Writer
from .organizations import Producer, Distributor
from .locations import Location
from .facts import FunFact

class Film(GraphObject):
    '''
    Represents a film in the San Francisco Film Locations dataset.
    '''
    __primarykey__ = 'title'

    title = Property()
    release_year = Property()
    film = Label()

    film = True

    directed_by = RelatedTo(Director)
    distributed_by = RelatedTo(Distributor)
    written_by = RelatedTo(Writer)
    starring = RelatedTo(Actor)
    produced_by = RelatedTo(Producer)
    filmed_at = RelatedTo(Location)
    has_fact = RelatedTo(FunFact)