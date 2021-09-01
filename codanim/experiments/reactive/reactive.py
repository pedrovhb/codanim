import asyncio
import sys
from dataclasses import dataclass
from typing import NamedTuple, Generic, TypeVar, Any, Optional, List, cast
from loguru import logger

import attr
import attr as attrs

UNINITIALIZED = object()

T = TypeVar("T")


class KnownObserver(NamedTuple):
    observer: "Observer"
    observer_attr: attr.Attribute


def on_setattr_notify_observers(
    instance: "Observable", key: attr.Attribute, value: T
) -> T:
    previous_value = getattr(instance, key.name)
    instance.notify_observers(key, previous_value, value)
    return value


_NO_PARENT_OBSERVABLE_UPDATE = ("observable_parent", "observable_parent_attr")


def on_setattr_add_parent_observable(
    instance: "Observable", key: attr.Attribute, value: T
) -> T:
    if isinstance(value, Observable):
        value.set_observable_parent(instance, key)
    return value


def on_setattr_notify_parent_observable(
    instance: "Observable", key: attr.Attribute, value: T
):
    if observable_parent := instance.observable_parent:
        parent_attr = instance.observable_parent_attr
        previous_value = getattr(instance, key.name)
        logger.trace(
            f"Child {instance} notifying parent "
            f"{observable_parent} {parent_attr.name} "
            f"of change: {previous_value} -> {value}"
        )
        observable_parent.on_child_observable_change(
            instance,
            key,
            parent_attr,
            previous_value,
            value,
        )
    return value


# [2021-08-31 01:09 PM] todo - add converter which picks up automatically which values are observable


observable_setattr_hooks = [
    on_setattr_notify_observers,
    on_setattr_add_parent_observable,
    on_setattr_notify_parent_observable,
]

reactive_observable = attrs.attrs(
    auto_detect=True,
    auto_attribs=True,
    on_setattr=observable_setattr_hooks,
    slots=True,
)


@reactive_observable
class Observable:
    observers: List["KnownObserver"] = attrs.attrib(
        init=False, factory=list, repr=False
    )
    observable_parent: Optional["Observable"] = attrs.attrib(
        default=None, init=False, repr=False
    )
    observable_parent_attr: Optional[attr.Attribute] = attrs.attrib(
        default=None, init=False, repr=False
    )

    def __attrs_post_init__(self):
        for attribute in self.__attrs_attrs__:
            if isinstance(val := getattr(self, attribute.name), Observable):
                val.set_observable_parent(self, attribute)

    def set_observable_parent(
        self,
        observable_parent: "Observable",
        observable_parent_attr: attr.Attribute,
    ) -> None:
        logger.trace(
            f"Setting {self} observable_parent to {observable_parent},"
            f" attr {observable_parent_attr}"
        )
        object.__setattr__(self, "observable_parent", observable_parent)
        object.__setattr__(
            self, "observable_parent_attr", observable_parent_attr
        )

    def on_child_observable_change(
        self,
        child: "Observable",
        child_changed_attribute: attr.Attribute,
        parent_changed_attribute: attr.Attribute,
        previous_value: Any,
        new_value: Any,
    ) -> None:
        logger.trace(
            f"Observable {self} saw (attr {parent_changed_attribute.name}) "
            f"child {child} {child_changed_attribute.name} change from "
            f"{previous_value} to {new_value}"
        )
        self.notify_observers(parent_changed_attribute, child, child)

    def add_observer(
        self, observer: "Observer", attribute: attr.Attribute
    ) -> None:
        known_observer = KnownObserver(observer, attribute)
        if known_observer not in self.observers:
            logger.trace(
                f"Adding observer {known_observer} to {self} observers"
            )
            self.observers.append(known_observer)

    def notify_observers(
        self,
        attribute: attr.Attribute,
        previous_value: T,
        new_value: T,
    ) -> None:
        logger.trace(
            f"Notifying observers "
            f"({self} {attribute.name}): {previous_value} -> {new_value}"
        )
        for observer, observer_attribute in self.observers:
            observer.on_observable_change(
                instance=self,
                instance_attribute=attribute,
                observer_attribute=observer_attribute,
                previous_value=previous_value,
                new_value=new_value,
            )


def observer_on_setattr_add_to_observable(
    instance: "Observer", key: attr.Attribute, value: T
) -> T:
    if isinstance(value, Observable):
        value.add_observer(instance, key)
    return value


observer_setattr_hooks = [observer_on_setattr_add_to_observable]

reactive_observer = attrs.attrs(
    auto_detect=True,
    auto_attribs=True,
    collect_by_mro=True,
    on_setattr=observer_setattr_hooks,
    slots=True,
)


@reactive_observer
class Observer:
    def on_observable_change(
        self,
        instance: Observable,
        instance_attribute: attr.Attribute,
        observer_attribute: attr.Attribute,
        previous_value: T,
        new_value: T,
    ) -> None:
        print(
            f"Observer {self} (attribute: {observer_attribute}) saw {instance} "
            f"{instance_attribute.name} change "
            f"from {previous_value} to {new_value}"
        )


# [2021-08-31 02:26 PM] todo - create observable list
