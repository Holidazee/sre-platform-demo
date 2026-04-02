import logging
import time
from flask import Flask, Response
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST

app = Flask(__name__)

logging.basicConfig(level=logging.INFO)

REQUEST_COUNT = Counter(
    "app_requests_total",
    "Total number of requests",
    ["method", "endpoint", "http_status"]
)

REQUEST_LATENCY = Histogram(
    "app_request_latency_seconds",
    "Request latency in seconds",
    ["endpoint"]
)

def track_metrics(endpoint_name, status_code, start_time, method="GET"):
    REQUEST_COUNT.labels(method=method, endpoint=endpoint_name, http_status=status_code).inc()
    REQUEST_LATENCY.labels(endpoint=endpoint_name).observe(time.time() - start_time)

@app.route("/")
def home():
    start_time = time.time()
    app.logger.info("Home endpoint hit")
    response = {
        "status": "ok",
        "service": "sre-platform-demo"
    }
    track_metrics("/", "200", start_time)
    return response

@app.route("/health")
def health():
    start_time = time.time()
    app.logger.info("Health check hit")
    response = {"status": "healthy"}
    track_metrics("/health", "200", start_time)
    return response

@app.route("/error")
def error():
    start_time = time.time()
    app.logger.error("Simulated failure")
    response = {"status": "error"}
    track_metrics("/error", "500", start_time)
    return response, 500

@app.route("/metrics")
def metrics():
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)