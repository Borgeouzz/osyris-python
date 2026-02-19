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

### Sync client

```python
from osyris import Osyris

client = Osyris()  # uses OSYRIS_API_KEY from environment

# Optional: timeout and retries
client = Osyris(timeout=60.0, max_retries=5)

# Workspaces
for ws in client.workspaces.list():
    print(ws.id, ws.name)

# Files
client.files.upload(workspace_id="...", path="doc.txt", content="Hello")
client.files.delete(path="doc.txt")
```

### Async client

For async applications (e.g. FastAPI, asyncio), use `AsyncOsyris` and `await` all API calls. Prefer the async context manager so the HTTP client is closed properly:

```python
import asyncio
from osyris import AsyncOsyris

async def main():
    async with AsyncOsyris() as client:
        workspaces = await client.workspaces.list()
        for ws in workspaces:
            print(ws.id, ws.name)
        await client.files.upload(workspace_id="...", path="doc.txt", content="Hello")

asyncio.run(main())
```

## Project structure

- `osyris.client` – main client
- `osyris.config` – configuration (API key, base URL)
- `osyris.exceptions` – SDK exceptions
- `osyris.http` – sync/async HTTP client (httpx) and retry
- `osyris.models` – models (Workspace, Conversation, File)
- `osyris.resources` – API resources (workspaces, conversations, files)
- `osyris.sync` – sync engine and watcher
- `osyris.cli` – CLI commands

## Requirements

- Python >= 3.9
