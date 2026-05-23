# Prometheus Demo App

A lightweight Python Flask application instrumented with Prometheus metrics for practicing PromQL, histograms, latency monitoring, error rates, Grafana dashboards, and observability concepts.

![Python](https://img.shields.io/badge/Python-3.12-blue)
![Docker](https://img.shields.io/badge/Docker-Enabled-blue)
![Prometheus](https://img.shields.io/badge/Prometheus-Metrics-orange)

---

## Dashboard Preview

> Custom-built Grafana dashboard created specifically for practicing PromQL, histogram metrics, error rate monitoring, and latency analysis.

![Grafana Dashboard](./screenshots/Grafana.jpg)

---

## Architecture

```text
Client Traffic
      ↓
Flask Demo App
      ↓
/metrics
      ↓
Prometheus
      ↓
Grafana Dashboards
```

---

## Purpose

This project was built as a practice application for a local Prometheus monitoring lab.

It provides custom application metrics that can be used to practice:

- PromQL queries
- rate and aggregation
- HTTP error rate calculation
- histogram buckets
- p95 latency monitoring
- Grafana dashboard creation
- alerting scenarios

The monitoring stack itself is maintained in a separate repository:

```text
https://github.com/DVanyan/monitoring-lab
```

---

## Features

- Prometheus `/metrics` endpoint
- HTTP request counters
- Active users gauge
- Request latency histogram
- Randomized HTTP status codes for realistic monitoring practice
- Dockerized deployment
- Designed to integrate with a separate Prometheus monitoring stack

---

## Tech Stack

- Python
- Flask
- prometheus_client
- Docker
- Docker Compose
- Prometheus

---

## Application Endpoints

| Endpoint | Description |
|---|---|
| `/` | Demo endpoint with random `200` and `500` responses |
| `/api` | Demo API endpoint with random `200`, `404`, and `500` responses |
| `/metrics` | Prometheus metrics endpoint |

---

## Exposed Metrics

### Counter: `demo_http_requests_total`

Tracks total HTTP requests grouped by `method`, `endpoint`, and `status`.

Example:

```text
demo_http_requests_total{endpoint="/api", method="GET", status="500"}
```

---

### Gauge: `demo_active_users`

Simulates current active users count.

---

### Histogram: `demo_http_request_duration_seconds`

Tracks request latency by endpoint.

Configured buckets:

```text
0.05, 0.1, 0.2, 0.3, 0.5, 1, 2, 5
```

---

## Project Structure

```text
prometheus-demo-app/
├── app.py
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── README.md
├── .gitignore
└── screenshots/
```

---

## How to Run

### Clone repository

```bash
git clone https://github.com/DVanyan/prometheus-demo-app.git
cd prometheus-demo-app
```

### Make sure monitoring-lab is running

This demo application is designed to work together with the monitoring stack from:

```text
https://github.com/DVanyan/monitoring-lab
```

Start the monitoring stack first from the `monitoring-lab` repository:

```bash
cd ../monitoring-lab
docker compose up -d
```

### Verify Docker network

The demo application connects to the Docker network created by `monitoring-lab`.

Expected network name:

```text
monitoring-lab_default
```

Check existing Docker networks:

```bash
docker network ls
```

If your network name is different, update it in `docker-compose.yml`:

```yaml
networks:
  monitoring:
    external: true
    name: monitoring-lab_default
```

### Start demo application

Return to the demo application repository:

```bash
cd ../prometheus-demo-app
docker compose up -d --build
```

### Add Prometheus scrape target

In the `monitoring-lab` repository, add the following scrape job to the Prometheus configuration:

```yaml
- job_name: "demo-app"
  static_configs:
    - targets: ["prometheus-demo-app:8000"]
```

Then restart Prometheus:

```bash
cd ../monitoring-lab
docker compose restart prometheus
```

### Open services

Demo App:

```text
http://localhost:8000
```

Metrics endpoint:

```text
http://localhost:8000/metrics
```

Prometheus:

```text
http://localhost:9090
```

Grafana:

```text
http://localhost:3000
```

---

## Docker Compose

This application connects to the external Docker network created by the monitoring stack.

```yaml
services:
  demo-app:
    build: .
    container_name: prometheus-demo-app
    ports:
      - "8000:8000"
    networks:
      - monitoring

networks:
  monitoring:
    external: true
    name: monitoring-lab_default
```

---

## Generate Test Traffic

### Basic traffic

```bash
timeout 300 bash -c 'while true; do curl -s localhost:8000 > /dev/null; sleep 0.1; done'
```

### API traffic

```bash
timeout 300 bash -c 'while true; do curl -s localhost:8000/api > /dev/null; sleep 0.1; done'
```

---

## Example Metrics

```text
demo_http_requests_total{endpoint="/api",status="500"} 125
demo_active_users 47
demo_http_request_duration_seconds_bucket{le="0.5"} 312
```

---

## PromQL Examples

### Requests per second

```promql
rate(demo_http_requests_total[1m])
```

### Requests per second grouped by status

```promql
sum by(status) (
  rate(demo_http_requests_total[1m])
)
```

### API requests per second grouped by status

```promql
sum by(status) (
  rate(demo_http_requests_total{endpoint="/api"}[1m])
)
```

### API error percentage

```promql
sum(rate(demo_http_requests_total{endpoint="/api", status=~"404|500"}[5m]))
/
sum(rate(demo_http_requests_total{endpoint="/api"}[5m]))
* 100
```

### p95 request latency

```promql
histogram_quantile(
  0.95,
  sum by(le, endpoint) (
    rate(demo_http_request_duration_seconds_bucket[5m])
  )
)
```

---

## Learning Goals

This project is designed for practicing:

- Prometheus fundamentals
- PromQL
- Counters, Gauges, and Histograms
- Labels and aggregation
- Error rate monitoring
- Request latency analysis
- Histogram quantiles
- Grafana dashboards
- Observability concepts
- Alerting fundamentals

---

## Skills Demonstrated

- Prometheus instrumentation
- PromQL
- Histogram metrics
- Error rate monitoring
- Request latency monitoring
- Docker networking
- Flask application monitoring
- Metrics aggregation
- Grafana visualization
- Observability fundamentals

---

## Related Repository

Monitoring stack repository:

```text
https://github.com/DVanyan/monitoring-lab
```

Includes:

- Prometheus
- Grafana
- Node Exporter
- cAdvisor
- Blackbox Exporter
- Alertmanager

## How to Use with monitoring-lab

This application is designed to work together with the monitoring stack from:

```text

https://github.com/DVanyan/monitoring-lab

```

1. Start the monitoring stack from the `monitoring-lab` repository.

2. Start this demo application.

3. Add the demo-app scrape configuration to Prometheus.

4. Open Grafana dashboards and begin generating traffic.

---

## Author

**David Vanyan**

LFCS Certified Linux Administrator

- GitHub: https://github.com/DVanyan

- LinkedIn: www.linkedin.com/in/davidvanyan

[![LFCS](https://images.credly.com/size/220x220/images/1e6611ca-8afe-4ecc-ad4d-305fba52ee7e/1_LFCS-600x600.png)](https://www.credly.com/badges/eb28bbcb-1a81-4e01-98bf-b6d1e6c674be/public_url)
