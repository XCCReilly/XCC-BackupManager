import typing
from datetime import datetime
from typing import List

import structlog

from backupmanager.model import VM, Disk, Snapshot, AsyncOperation

try:
    from google.cloud.compute_v1 import InstancesClient, SnapshotsClient, DisksClient, ZoneOperationsClient
    from google.cloud.compute_v1 import Snapshot as GCPSnapshot
except ImportError as e:
    print("did you forget to install with [gcp] optional dependenies")
    raise e


logger = structlog.getLogger(__name__)


class Backend(typing.Protocol):
    def fetch_vms(self) -> List[VM]:
        ...

    def make_snapshot(self, disk: Disk) -> Snapshot:
        ...

    def delete_snapshot(self, snapshot: Snapshot) -> None:
        ...


# Facade class
class GCPBackend:
    def __init__(self, project, zone):
        self.snapshots_client = SnapshotsClient()
        self.instances_client = InstancesClient()
        self.disks_client = DisksClient()
        self.zone_operations_client = ZoneOperationsClient()
        self.project = project
        self.zone = zone

    def fetch_vms(self) -> List[VM]:
        instances = self.instances_client.list(project=self.project, zone=self.zone)
        snapshots = self.snapshots_client.list(project=self.project)
        result = []
        for instance in instances:
            result.append(VM(
                name=instance.name,
                backup_enabled=instance.labels.get("backup", "false") == "true",
                disks=[Disk(
                    name=disk.source.split("/")[-1],
                    snapshots=[Snapshot(
                        creation_time=datetime.fromisoformat(snapshot.creation_timestamp),
                        name=snapshot.name,
                        ) for snapshot in snapshots
                        if snapshot.source_disk == disk.source
                    ],
                ) for disk in instance.disks
                ],
            ))

        return result

    def make_snapshot(self, disk: Disk) -> AsyncOperation:
        op = self.disks_client.create_snapshot(
            project=self.project,
            zone=self.zone,
            disk=disk.name,
            snapshot_resource=GCPSnapshot(name=f"{disk.name}-{datetime.now().strftime('%Y%m%d%H%M%S')}".lower()),
        )
        return AsyncOperation(id=op.name, status=op.status, errors=op.error)

    def wait_for(self, operations: List[AsyncOperation]) -> typing.Generator[AsyncOperation, None, None]:
        while True:
            for operation in operations:
                op_result = self.zone_operations_client.get(
                    project=self.project, zone=self.zone, operation=operation.id
                )
                if op_result.status != 121282975:  # not running
                    yield AsyncOperation(
                        id=op_result.name,
                        status="READY",
                        errors=op_result.error,
                    )
                    operations.remove(operation)

            if len(operations) == 0:
                break

    def delete_snapshot(self, snapshot: Snapshot) -> None:
        ...
