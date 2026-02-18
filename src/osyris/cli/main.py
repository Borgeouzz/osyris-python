"""Osyris CLI entrypoint."""

import argparse
import sys

from osyris.cli.commands import sync_cmd, login_cmd, workspace_cmd


def main() -> int:
    parser = argparse.ArgumentParser(prog="osyris", description="Osyris SDK CLI")
    subparsers = parser.add_subparsers(dest="command", required=True, help="Command")

    # osyris sync <path>
    sync_parser = subparsers.add_parser("sync", help="Watch and sync a folder")
    sync_parser.add_argument("path", help="Directory path to watch")
    sync_parser.set_defaults(handler=sync_cmd)

    # osyris login [key]
    login_parser = subparsers.add_parser("login", help="Set or verify API key")
    login_parser.add_argument("key", nargs="?", help="API key (optional, to verify use env OSYRIS_API_KEY)")
    login_parser.set_defaults(handler=login_cmd)

    # osyris workspace [id]
    ws_parser = subparsers.add_parser("workspace", help="List workspaces or show one")
    ws_parser.add_argument("workspace_id", nargs="?", help="Workspace ID (optional)")
    ws_parser.set_defaults(handler=workspace_cmd)

    args = parser.parse_args()
    return args.handler(args)


if __name__ == "__main__":
    sys.exit(main())
