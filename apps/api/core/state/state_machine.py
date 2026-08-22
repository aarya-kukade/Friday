"""
FRIDAY AI Operating System

Central State Machine

This class is the single source of truth
for the current operating state of FRIDAY.
"""

from __future__ import annotations

import threading
from datetime import datetime

from apps.api.core.event_bus import event_bus
from apps.api.core.events import Event
from apps.api.core.state.states import FridayState


class StateChangedEvent(Event):

    previous_state: FridayState | None = None

    current_state: FridayState | None = None


class StateMachine:

    def __init__(self):

        self._lock = threading.RLock()

        self._state = FridayState.BOOTING

        self._history: list[tuple[datetime, FridayState]] = [

            (datetime.utcnow(), self._state)

        ]

    @property
    def current(self) -> FridayState:

        return self._state

    @property
    def history(self):

        return tuple(self._history)

    def is_state(self, state: FridayState) -> bool:

        return self._state == state

    def transition(self, new_state: FridayState):

        with self._lock:

            if new_state == self._state:
                return

            previous = self._state

            self._state = new_state

            self._history.append(

                (datetime.utcnow(), new_state)

            )

            event_bus.publish(

                StateChangedEvent(

                    previous_state=previous,

                    current_state=new_state,

                )

            )

    def reset(self):

        with self._lock:

            self._state = FridayState.BOOTING

            self._history.clear()

            self._history.append(

                (datetime.utcnow(), self._state)

            )

    def print_history(self):

        print("\n====== STATE HISTORY ======\n")

        for ts, state in self._history:

            print(

                f"{ts.strftime('%H:%M:%S')} -> {state.value}"

            )

        print()


state_machine = StateMachine()