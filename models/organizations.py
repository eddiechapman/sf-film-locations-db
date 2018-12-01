from py2neo.ogm import Property, GraphObject, Label, RelatedFrom, RelatedTo

from models.film import Film


class Organization(GraphObject):
    """
    Represents a distribution company in the San Francisco Film Locations dataset.
    """
    __primarykey__ = 'name'

    name = Property()
    organization = Label()

#     distributed = RelatedTo(Film)
#     distributed_by = RelatedFrom(Film)
#
#
# class Producer(GraphObject):
#     """
#     Represents a production company in the San Francisco Film Locations dataset.
#     """
#     __primarykey__ = 'name'
#
#     name = Property()
#     organization = Label()
#     producer = Label()
#
#     organization = True
#     producer = True
#
#     produced = RelatedTo(Film)
#     produced_by = RelatedFrom(Film)
