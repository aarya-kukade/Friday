"""
Execution Engine

Receives Commands and dispatches them
to the correct executor.
"""

from __future__ import annotations

from apps.api.core.eventbus import event_bus

from apps.api.core.events import IntentReadyEvent

from .registry import registry


class ExecutionEngine:

    def __init__(self):

        self.executed_commands = 0

    def start(self):

        event_bus.subscribe(

            IntentReadyEvent,

            self.execute,

        )

        print("Execution Engine Started")

    def stop(self):

        event_bus.unsubscribe(

            IntentReadyEvent,

            self.execute,

        )

    def execute(self, event):

        command = event.command

        executor = registry.get(command.intent)

        if executor is None:

            print(f"No executor for {command.intent}")

            return

        executor.execute(command)

        self.executed_commands += 1


execution_engine = ExecutionEngine()