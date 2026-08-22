"""
FRIDAY AI Operating System

Thread-safe asynchronous Event Bus.

Every subsystem communicates through this module.

Author: FRIDAY Core
"""

from __future__ import annotations

import queue
import threading
from collections import defaultdict
from typing import Callable
from typing import Type

from .events import Event


EventHandler = Callable[[Event], None]


class EventBus:

    def __init__(self):

        self._subscribers: dict[
            Type[Event],
            list[EventHandler],
        ] = defaultdict(list)

        self._queue: queue.Queue[Event] = queue.Queue()

        self._lock = threading.RLock()

        self._running = True

        self._worker = threading.Thread(

            target=self._dispatcher,

            daemon=True,

            name="FRIDAY-EventBus",

        )

        self._worker.start()

    # --------------------------------------------------

    def subscribe(

        self,

        event_type: Type[Event],

        handler: EventHandler,

    ) -> None:

        with self._lock:

            if handler not in self._subscribers[event_type]:

                self._subscribers[event_type].append(handler)

    # --------------------------------------------------

    def unsubscribe(

        self,

        event_type: Type[Event],

        handler: EventHandler,

    ) -> None:

        with self._lock:

            if handler in self._subscribers[event_type]:

                self._subscribers[event_type].remove(handler)

    # --------------------------------------------------

    def publish(

        self,

        event: Event,

    ) -> None:

        self._queue.put(event)

    # --------------------------------------------------

    def _dispatcher(self):

        while self._running:

            event = self._queue.get()

            handlers = list(

                self._subscribers.get(type(event), [])

            )

            for handler in handlers:

                try:

                    handler(event)

                except Exception as exc:

                    print(

                        f"[EventBus] {handler.__name__} failed:",

                        exc,

                    )

    # --------------------------------------------------

    def clear(self):

        with self._lock:

            self._subscribers.clear()

    # --------------------------------------------------

    def shutdown(self):

        self._running = False

        self._queue.put(Event())

        self._worker.join()


event_bus = EventBus()