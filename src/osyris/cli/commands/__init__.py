"""CLI commands."""

from osyris.cli.commands.sync import sync_cmd
from osyris.cli.commands.login import login_cmd
from osyris.cli.commands.workspace import workspace_cmd

__all__ = ["sync_cmd", "login_cmd", "workspace_cmd"]
