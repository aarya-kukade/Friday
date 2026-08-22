"""
FRIDAY AI Operating System

Base Executor Interface
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from apps.api.core.nlu.command import Command


class BaseExecutor(ABC):

    @abstractmethod
    def execute(self, command: Command):
        """
        Execute the supplied command.
        """
        raise NotImplementedError