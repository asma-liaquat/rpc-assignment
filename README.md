# RPC assignment - Vector Clocks

This project implements a small RPC server and clients that exchange vector clock metadata to track causal relationships.

Files of interest:
- `server/server.py` - Flask server that maintains a vector clock and returns it in responses.
- `server/vector_clock.py` - VectorClock implementation used by the server.
- `client/client.py` - Example client that maintains its own vector clock and demonstrates interactions.
- `client/vector_clock.py` - VectorClock implementation for the client.
- `server/Dockerfile` - Dockerfile to run the server.

Running locally

1. Create a virtualenv and install requirements:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2. Start the server:

```bash
python server/server.py
```

3. In another terminal run the demo client:

```bash
python client/client.py
```

Running with Docker

```bash
cd server
docker build -t rpc-server .
docker run -p 8080:8080 rpc-server
```

The demo client assumes the server is reachable at `http://127.0.0.1:8080`.
