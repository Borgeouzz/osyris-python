import os
from typing import Optional

from osyris.sync.hasher import hash_file
from osyris.sync.state import LocalState


class SyncEngine:
    def __init__(self, client: Optional[object], root_path: str):
        self._client = client
        self._root_path = os.path.abspath(root_path)
        self._state = LocalState(
            os.path.join(self._root_path, ".osyris", "state.json")
        )

    def _is_ignored(self, full_path: str) -> bool:
        if os.path.basename(full_path).startswith("."):
            return True
        # Ignore files inside .osyris (e.g. state.json) to avoid loop
        rel = self._relative(full_path)
        if rel.startswith(".osyris"):
            return True
        return False

    def initial_sync(self):
        for root, _, files in os.walk(self._root_path):
            for filename in files:
                full_path = os.path.join(root, filename)
                if self._is_ignored(full_path):
                    continue
                self._sync_file(full_path)

        self._state.save()

    def handle_file_modified(self, full_path: str):
        if self._is_ignored(full_path):
            return
        self._sync_file(full_path)
        self._state.save()
        print(f"\nFile modified: {full_path}")

    def handle_file_deleted(self, full_path: str):
        if self._is_ignored(full_path):
            return
        relative_path = self._relative(full_path)
        if self._client:
            self._client.delete_file(relative_path)
        self._state.remove_file(relative_path)
        self._state.save()
        print(f"\nFile deleted: {full_path}")

    def _sync_file(self, full_path: str):
        if not os.path.isfile(full_path):
            return

        if self._is_ignored(full_path):
            return

        relative_path = self._relative(full_path)
        new_hash = hash_file(full_path)
        old_hash = self._state.get_file_hash(relative_path)

        if new_hash == old_hash:
            return  # niente da fare

        with open(full_path, "r", encoding="utf-8") as f:
            content = f.read()

        if self._client:
            self._client.upload_file(relative_path, content)
        self._state.update_file(relative_path, new_hash)

    def _relative(self, full_path: str) -> str:
        return os.path.relpath(full_path, self._root_path)
