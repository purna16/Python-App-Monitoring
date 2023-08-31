from flask import Flask, jsonify, request
import time
import random
from prometheus_flask_exporter import PrometheusMetrics

app = Flask(__name__)
metrics = PrometheusMetrics(app)

@app.route('/api/v1/hello', methods=['GET'])
def hello():
    time.sleep(random.uniform(0.1, 1))  # Simulate random delay
    if random.random() < 0.1:  # Simulate 10% failure rate
        return "Internal Server Error", 500
    return jsonify({"message": "hello-world"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
