
import operator
from . import exceptions


class IterableAttr(object):

    def __init__(self, iterable, key):
        self._items = [item[key] for item in iterable]

    def __eq__(self, other):
        return other in self._items

    def __getitem__(self, key):
        return self.__class__(self._items, key)


def attrgetter(*items):

    if len(items) == 1:
        attr = items[0]
        def g(obj):
            return resolve_attr(obj, attr)
    else:
        def g(obj):
            return tuple(resolve_attr(obj, attr) for attr in items)
    return g

def resolve_attr(obj, attr):
    """A custom attrgetter that operates both on dictionaries and objects"""
    for name in attr.split("."):
        try:
            try:
                # Slight hack for better speed, since accessing dict is faster than getattr
                obj = obj.__dict__[name]
            except KeyError:
                obj = getattr(obj, name)

        except AttributeError:
            try:
                try:
                    obj = obj[name]
                except TypeError:
                    obj = IterableAttr(obj, name)
            except (KeyError, TypeError):
                raise exceptions.MissingAttribute('Object {0} has no attribute or key "{1}"'.format(obj, name))
    return obj

def unique_everseen(seq):
    """Solution found here : http://stackoverflow.com/questions/480214/how-do-you-remove-duplicates-from-a-list-in-python-whilst-preserving-order"""
    seen = set()
    seen_add = seen.add
    return [x for x in seq if not (x in seen or seen_add(x))]
