# Vector Clocks RPC Assignment - Short Report

## Implementation

We implemented a small VectorClock class (in `server/vector_clock.py` and `client/vector_clock.py`) which stores a mapping of node id to integer counter. It supports:

- `increment(node_id)` — increments the counter for the given node.
- `update(other_clock)` — merges another clock by taking element-wise maxima.
- `compare(other_clock)` — compares two clocks and returns one of: `happens-before`, `happens-after`, `concurrent`, `equal`.

The server (`server/server.py`) maintains a local vector clock with node id `server`. For each request it:

1. Increments its own clock.
2. Merges the client's clock (if provided).
3. Returns the updated clock in the response JSON under `vc`.

Clients maintain their own vector clocks (examples in `client/client.py`). Before sending a request, a client increments its own clock and includes it in the request as the `vc` field. After receiving a response, the client merges the server's clock.

## Example execution logs

Run the server and then `python client/client.py` to see a short demo. The demo prints client clocks before/after operations and the relation between two clients (A and B). Example output will show both `happens-before` and `concurrent` cases depending on timing.

Example output from `python test_vector_clock.py` used during development:

```
a: {'A': 1}
b: {'B': 1}
a vs b: concurrent
a after merge b: {'A': 1, 'B': 1}
a vs b after merge: happens-after

a2: {'A': 1}
b2: {'A': 1, 'B': 1}
a2 vs b2: happens-before
```

## Handling concurrent updates

Vector clocks allow clients and the server to detect when events are concurrent (neither happened-before the other). The merge strategy on update (element-wise maxima) ensures causally later clocks dominate earlier ones while preserving concurrency information.
