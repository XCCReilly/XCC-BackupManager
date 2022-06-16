from datetime import datetime, timedelta, timezone

from backupmanager.model import Snapshot, Disk, VM


def test_time_since_snapshot():
    s = Snapshot(name='s1', creation_time=datetime.now().replace(tzinfo=timezone.utc) - timedelta(hours=5))
    # assert timedelta(minutes=299) < s.time_since < timedelta(minutes=301)


def test_sort_order_snapshots():
    assert Snapshot(name="snapshot1", creation_time=datetime(2022, 6, 1).replace(tzinfo=timezone.utc)) < Snapshot(
        name="a-snapshot", creation_time=datetime(2022, 6, 2).replace(tzinfo=timezone.utc)
    )


def test_disks_have_snapshots():
    disk = Disk(name="disk-1", snapshots=[Snapshot(name="snapshot1", creation_time=datetime(2022, 6, 1))])

    assert len(disk.snapshots) == 1


def test_vms_have_disks():
    vm = VM(
        name="VM-1",
        disks=[
            Disk(name="disk-1", snapshots=[
                Snapshot(name="snapshot1", creation_time=datetime(2022, 6, 1))
            ])
        ],
    )
    assert len(vm.disks) == 1


def test_vms_default_no_backup_enabled():
    vm = VM(name="non-backup-instance", disks=[])
    assert not vm.backup_enabled
