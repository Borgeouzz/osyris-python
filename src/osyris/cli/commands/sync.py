"""Sync command: watch and sync a folder."""

import argparse
import os
import sys

from osyris.cli.utils import get_optional_client
from osyris.sync.engine import SyncEngine
from osyris.sync.watcher import Watcher


def sync_cmd(args: argparse.Namespace) -> int:
    """Run sync watch for the given path."""
    path = os.path.abspath(args.path)
    if not os.path.isdir(path):
        print(f"Not a directory: {path}", file=sys.stderr)
        return 1

    client = get_optional_client()
    if not client:
        print("OSYRIS_API_KEY is not set. Sync will run in local-only mode.", file=sys.stderr)

    engine = SyncEngine(client, path)
    engine.initial_sync()

    watcher = Watcher(engine, path)
    watcher.start()

    print("Watching for changes... (Ctrl+C to stop)")
    try:
        watcher.join()
    except KeyboardInterrupt:
        pass
    return 0
