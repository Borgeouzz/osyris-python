import json
import os
from typing import Dict, Optional


class LocalState:
    def __init__(self, state_path: str):
        self._state_path = state_path
        self._data = {"files": {}}
        self._load()

    def _load(self):
        if os.path.exists(self._state_path):
            with open(self._state_path, "r") as f:
                self._data = json.load(f)
        if "files" not in self._data:
            self._data["files"] = {}

    def save(self):
        os.makedirs(os.path.dirname(self._state_path), exist_ok=True)
        with open(self._state_path, "w") as f:
            json.dump(self._data, f, indent=2)

    def get_file_hash(self, relative_path: str) -> Optional[str]:
        entry = self._data["files"].get(relative_path)
        return entry["hash"] if entry else None

    def update_file(self, relative_path: str, file_hash: str):
        self._data["files"][relative_path] = {
            "hash": file_hash
        }

    def remove_file(self, relative_path: str):
        self._data["files"].pop(relative_path, None)
