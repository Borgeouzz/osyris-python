"""Login command: set or verify API key."""

import argparse
import os
import sys

from osyris.client import Osyris
from osyris.exceptions import AuthenticationError, APIError


def login_cmd(args: argparse.Namespace) -> int:
    """Set OSYRIS_API_KEY or verify current key."""
    if args.key:
        # Suggest setting env var (we don't persist to disk by default)
        print("To use this API key, set it in your environment:")
        print(f"  export OSYRIS_API_KEY={args.key}")
        print("Or add it to your shell profile (.bashrc, .zshrc, etc.).")
        # Verify the key works
        try:
            Osyris(api_key=args.key)
            print("Key format is valid.")
        except (AuthenticationError, APIError) as e:
            print(f"Warning: {e}", file=sys.stderr)
        return 0

    # No key provided: check env
    key = os.getenv("OSYRIS_API_KEY")
    if not key:
        print("OSYRIS_API_KEY is not set.", file=sys.stderr)
        print("Run: osyris login <your-api-key>", file=sys.stderr)
        return 1
    try:
        client = Osyris(api_key=key)
        # Light call to verify (e.g. list workspaces)
        client.workspaces.list()
        print("Logged in successfully.")
    except APIError as e:
        print(f"Login failed: {e}", file=sys.stderr)
        return 1
    except AuthenticationError as e:
        print(str(e), file=sys.stderr)
        return 1
    return 0
