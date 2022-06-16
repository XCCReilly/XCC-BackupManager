import structlog
from datetime import timedelta, datetime

from backupmanager.backends import GCPBackend

logger = structlog.getLogger(__name__)


class BackupManager:
    def __init__(self, backend):
        self.backend = backend
        self.backup_interval = timedelta(seconds=1)

    def make_backups(self):
        """makes a backup if the vm has backup enabled and ...."""

        vms = self.backend.fetch_vms()
        operations = []
        for vm in vms:
            log = logger.bind(vm=vm.name)
            if not vm.backup_enabled:
                log.info("backup_disabled")
                continue

            log.info("backup_enabled")
            for disk in vm.disks:
                log = log.bind(disk=disk.name)
                if disk.latest_snapshot is None or disk.latest_snapshot.time_since > self.backup_interval:
                    log.info("backup_started")
                    operations.append(disk.snapshot(self.backend))
                else:
                    log.info("backup_too_recent")

        for done_operation in self.backend.wait_for(operations):
            duration = datetime.now() - datetime.fromisoformat(done_operation.start_time)
            logger.info(
                "backup_done",
                disk=done_operation.target_link,
                errors=done_operation.error,
                duration=duration
            )

    def retention_policy(self):
        ...


if __name__ == "__main__":
    bm = BackupManager(GCPBackend(project='asml-orchestrator-mb', zone='europe-west4-a'))

    bm.make_backups()
