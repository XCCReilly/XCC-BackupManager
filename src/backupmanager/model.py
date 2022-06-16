import typing
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import List, Optional
from enum import Enum


class SnapshotStatus(Enum):
    CREATING = 'CREATING'
    READY = 'READY'


@dataclass(order=True)
class Snapshot:
    creation_time: datetime
    name: str
    status: SnapshotStatus = SnapshotStatus.READY

    @property
    def time_since(self):
        return datetime.utcnow().replace(tzinfo=timezone.utc) - self.creation_time


@dataclass
class Disk:
    name: str
    snapshots: List[Snapshot]  # not list()

    def snapshot(self, backend):
        return backend.make_snapshot(self)

    @property
    def latest_snapshot(self) -> Optional[Snapshot]:
        if len(self.snapshots) == 0:
            return None
        return sorted(self.snapshots)[-1]


@dataclass
class AsyncOperation:
    id: str
    status: str
    errors: typing.Any


@dataclass
class VM:
    name: str
    disks: List[Disk]
    backup_enabled: bool = False
