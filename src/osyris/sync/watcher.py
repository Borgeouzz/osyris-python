from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


class _Handler(FileSystemEventHandler):
    def __init__(self, engine):
        self._engine = engine

    def on_modified(self, event):
        if not event.is_directory:
            self._engine.handle_file_modified(event.src_path)

    def on_deleted(self, event):
        if not event.is_directory:
            self._engine.handle_file_deleted(event.src_path)


class Watcher:
    def __init__(self, engine, path: str):
        self._engine = engine
        self._path = path
        self._observer = Observer()

    def start(self):
        handler = _Handler(self._engine)
        self._observer.schedule(handler, self._path, recursive=True)
        self._observer.start()

    def join(self):
        self._observer.join()
