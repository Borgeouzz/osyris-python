# Osyris Python SDK

Official SDK for integrating Osyris into Python applications.

## Installation

```bash
pip install osyris
```

Development (from source):

```bash
pip install -e .
```

## Configuration

Set your API key:

```bash
export OSYRIS_API_KEY=your-api-key
```

Or verify login:

```bash
osyris login
osyris login your-api-key
```

## CLI

- **Sync** – watch a folder and sync files:
  ```bash
  osyris sync /path/to/folder
  ```

- **Workspace** – list workspaces or show one:
  ```bash
  osyris workspace
  osyris workspace <workspace_id>
  ```

## Usage in code

```python
from osyris import Osyris

client = Osyris()  # uses OSYRIS_API_KEY from environment

# Workspaces
for ws in client.workspaces.list():
    print(ws.id, ws.name)

# Files
client.files.upload(workspace_id="...", path="doc.txt", content="Hello")
client.files.delete(path="doc.txt")
```

## Project structure

- `osyris.client` – main client
- `osyris.config` – configuration (API key, base URL)
- `osyris.exceptions` – SDK exceptions
- `osyris.http` – HTTP client and retry
- `osyris.models` – models (Workspace, Conversation, File)
- `osyris.resources` – API resources (workspaces, conversations, files)
- `osyris.sync` – sync engine and watcher
- `osyris.cli` – CLI commands

## Requirements

- Python >= 3.9
