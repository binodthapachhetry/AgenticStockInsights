# Market Intelligence Platform

![Python CI](https://github.com/<owner>/<repo>/actions/workflows/python-ci.yml/badge.svg)
![Docker Build](https://github.com/<owner>/<repo>/actions/workflows/docker-publish.yml/badge.svg)
![License: Apache-2.0](https://img.shields.io/github/license/<owner>/<repo>)

## Table of Contents
- [Overview](#overview)
- [Architecture](#architecture)
- [Quick Start](#quick-start)
- [Running the Test Suite](#running-the-test-suite)
- [Deployment Guide](#deployment-guide)
- [Observability](#observability)
- [Roadmap](#roadmap)
- [Contributing](#contributing)
- [License](#license)

## Overview
AgenticStockInsights is a multi-service, AI-powered market-intelligence stack.  
Python (FastAPI) micro-services ingest raw market data, enrich it with NLP
(summarisation, sentiment, semantic search, Q&A) and publish insights through a
single Orchestrator API.  
A React + TypeScript front-end (Firebase Auth & Hosting) visualises price
movements, sentiment heat-maps and analytics dashboards.  
Underlying plumbing includes Kafka / GCP PubSub, Prometheus metrics, Docker /
Kubernetes and CI/CD GitHub Actions.

## Architecture
Detailed sequence diagram lives in [ARCHITECTURE.md](./ARCHITECTURE.md).

• data_ingestor_agent – pulls SEC EDGAR filings & yfinance prices, publishes to  
  Kafka, exposes health & Prometheus metrics (circuit-breaker + retries).  
• analytics_agent – correlates stock prices with sentiment scores.  
• summarization_agent – distils long filings/news into concise bullet points.  
• sentiment_agent – FinBERT-based tone classification (positive/negative/neutral).  
• semantic_search_agent – vector indexes documents for similarity search.  
• qa_agent – answers factoid questions over indexed data.  
• orchestrator_agent – gateway that chains agents into full workflows.  
• React Web (./web) – dashboard UI, authenticated via Firebase.

## Quick Start
### Prerequisites
- Docker >= 20.10 (or Podman)
- Docker Compose v2
- Node >= 18
- Python >= 3.10

### One-liner
```bash
git clone <repo>; cd <repo>; docker compose up --build
```

### Manual dev workflow
1. `pip install -r requirements/requirements.txt`
2. `cd web && npm i && npm start`
3. Browse `http://localhost:5173` (web) and any service at `/docs` for Swagger.

## Running the Test Suite
```bash
pytest agents/data_ingestor_agent -q
```
A subset of high-value tests (~90 % pass rate) also runs in CI (see badge).

## Deployment Guide
- `docker compose -f docker-compose.yml up -d` for local/CI.
- `kustomize build k8s-manifests | kubectl apply -f -` for Kubernetes / GKE.
- Firebase Hosting auto-deploys the web app via the GitHub workflow
  `.github/workflows/firebase-hosting-*.yml`.

## Observability
- Each agent exports Prometheus metrics at `/metrics`.
- Example counters: `data_ingestor_requests_total`, `data_ingestor_circuit_state`.
- Pre-built Grafana dashboards live in `/metrics/`.

## Roadmap
Upcoming milestones are tracked in [`MVP_ROADMAP.md`](./MVP_ROADMAP.md).

## Contributing
1. Fork & clone  
2. `pre-commit run --all-files` must pass  
3. Create branch `feat/<topic>`  
4. Open a PR against `main`

## License
Apache-2.0 © 2024
