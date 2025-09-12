# Threat Intelligence Platform for Cyber Aware Group

A comprehensive cybersecurity platform designed to protect vulnerable populations from cyber-enabled fraud by combining enterprise-grade threat intelligence with human-centered advisory tools.

## 🚀 Features

### Core Capabilities
- **AI-Powered Fraud Advisor**: OpenAI GPT-4o powered chatbot for real-time fraud advice
- **Real-Time Threat Intelligence**: Integration with multiple threat feeds (HIBP, AbuseIPDB, SOCRadar, Netcraft, Cloudflare)
- **Breach Detection**: Check email addresses against 15+ billion compromised records
- **IP Reputation**: Real-time IP address threat assessment
- **Phishing Detection**: URL verification using zvelo PhishScan
- **SIM-Swap Protection**: Carrier API integration for OTP security
- **Human Escalation**: Seamless handoff to certified security advisors
- **Fraud Reporting**: Automated reporting to Action Fraud and Citizens Advice

### Target Users
- **Vulnerable Citizens**: Elderly individuals, low-income households, recent migrants
- **Front-line Advisers**: Citizens Advice volunteers, community support workers
- **IT Directors**: Organizations seeking cybersecurity solutions for vulnerable populations

## 🏗️ Architecture

### Technology Stack
- **Frontend**: React 18 + TypeScript + Vite + shadcn/ui + Tailwind CSS
- **Backend**: FastAPI + Python + SQLModel + PostgreSQL
- **Background Tasks**: Celery + Redis + RabbitMQ
- **AI Integration**: OpenAI GPT-4o Functions API
- **Security**: OAuth 2.0 + JWT + Rate Limiting
- **Deployment**: Docker + Docker Compose + Nginx

### System Components
1. **Client Layer**: React SPA with real-time WebSocket communication
2. **API Gateway**: FastAPI with comprehensive security middleware
3. **Data Layer**: PostgreSQL 15 + Redis for caching
4. **Threat Intelligence**: Multiple external API integrations
5. **AI Services**: OpenAI integration for fraud analysis
6. **Background Workers**: Celery for threat feed ingestion
7. **Monitoring**: Prometheus metrics + Grafana dashboards

## 🚀 Quick Start

### Prerequisites
- Docker and Docker Compose
- Python 3.11+
- Node.js 18+
- PostgreSQL 15
- Redis 7

### Environment Setup
1. Clone the repository:
```bash
git clone <repository-url>
cd vigilance-voice
```

2. Create environment file:
```bash
cp .env.example .env
# Edit .env with your API keys and configuration
```

3. Required API Keys:
```bash
OPENAI_API_KEY=your_openai_key
HIBP_API_KEY=your_hibp_key
ABUSEIPDB_API_KEY=your_abuseipdb_key
TWILIO_ACCOUNT_SID=your_twilio_sid
TWILIO_AUTH_TOKEN=your_twilio_token
```

### Development Setup

#### Option 1: Docker Compose (Recommended)
```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

#### Option 2: Local Development
```bash
# Backend
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload

# Frontend
npm install
npm run dev
```

### Database Setup
```bash
# Initialize database
cd backend
python -c "from app.core.database import init_db; init_db()"
```

## 📚 API Documentation

Once the backend is running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/healthz

### Key Endpoints
- `POST /api/v1/chatbot/sessions` - Create fraud advice session
- `GET /api/v1/threat-intelligence/breach-check/{email}` - Check email breaches
- `GET /api/v1/threat-intelligence/ip-check/{ip}` - Check IP reputation
- `GET /api/v1/threat-intelligence/phishing-check` - Verify phishing URLs

## 🔒 Security Features

### Compliance
- **Cyber Essentials Plus** aligned
- **GDPR** compliant with minimal data retention
- **NCSC** guidance following
- **WCAG 2.2 AA** accessibility standards

### Security Controls
- Rate limiting and abuse prevention
- API key management
- Zero PII retention beyond consent
- Structured audit logging
- Vulnerability assessment scoring

## 📊 Threat Intelligence Sources

| Provider | Purpose | Rate Limits | Features |
|----------|---------|-------------|----------|
| **Have I Been Pwned** | Email breach detection | 1k RPM | 15B+ records, real-time updates |
| **AbuseIPDB** | IP reputation | 1k/day free | Community-driven threat intelligence |
| **SOCRadar** | IOC feeds | 1.5k/month | 150k daily IoCs, CSV/JSON feeds |
| **Netcraft** | URL takedown | Webhook-based | Real-time threat detection |
| **Cloudflare Radar** | Global telemetry | 10 QPS | DDoS/BGP anomaly detection |
| **zvelo PhishScan** | Phishing verification | Pay-per-lookup | Live phishing verdicts |

## 🧠 AI-Powered Features

### Fraud Analysis
- **Message Analysis**: Automatic fraud type and risk level detection
- **Vulnerability Assessment**: Age, stress, and disability factor consideration
- **Escalation Logic**: Intelligent routing to human advisors
- **Context Awareness**: Conversation history and user profile integration

### Natural Language Processing
- **Plain English Advice**: Accessible security guidance
- **Multilingual Support**: English, French, Arabic (planned)
- **Voice Integration**: Speech-to-text and text-to-speech capabilities

## 📈 Monitoring & Analytics

### Metrics Dashboard
- Real-time threat statistics
- User vulnerability scoring
- Fraud pattern analysis
- Campaign effectiveness metrics

### Alerting
- Slack webhook integration
- Email notifications
- SMS alerts via Twilio
- On-call rotation management

## 🚀 Deployment

### Production Deployment
```bash
# Build production images
docker-compose -f docker-compose.prod.yml build

# Deploy with Traefik
docker-compose -f docker-compose.prod.yml up -d

# Monitor deployment
docker-compose -f docker-compose.prod.yml logs -f
```

### Infrastructure
- **AWS ECS Fargate** for container orchestration
- **RDS PostgreSQL** with read replicas
- **ElastiCache Redis** for caching
- **S3** for static assets and file storage
- **CloudFront** for global CDN

## 🧪 Testing

### Backend Testing
```bash
cd backend
pytest tests/ -v
pytest tests/ --cov=app --cov-report=html
```

### Frontend Testing
```bash
npm run test
npm run test:coverage
```

### Integration Testing
```bash
# Test complete stack
docker-compose -f docker-compose.test.yml up --abort-on-container-exit
```

## 📝 Development Guidelines

### Code Style
- **Python**: Black + isort + flake8
- **TypeScript**: ESLint + Prettier
- **Database**: SQLModel with type hints
- **API**: OpenAPI 3.0 specification

### Git Workflow
1. Feature branches from `develop`
2. Pull request reviews required
3. Automated testing on PR
4. Semantic versioning

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

### Development Setup
```bash
# Install pre-commit hooks
pre-commit install

# Run linting
pre-commit run --all-files
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

- **Documentation**: [Wiki](wiki-url)
- **Issues**: [GitHub Issues](issues-url)
- **Discussions**: [GitHub Discussions](discussions-url)
- **Email**: support@cyberawaregroup.org

## 🙏 Acknowledgments

- **Citizens Advice** for community partnership
- **Age UK** for vulnerability assessment guidance
- **NCSC** for cybersecurity best practices
- **OpenAI** for AI capabilities
- **Open Source Community** for foundational technologies

---

**Built with ❤️ for vulnerable populations by the Cyber Aware Group team**
