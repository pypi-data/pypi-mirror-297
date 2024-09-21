from abc import ABC
from typing import Optional
from threading import Lock

from dependency_needle.dependency_strategy.\
    dependency_strategy_interface import IDependencyStrategyInterface


singleton_build_lock = Lock()


class SingeltonDependencyStrategy(IDependencyStrategyInterface):
    """Scoped strategy for dependency building."""

    def _custom_post_build_strategy(self, interface: ABC,
                                    concrete_class: object,
                                    key_lookup: object) -> None:
        """Singelton post build strategy"""
        if (interface not
                in self._interface_lifetime_registery_lookup):
            self._interface_lifetime_registery_lookup[interface] = (
                concrete_class
            )

    def _custom_pre_build_strategy(self,
                                   interface: ABC,
                                   key_lookup: object) -> Optional[object]:
        """Singelton pre build strategy"""
        if (interface
                in self._interface_lifetime_registery_lookup):
            return self._interface_lifetime_registery_lookup[interface]
        return None

    def _build(self, interface: ABC, interface_registery: dict, key_lookup: object) -> object:
        with singleton_build_lock:
            return super()._build(interface, interface_registery, key_lookup)
