# GenAI Security Ensemble 🔒

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115.4-009688.svg)](https://fastapi.tiangolo.com/)
[![GitHub](https://img.shields.io/badge/GitHub-Repository-181717.svg?logo=github)](https://github.com/OkbaBenatia/genai-security-ensemble)

**🔗 Repository**: [https://github.com/OkbaBenatia/genai-security-ensemble](https://github.com/OkbaBenatia/genai-security-ensemble)

A production-ready **LLM security firewall** that protects Large Language Model applications from malicious inputs, prompt injections, and data exfiltration attempts. This ensemble-based system combines multiple detection techniques to provide robust security for GenAI deployments.

## 🎯 Overview

GenAI Security Ensemble is an open-source security layer designed to sit between users and LLM applications. It uses a multi-layered detection approach combining keyword analysis, machine learning-based anomaly detection, and zero-shot intent classification to identify and block potentially harmful requests before they reach your LLM.

### Why Use This?

- **🛡️ Multi-Layer Protection**: Combines multiple detection methods for higher accuracy
- **⚡ Fast & Lightweight**: Minimal latency overhead with efficient ML models
- **🔧 Policy-as-Code**: Define security policies in YAML for easy updates
- **📊 Comprehensive Logging**: JSONL-based event logging for audit trails
- **🐳 Docker Ready**: Containerized deployment for easy integration
- **🔌 API-First**: RESTful API that integrates with any LLM application

## ✨ Features

### Core Security Features

- **Keyword Detection**: Fast pattern matching for known attack vectors
- **Anomaly Detection**: Isolation Forest-based detection of unusual input patterns
- **Intent Classification**: Zero-shot classification using BART-MNLI to identify malicious intent
- **PII Redaction**: Automatic detection and redaction of sensitive information (emails, phone numbers, AWS keys)
- **Prompt Injection Detection**: Heuristic-based detection of common injection patterns
- **Output Policy Enforcement**: Post-generation checks to prevent data leakage

### Operational Features

- **RESTful API**: FastAPI-based endpoints for easy integration
- **JSONL Logging**: Structured logging for security events and audit trails
- **Human Review Tools**: Helper scripts for reviewing flagged events
- **Configurable Thresholds**: Tuneable detection sensitivity
- **Policy Management**: YAML-based policy configuration
- **Docker Support**: Containerized deployment with Docker Compose

## 🏗️ Architecture

The system uses an **ensemble decision-making approach** that combines three detection methods:

```
User Input
    ↓
[PII Redaction] → Sanitized Input
    ↓
[Injection Detection] → If detected: BLOCK
    ↓
[Ensemble Decision]
    ├─→ Keyword Detector
    ├─→ Anomaly Detector (Isolation Forest)
    └─→ Intent Classifier (Zero-Shot BART-MNLI)
    ↓
Decision: ALLOW | FLAG | BLOCK
    ↓
[Logging & Response]
```

### Decision Logic

- **BLOCK**: High-confidence malicious intent OR keyword + anomaly detected
- **FLAG**: Suspicious patterns requiring human review
- **ALLOW**: Low-risk input that passes all checks

## 🚀 Quick Start

### Prerequisites

- Python 3.11 or higher
- pip package manager
- (Optional) Docker and Docker Compose for containerized deployment

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/OkbaBenatia/genai-security-ensemble.git
   cd genai-security-ensemble
   ```

2. **Create virtual environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   ```bash
   cp .env.example .env
   # Edit .env if needed (defaults are usually fine)
   ```

5. **Start the server**
   ```bash
   uvicorn src.app:app --reload
   ```

The API will be available at `http://localhost:8000`

### Docker Deployment

1. **Build and run with Docker Compose**
   ```bash
   docker-compose up -d
   ```

2. **View logs**
   ```bash
   docker-compose logs -f
   ```

3. **Stop the service**
   ```bash
   docker-compose down
   ```

## 📖 API Documentation

Once the server is running, visit:
- **Interactive API Docs**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

### Endpoints

#### `POST /guard/inspect`

Inspect a text input and get a security decision without calling an LLM.

**Request Body:**
```json
{
  "text": "Your input text here"
}
```

**Response:**
```json
{
  "decision": "ALLOW|FLAG|BLOCK",
  "meta": {
    "intent_label": "benign|suspicious|malicious",
    "intent_score": 0.95,
    "iso_score": 0.12,
    "keyword": false,
    "reason": "low_risk"
  }
}
```

**Example:**
```bash
curl -X POST "http://localhost:8000/guard/inspect" \
  -H "Content-Type: application/json" \
  -d '{"text": "What is the weather today?"}'
```

#### `POST /guard/generate`

Full pipeline including output policy checks (simulated LLM in scaffold version).

**Request Body:**
```json
{
  "text": "Your prompt here"
}
```

**Response:**
```json
{
  "answer": "Generated response (if allowed)"
}
```

**Example:**
```bash
curl -X POST "http://localhost:8000/guard/generate" \
  -H "Content-Type: application/json" \
  -d '{"text": "Explain quantum computing"}'
```

## ⚙️ Configuration

### Environment Variables

Create a `.env` file in the project root:

```env
# Path to the JSONL log file for security events
LOG_PATH=security_events.jsonl
```

### Policy Configuration

Edit `policies/llm_policy.yml` to customize:

- **Injection Indicators**: Patterns that trigger prompt injection detection
- **Output Rules**: Policies for generated content (PII blocking, banned terms)

Example policy structure:
```yaml
injection_indicators:
  - "ignore previous"
  - "system prompt"
  - "exfiltrate"

output_rules:
  no_pii: true
  banned_terms:
    - "nuke"
    - "bomb"
```

### Threshold Tuning

Adjust detection sensitivity in `src/pipelines.py`:

```python
SCORE_THRESH_MALICIOUS = 0.70     # Zero-shot malicious confidence threshold
IFOREST_SCORE_THRESH   = -0.05    # Isolation Forest anomaly threshold
```

## 📁 Project Structure

```
genai-security-ensemble/
├── src/
│   ├── app.py              # FastAPI application and endpoints
│   ├── models.py           # ML model loading (embeddings, zero-shot)
│   ├── detectors.py        # Anomaly detector and keyword detection
│   ├── pipelines.py        # Ensemble decision logic
│   ├── guardrails.py       # PII redaction, injection detection, output checks
│   ├── logging_utils.py    # JSONL event logging
│   └── human_review.py    # Helper for reviewing flagged events
├── data/
│   ├── benign_seed.txt     # Training examples for benign inputs
│   └── malicious_seed.txt  # Training examples for malicious inputs
├── policies/
│   └── llm_policy.yml      # Policy-as-code configuration
├── tests/
│   ├── test_guardrails.py  # Guardrails unit tests
│   └── test_pipeline.py    # Pipeline integration tests
├── Dockerfile              # Container image definition
├── docker-compose.yml      # Docker Compose configuration
├── requirements.txt        # Python dependencies
└── .env.example           # Environment variable template
```

## 🧪 Testing

Run the test suite:

```bash
# Activate virtual environment first
source .venv/bin/activate

# Run all tests
pytest tests/

# Run specific test file
pytest tests/test_guardrails.py -v
```

## 🔍 Usage Examples

### Python Integration

```python
import requests

# Check if input is safe
response = requests.post(
    "http://localhost:8000/guard/inspect",
    json={"text": "User input here"}
)

result = response.json()
if result["decision"] == "ALLOW":
    # Proceed with LLM call
    pass
elif result["decision"] == "BLOCK":
    # Reject the request
    pass
else:  # FLAG
    # Send for human review
    pass
```

### Reviewing Flagged Events

```bash
python src/human_review.py
```

This will display all `FLAG` events from the log file for manual review.

## 🤝 Contributing

**We welcome contributions!** This is an open-source project and we need developers to help improve it.

### How to Contribute

1. **Fork the repository** at [https://github.com/OkbaBenatia/genai-security-ensemble](https://github.com/OkbaBenatia/genai-security-ensemble)
2. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. **Make your changes** and add tests
4. **Run the test suite** to ensure everything passes
5. **Submit a pull request** with a clear description of your changes

### Areas Where We Need Help

- 🐛 **Bug Fixes**: Report and fix issues
- ✨ **New Features**: Add detection methods, improve accuracy
- 📚 **Documentation**: Improve docs, add examples, tutorials
- 🧪 **Testing**: Expand test coverage, add integration tests
- 🎨 **UI/UX**: Build a web dashboard for monitoring and review
- ⚡ **Performance**: Optimize model loading, reduce latency
- 🌐 **Integrations**: Add support for more LLM providers
- 🔒 **Security**: Enhance detection methods, add new attack pattern recognition

### Development Setup

1. Clone and set up as described in Quick Start
2. Install development dependencies (if any)
3. Make your changes
4. Ensure tests pass: `pytest tests/`
5. Follow code style (PEP 8 for Python)

### Reporting Issues

Found a bug or have a feature request? Please open an issue on GitHub with:
- Clear description of the problem/feature
- Steps to reproduce (for bugs)
- Expected vs actual behavior
- Environment details (OS, Python version, etc.)

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🗺️ Roadmap

- [ ] Support for more LLM providers (OpenAI, Anthropic, etc.)
- [ ] Real-time monitoring dashboard
- [ ] Advanced ML models for better detection
- [ ] Rate limiting and DDoS protection
- [ ] Multi-language support
- [ ] GraphQL API option
- [ ] Kubernetes deployment manifests
- [ ] Performance benchmarking suite
- [ ] Pre-trained model fine-tuning tools

## 🙏 Acknowledgments

- Built with [FastAPI](https://fastapi.tiangolo.com/)
- Uses [sentence-transformers](https://www.sbert.net/) for embeddings
- Zero-shot classification powered by [Hugging Face Transformers](https://huggingface.co/transformers/)
- Anomaly detection using [scikit-learn](https://scikit-learn.org/)

## 📧 Support

- **Issues**: Open an issue on [GitHub](https://github.com/OkbaBenatia/genai-security-ensemble/issues)
- **Discussions**: Use [GitHub Discussions](https://github.com/OkbaBenatia/genai-security-ensemble/discussions) for questions
- **Repository**: [https://github.com/OkbaBenatia/genai-security-ensemble](https://github.com/OkbaBenatia/genai-security-ensemble)
- **Security**: For security vulnerabilities, please email directly (don't open public issues)

---

**Made with ❤️ by the open-source community**

*Help us make GenAI applications safer for everyone!*
