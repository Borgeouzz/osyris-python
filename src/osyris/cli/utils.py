"""CLI utilities."""

import os
import sys
from typing import Optional

from osyris.client import Osyris
from osyris.exceptions import AuthenticationError


def get_client(api_key: Optional[str] = None) -> Osyris:
    """Build an Osyris client, using env OSYRIS_API_KEY if api_key is not given."""
    key = api_key or os.getenv("OSYRIS_API_KEY")
    if not key:
        print("OSYRIS_API_KEY is not set. Run 'osyris login' or set the environment variable.", file=sys.stderr)
        sys.exit(1)
    try:
        return Osyris(api_key=key)
    except AuthenticationError as e:
        print(str(e), file=sys.stderr)
        sys.exit(1)


def get_optional_client(api_key: Optional[str] = None) -> Optional[Osyris]:
    """Build an Osyris client if API key is available, else return None."""
    key = api_key or os.getenv("OSYRIS_API_KEY")
    if not key:
        return None
    try:
        return Osyris(api_key=key)
    except AuthenticationError:
        return None
