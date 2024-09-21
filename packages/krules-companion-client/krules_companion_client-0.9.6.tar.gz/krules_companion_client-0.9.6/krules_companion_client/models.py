from datetime import datetime
from enum import Enum
from pydantic import BaseModel, root_validator

from types import NoneType
from typing import Generic, TypeVar, Sequence

T = TypeVar("T")


class EventType(str, Enum):
    EntityCreated = "io.krules.streams.entity.v1.created"
    EntityUpdated = "io.krules.streams.entity.v1.updated"
    EntityDeleted = "io.krules.streams.entity.v1.deleted"
    EntityCallback = "io.krules.streams.entity.v1.callback"

class BaseUpdateEvent(BaseModel):

    @root_validator(pre=True)
    def assign_id_to_state(cls, values):
        state = values.get('state')
        if isinstance(state, dict) and 'id' not in state:
            state['id'] = values['id']

        old_state = values.get('old_state')
        if isinstance(old_state, dict) and 'id' not in old_state:
            old_state['id'] = values['id']

        return values

class EntityUpdatedEvent(BaseUpdateEvent, Generic[T]):
    id: str
    group: str
    subscription: int
    changed_properties: Sequence[str]
    state: T
    old_state: T | None = None


class EntityCreatedEvent(BaseUpdateEvent, Generic[T]):
    id: str
    group: str
    subscription: int
    changed_properties: Sequence[str]
    state: T
    old_state: NoneType


class EntityDeletedEvent(BaseUpdateEvent, Generic[T]):
    id: str
    group: str
    subscription: int
    changed_properties: Sequence[str]
    state: NoneType
    old_state: T


class EntityCallbackEvent(BaseUpdateEvent, Generic[T]):
    last_updated: datetime
    task_id: str
    id: str
    group: str
    subscription: int
    state: T
    message: str
