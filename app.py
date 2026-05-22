from flask import Flask, Response
from prometheus_client import Counter, Gauge, Histogram, generate_latest
import random
import time

app = Flask(__name__)

REQUESTS = Counter(
    "demo_http_requests_total",
    "Total HTTP requests",
    ["method", "endpoint", "status"]
)

ACTIVE_USERS = Gauge(
    "demo_active_users",
    "Current active users"
)

LATENCY = Histogram(
    "demo_http_request_duration_seconds",
    "HTTP request latency in seconds",
    ["endpoint"],
    buckets=[0.05, 0.1, 0.2, 0.3, 0.5, 1, 2, 5]
)

@app.route("/")
def index():
    start = time.time()
    endpoint = "/"
    status = random.choice(["200", "200", "200", "500"])

    time.sleep(random.uniform(0.01, 0.4))

    REQUESTS.labels("GET", endpoint, status).inc()
    ACTIVE_USERS.set(random.randint(1, 100))
    LATENCY.labels(endpoint).observe(time.time() - start)

    return "Demo app is running\n", int(status)

@app.route("/api")
def api():
    start = time.time()
    endpoint = "/api"
    status = random.choice(["200", "200", "404", "500"])

    time.sleep(random.uniform(0.05, 1.2))

    REQUESTS.labels("GET", endpoint, status).inc()
    ACTIVE_USERS.set(random.randint(1, 100))
    LATENCY.labels(endpoint).observe(time.time() - start)

    return "API response\n", int(status)

@app.route("/metrics")
def metrics():
    return Response(generate_latest(), mimetype="text/plain")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
