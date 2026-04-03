from time import time

from flask import Flask, Response
from prometheus_client import CONTENT_TYPE_LATEST, Counter, Histogram, generate_latest


app = Flask(__name__)

REQUEST_COUNT = Counter("app_requests_total", "Total app requests")
ERROR_COUNT = Counter("app_errors_total", "Total app errors")
REQUEST_LATENCY = Histogram("app_request_latency_seconds", "Request latency in seconds")


@app.before_request
def before_request():
    app.start_time = time()


@app.after_request
def after_request(response):
    latency = time() - app.start_time
    REQUEST_LATENCY.observe(latency)

    if response.status_code >= 400:
        ERROR_COUNT.inc()

    return response


@app.route("/")
def home():
    REQUEST_COUNT.inc()
    return "SRE demo project is running!"


@app.route("/health")
def health():
    REQUEST_COUNT.inc()
    return {"status": "healthy"}, 200


@app.route("/error")
def error():
    REQUEST_COUNT.inc()
    ERROR_COUNT.inc()
    return {"status": "error", "message": "Simulated failure"}, 500


@app.route("/metrics")
def metrics():
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
