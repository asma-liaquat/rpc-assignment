import requests
import time
from vector_clock import VectorClock

SERVER_URL = "http://127.0.0.1:8080"


class RPCClient:
    def __init__(self, node_id):
        self.node_id = node_id
        self.vc = VectorClock()

    def _post(self, path, payload):
        # increment before sending
        self.vc.increment(self.node_id)
        payload = dict(payload)
        payload['vc'] = self.vc.to_dict()
        resp = requests.post(f"{SERVER_URL}{path}", json=payload)
        data = resp.json()
        server_vc = data.get('vc')
        if server_vc:
            self.vc.update(server_vc)
        return data

    def add(self, x, y):
        return self._post('/add', {'x': x, 'y': y})

    def multiply(self, x, y):
        return self._post('/multiply', {'x': x, 'y': y})


def demo_sequence():
    a = RPCClient('A')
    b = RPCClient('B')

    print('Client A initial VC:', a.vc.to_dict())
    print('Client B initial VC:', b.vc.to_dict())

    # A does an add
    r1 = a.add(1, 2)
    print('A after add:', a.vc.to_dict(), 'server returned', r1.get('vc'))

    # B does a multiply (concurrent if B didn't see A)
    r2 = b.multiply(2, 3)
    print('B after multiply:', b.vc.to_dict(), 'server returned', r2.get('vc'))

    # Now A does another op and should merge server vc
    r3 = a.multiply(3, 4)
    print('A after second op:', a.vc.to_dict(), 'server returned', r3.get('vc'))

    # Show relation between A and B clocks
    comp = a.vc.compare(b.vc)
    print('Relation between A and B:', comp)


if __name__ == '__main__':
    # Wait a bit in case server is being started in parallel
    time.sleep(0.2)
    demo_sequence()