from typing import Any, Dict
import sys
import structlog
import typer

from backupmanager.backends import GCPBackend
from backupmanager.backup import BackupManager

app = typer.Typer(name="backup-manager", help="Manages backups and retentions on GCP")


@app.command()
def list(project: str, zone: str):
    ...


def check_gcp_project_exists(project):
    if project not in ["asml-orchestrator-mb"]:
        print("no such project, expected one of ...")
        raise typer.Exit(code=1)
    return project


@app.command()
def create_backups(
    project: str = typer.Argument(
        ...,
        help="the project to look for instances in",
        callback=check_gcp_project_exists,
    ),
    zone: str = typer.Argument("europe-west4-a", help="the zone to look for instances in"),
):
    """
    Creates a snapshot for all snapshot enabled VMS on GCP in the specified project and zone
    """
    bm = BackupManager(GCPBackend(project=project, zone=zone))

    bm.make_backups()


def render_to_log_kwargs(
    logger, name: str, event_dict: Any
) -> Dict[str, Any]:
    print(structlog.dev.ConsoleRenderer()(logger, name, event_dict.copy()), file=sys.stderr)
    return {"msg": {"event": event_dict.pop("event"), **event_dict}}


def main():
    # import google.cloud.logging
    # logging_client = google.cloud.logging.Client()
    # logging_client.setup_logging()
    #
    # structlog.configure(
    #     processors=[
    #         structlog.stdlib.filter_by_level,
    #         structlog.stdlib.add_logger_name,
    #         structlog.stdlib.add_log_level,
    #         structlog.stdlib.PositionalArgumentsFormatter(),
    #         structlog.processors.StackInfoRenderer(),
    #         structlog.processors.format_exc_info,
    #         structlog.processors.UnicodeDecoder(),
    #         render_to_log_kwargs
    #     ],
    #     logger_factory=structlog.stdlib.LoggerFactory(),
    #     wrapper_class=structlog.stdlib.BoundLogger,
    #     cache_logger_on_first_use=True,
    # )

    app()


if __name__ == "__main__":
    main()
