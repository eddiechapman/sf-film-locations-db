from py2neo.ogm import Property, GraphObject, RelatedTo


class Film(GraphObject):
    '''
    Represents a film in the San Francisco Film Locations dataset.
    '''
    __primarykey__ = 'title'

    title = Property()
    release_year = Property()

    directed_by = RelatedTo(Director)
    distributed_by = RelatedTo(Distributor)
    written_by = RelatedTo(Writer)
    starring = RelatedTo(Actor)
    produced_by = RelatedTo(Producer)
    filmed_at = RelatedTo(Location)
    has_fact = RelatedTo(FunFact)
