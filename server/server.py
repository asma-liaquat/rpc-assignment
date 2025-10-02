from flask import Flask, jsonify, request


app = Flask(__name__)

@app.route('/add', methods=['POST'])
def add():
    data = request.get_json()
    x = data.get('x')
    y = data.get('y')
    result = x + y
    return jsonify({'result': result})

@app.route('/multiply', methods=['POST'])
def multiply():
    data = request.get_json()
    x = data.get('x')
    y = data.get('y')
    result = x * y
    return jsonify({'result': result})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)