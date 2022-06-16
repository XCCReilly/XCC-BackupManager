
from backupmanager.backup import BackupManager
from backupmanager.model import VM, Disk, Snapshot, AsyncOperation
from backupmanager import backends
from unittest.mock import Mock


def test_no_backup_made_non_backup_enabled_vms():
    mockBackend = Mock()
    mockBackend.fetch_vms.return_value = [
        VM(
            name="non-backup-instance",
            backup_enabled=False,
            disks=[Disk(name="disk-1", snapshots=[])]
    )]
    mockBackend.make_snapshot.return_value = (
        AsyncOperation(id="mock", status="mock", errors=[])
    )
    def wait_for(ops):
        for op in ops:
            yield op

    mockBackend.wait_for = wait_for


    backup = BackupManager(mockBackend)
    backup.make_backups()

    mockBackend.fetch_vms.assert_called_with()
    mockBackend.make_snapshot.assert_not_called()
