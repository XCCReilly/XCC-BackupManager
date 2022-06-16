from fastapi import FastAPI

from backupmanager.backends import GCPBackend
from backupmanager.backup import BackupManager

app = FastAPI()


@app.post("/backups/{project}/{zone}")
def create_backup(project: str, zone: str):
    bm = BackupManager(GCPBackend(project=project, zone=zone))
    bm.make_backups()
    