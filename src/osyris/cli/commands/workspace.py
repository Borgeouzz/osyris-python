"""Workspace command: list or show workspaces."""

import argparse
import sys

from osyris.cli.utils import get_client


def workspace_cmd(args: argparse.Namespace) -> int:
    """List workspaces or show one by ID."""
    client = get_client()
    if args.workspace_id:
        try:
            ws = client.workspaces.get(args.workspace_id)
            print(f"ID:   {ws.id}")
            print(f"Name: {ws.name}")
        except Exception as e:
            print(f"Error: {e}", file=sys.stderr)
            return 1
    else:
        try:
            workspaces = client.workspaces.list()
            if not workspaces:
                print("No workspaces found.")
                return 0
            for ws in workspaces:
                print(f"{ws.id}\t{ws.name}")
        except Exception as e:
            print(f"Error: {e}", file=sys.stderr)
            return 1
    return 0
