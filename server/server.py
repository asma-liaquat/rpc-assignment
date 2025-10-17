from flask import Flask, jsonify, request
from vector_clock import VectorClock


app = Flask(__name__)

# Server has its own node id in the vector clock
SERVER_NODE_ID = 'server'
server_vc = VectorClock()


def _extract_client_vc(data):
    vc = data.get('vc') if isinstance(data, dict) else None
    if vc is None:
        return None
    return VectorClock.from_dict(vc)


@app.route('/add', methods=['POST'])
def add():
    data = request.get_json() or {}
    client_vc = _extract_client_vc(data)

    # Server updates its local vector clock
    server_vc.increment(SERVER_NODE_ID)
    # Merge client's vector clock (if any)
    if client_vc:
        server_vc.update(client_vc)

    x = data.get('x', 0)
    y = data.get('y', 0)
    result = x + y

    return jsonify({'result': result, 'vc': server_vc.to_dict()})


@app.route('/multiply', methods=['POST'])
def multiply():
    data = request.get_json() or {}
    client_vc = _extract_client_vc(data)

    server_vc.increment(SERVER_NODE_ID)
    if client_vc:
        server_vc.update(client_vc)

    x = data.get('x', 0)
    y = data.get('y', 0)
    result = x * y

    return jsonify({'result': result, 'vc': server_vc.to_dict()})


@app.route('/vc', methods=['GET'])
def get_vc():
    # Return current server vector clock
    return jsonify({'vc': server_vc.to_dict()})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)