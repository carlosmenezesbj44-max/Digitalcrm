from typing import Callable, Dict, List
from crm_core.events.events import Event


class EventBus:
    def __init__(self):
        self._handlers: Dict[str, List[Callable]] = {}

    def subscribe(self, event_type: str, handler: Callable):
        if event_type not in self._handlers:
            self._handlers[event_type] = []
        self._handlers[event_type].append(handler)

    def publish(self, event: Event):
        event_type = type(event).__name__
        if event_type in self._handlers:
            for handler in self._handlers[event_type]:
                handler(event)
