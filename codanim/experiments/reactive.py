import asyncio
from dataclasses import dataclass
from typing import NamedTuple, Generic, TypeVar, Any, Optional, List, cast

import attr
import attr as attrs

UNINITIALIZED = object()

T = TypeVar("T")


class ObserverRegistry(NamedTuple):
    observer: "Observer"
    observer_attr: str


# class Observable(Generic[T]):
#
#     def __init__(self):
#         self.observers: List[ObserverRegistry] = []
#
#     def __get__(self, obj: Any, objtype: Optional[type] = None) -> T:
#         value = getattr(obj, self.private_name)
#         # [2021-08-28 10:12 PM] todo - intercept and check for animation
#         return value
#
#     def __set__(self, instance: Any, value: T) -> None:
#         previous_value = getattr(instance, self.private_name, UNINITIALIZED)
#         setattr(instance, self.private_name, value)
#         self.notify_observers(instance, previous_value, value)
#         # if parent_observable: parent_observable.notify_observers
#
#     def __set_name__(self, owner: Any, name: str) -> None:
#         self.public_name = name
#         self.private_name = f"_{name}"
#
#
# class Observer:
#
#     def __init__(self):
#         pass
#
#     def __setattr__(self, key, value):
#         if isinstance(value, Observable):
#             value.add_observer(self, key)
#         super().__setattr__(key, value)
#
#     def on_observable_change(
#             self,
#             instance: Any,
#             attr: str,
#             old_value: T,
#             new_value: T
#     ) -> None:
#         print(
#             f"Observable {self} saw {instance} "
#             f"{attr} change from {old_value} to {new_value}"
#         )


# def observable_setattr(instance, att, value):
#     previous_value = getattr(instance, att, attr.NOTHING)
#     object.__setattr__(instance, att, value)
#     instance.notify_observers(instance, previous_value, value)


# def observable_getattr(instance, att):
#     return object.__getattribute__(instance, att)
#     # previous_value = getattr(instance, att, attr.NOTHING)
#     # object.__setattr__(instance, att, value)
#     # instance.notify_observers(instance, previous_value, value)

# def observable_setattr(self, key: str, value: T) -> None:
#     previous_value = getattr(self, key, UNINITIALIZED)
#     object.__setattr__(self, key, value)
#     self.notify_observers(self, previous_value, value)


def ob_setattr(self, key, value):

    if isinstance(key, attr.Attribute):
        previous_value = getattr(self, key.name, key.default)
    else:
        previous_value = getattr(self, key.name, UNINITIALIZED)
    if isinstance(value, Observable):
        object.__setattr__(value, "__observable_parent", self)
    if self.is_initialized:
        self.notify_observers(self, key, previous_value, value)
    return value


@attrs.attrs(
    auto_detect=True,
    auto_attribs=True,
    collect_by_mro=True,
    on_setattr=ob_setattr,
)
class Observable(Generic[T]):
    __observers: List["ObserverRegistry"] = attrs.attrib(
        init=False, factory=list, repr=False
    )
    __observable_parent: Optional["Observable"] = attrs.attrib(
        default=None, init=False, repr=False
    )
    is_initialized: bool = attrs.attrib(default=False, init=False, repr=False)

    def __attrs_post_init__(self):
        # todo use attrs to calc __hash__? prob not
        self.is_initialized = True
        for attribute in dir(self):
            if isinstance(val := getattr(self, attribute), Observable):
                val.observable_parent = self

    def on_child_observable_change(self, instance, name, old_value, new_value):
        print(
            f"Observer {self} saw child {instance} "
            f"{name.name} change from {old_value} to {new_value}"
        )

    def add_observer(self, observer: "Observer", observer_attr: str) -> None:
        if observer not in self.__observers:
            print(f"Adding {observer_attr} attr to observer {observer}")
            self.__observers.append(ObserverRegistry(observer, observer_attr))

    def notify_observers(
        self,
        instance: Any,
        name: str,
        old_value: T,
        new_value: T,
    ) -> None:
        for ob_reg in self.__observers:
            ob_reg.observer.on_observable_change(
                instance, name, old_value, new_value
            )
        # todo - to  avoid reprocessing, pass a list of observers which observers add themselves to
        # print(self, self.observable_parent)
        if self.__observable_parent:
            self.__observable_parent.on_child_observable_change(
                instance, name, old_value, new_value
            )


@attrs.attrs(auto_detect=True, collect_by_mro=True)
class Observer:
    def __setattr__(self, key, value):
        if isinstance(value, Observable):
            value.add_observer(self, key)
        super().__setattr__(key, value)

    def on_observable_change(self, instance, name, old_value, new_value):
        print(
            f"Observable {self} saw {instance} "
            f"{name.name} change from {old_value} to {new_value}"
        )


@attrs.attrs(auto_detect=True, auto_attribs=True, on_setattr=ob_setattr)
class Position(Observable):
    x: float
    y: float


@attrs.attrs(auto_detect=True, auto_attribs=True, on_setattr=ob_setattr)
class Circle(Observable):
    # todo use attrs to set all attributes to observers, or create metaclass
    position: Position
    radius: float


async def main():
    p = Position(3, 7)
    c = Circle(p, 10)

    batch_drawer = Observer()
    batch_drawer.circle = c
    c.radius = 20
    p.x = 3
    p.y = 5
    print(p, p.x, p.y)


if __name__ == "__main__":
    asyncio.run(main())
