import math
import pickle
import time
from datetime import timedelta

import attr
from pyglet import shapes


def __no_reference_converter(value):
    if isinstance(value, Element):
        return value.copy()
    return value


def __ensure_no_references(cls, fields):
    result = [f.evolve(converter=__no_reference_converter) for f in fields]
    return result


# [2021-07-29 08:21 PM] todo - component bag metaclass that generates classes
# and caches them for a given set of properties, so that copying is essentially
# free because all objs have the same properties


# [2021-07-29 08:24 PM] todo - related to the above - or, instead of generating
# on the fly, they're generated by flattening the composition structure and
# returning objects which only have flat members, could even be dataobjects

attrs_options = dict(
    auto_attribs=True, field_transformer=__ensure_no_references, slots=True
)


@attr.s(**attrs_options)
class Element:
    def copy(self):
        # it's faster than deepcopy and doesn't require recursing ¯\_(ツ)_/¯
        return pickle.loads(pickle.dumps(self))

    def with_offset(self, **kwargs):
        # todo docstrings
        copy = self.copy()
        return self._modified_copy(copy, True, kwargs)

    def but_with(self, **kwargs):
        copy = self.copy()
        return self._modified_copy(copy, False, kwargs)

    @staticmethod
    def _set_stuff(is_offset, cpy, attribute, value):
        # todo rename
        if is_offset:
            crt_value = getattr(cpy, attribute)
            setattr(cpy, attribute, crt_value + value)
        else:
            setattr(cpy, attribute, value)

    @classmethod
    def _modified_copy(cls, copy, is_offset: bool, mod_mapping: dict):
        """Return a copy of the element, but with one or more fields modified.

        Nested elements can have their fields modified by nesting with __.
        For example:
        """

        for attribute, value in mod_mapping.items():

            path = attribute.split("__")

            if len(path) == 1:
                # Non-nested attribute change
                cls._set_stuff(is_offset, copy, attribute, value)

            else:
                # Nested attribute change, e.g. circle__position__x=4
                *nested_attr_chain, attribute = path
                obj = copy
                for nested_attr in nested_attr_chain:
                    obj = getattr(obj, nested_attr)
                cls._set_stuff(is_offset, obj, attribute, value)

        return copy


@attr.s(**attrs_options)
class Position(Element):
    x: int
    y: int


@attr.s(**attrs_options)
class Color(Element):
    r: int
    g: int
    b: int
    # a: float = 1

    def as_tuple(self):
        return self.r, self.g, self.b


# I would like to be able to say circle.pos.x += 3
# I would also like to be able to pass the same pos to something else, and have it be a copy
# maybe override __init__/new to assign to self copies of elements instead of references?


@attr.s(**attrs_options)
class Circle(Element):
    position: Position
    radius: int
    color: Color

    def add_to_batch(self, batch):
        return [
            shapes.Circle(
                self.position.x,
                self.position.y,
                self.radius,
                color=self.color.as_tuple(),
                batch=batch,
            )
        ]
