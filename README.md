# Incident Management & Observability Framework

A distributed system for real-time incident management, alerting, and observability built with modern technologies.

## Features

- Real-time alerting system using NATS pub/sub streams
- Centralized log aggregation with Elasticsearch
- Incident Commander CLI for streamlined incident response
- Automated on-call rotation and paging
- Post-mortem report generation
- Containerized deployment with Docker and Kubernetes
- Multi-tenant monitoring with RBAC and network policies

## Architecture

```
├── alerting/           # NATS-based alerting system
├── cli/               # Python/Bash CLI tools
├── kubernetes/        # K8s manifests and configs
├── observability/     # Monitoring and logging components
└── docs/             # Documentation and runbooks
```

## Prerequisites

- Python 3.9+
- Docker
- Kubernetes cluster
- NATS server
- Elasticsearch cluster

## Quick Start

1. Clone the repository:
```bash
git clone https://github.com/hardikkgupta/incident-framework.git
cd incident-framework
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Deploy to Kubernetes:
```bash
./deploy.sh
```

4. Install the CLI (for local development):
```bash
pip install -e .
```

5. Use the CLI:
```bash
incident-framework --help
```

## Components

### Alerting System
- NATS-based pub/sub for real-time alert distribution
- Elasticsearch for log aggregation and analysis
- Custom alert rules and routing

### Incident Commander CLI
- Python-based command-line interface
- Automated on-call rotation management
- Incident response workflows
- Post-mortem report generation

### Observability Stack
- Containerized monitoring components
- Multi-tenant support with RBAC
- Network policies for security
- Metrics collection and visualization

## Contributing

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct and the process for submitting pull requests.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.