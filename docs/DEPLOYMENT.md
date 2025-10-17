# 🚀 Deployment Guide

Complete guide for deploying your AI Customer Support Chatbot to various environments.

---

## 📋 Table of Contents

1. [Local Deployment](#local-deployment)
2. [Docker Deployment](#docker-deployment)
3. [Cloud Deployment](#cloud-deployment)
4. [Configuration](#configuration)
5. [Monitoring](#monitoring)
6. [Troubleshooting](#troubleshooting)

---

## 🏠 Local Deployment

### Standard Installation

```bash
# 1. Clone repository
git clone https://github.com/yourusername/AI-Customer-Support-Chatbot.git
cd AI-Customer-Support-Chatbot

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure environment
cp config/.env.example config/.env
# Edit config/.env with your settings

# 4. Start Ollama
ollama serve

# 5. Pull model
ollama pull gpt-oss:20b

# 6. Build vector database (first time only)
python scripts/build_vector_db.py

# 7. Run chatbot
python app.py
```

### Package Installation

```bash
# Install as package
pip install -e .

# Run as command
chatbot
```

---

## 🐳 Docker Deployment

### Using Docker Compose (Recommended)

**Best for:** Complete stack with Ollama included

```bash
# Build and start
docker-compose up --build

# Run in background
docker-compose up -d

# Stop
docker-compose down

# View logs
docker-compose logs -f chatbot
```

**Access:** http://localhost:7860

### Using Dockerfile Only

**Best for:** Deploying to existing infrastructure

```bash
# Build image
docker build -t ai-customer-support-chatbot .

# Run container
docker run -d \
  --name chatbot \
  -p 7860:7860 \
  -v $(pwd)/chroma_db:/app/chroma_db \
  -v $(pwd)/data:/app/data \
  -v $(pwd)/logs:/app/logs \
  -e MODEL_NAME=gpt-oss:20b \
  -e OLLAMA_BASE_URL=http://host.docker.internal:11434 \
  ai-customer-support-chatbot

# View logs
docker logs -f chatbot

# Stop
docker stop chatbot
```

### Docker Best Practices

```dockerfile
# Use multi-stage builds
FROM python:3.13-slim as builder
# ... build stage ...

FROM python:3.13-slim
# ... runtime stage ...

# Health check
HEALTHCHECK --interval=30s --timeout=10s \
  CMD curl -f http://localhost:7860/ || exit 1
```

---

## ☁️ Cloud Deployment

### AWS (Amazon Web Services)

#### Option 1: AWS ECS (Elastic Container Service)

```bash
# 1. Build and push to ECR
aws ecr create-repository --repository-name ai-chatbot
docker tag ai-customer-support-chatbot:latest \
  123456789.dkr.ecr.us-east-1.amazonaws.com/ai-chatbot:latest
docker push 123456789.dkr.ecr.us-east-1.amazonaws.com/ai-chatbot:latest

# 2. Create ECS task definition
# 3. Create ECS service
# 4. Configure load balancer
```

#### Option 2: AWS EC2

```bash
# 1. Launch EC2 instance (t3.xlarge recommended)
# 2. SSH into instance
# 3. Install Docker
# 4. Run docker-compose

ssh -i key.pem ubuntu@ec2-ip
sudo apt update
sudo apt install docker.io docker-compose
git clone <your-repo>
cd AI-Customer-Support-Chatbot
sudo docker-compose up -d
```

### Azure

#### Azure Container Instances

```bash
# 1. Login to Azure
az login

# 2. Create resource group
az group create --name chatbot-rg --location eastus

# 3. Deploy container
az container create \
  --resource-group chatbot-rg \
  --name ai-chatbot \
  --image <your-image> \
  --dns-name-label ai-chatbot \
  --ports 7860
```

### Google Cloud Platform (GCP)

#### Cloud Run

```bash
# 1. Build and push to GCR
gcloud builds submit --tag gcr.io/PROJECT-ID/ai-chatbot

# 2. Deploy to Cloud Run
gcloud run deploy ai-chatbot \
  --image gcr.io/PROJECT-ID/ai-chatbot \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

### Heroku

```bash
# 1. Create Heroku app
heroku create ai-customer-support-chatbot

# 2. Add buildpack
heroku buildpacks:set heroku/python

# 3. Deploy
git push heroku main

# 4. Scale up
heroku ps:scale web=1:standard-2x
```

---

## ⚙️ Configuration

### Environment Variables

**Production Settings:**

```bash
# config/.env
MODEL_NAME=gpt-oss:20b
OLLAMA_BASE_URL=http://ollama:11434
CHROMA_PERSIST_DIR=/app/chroma_db
GRADIO_SERVER_PORT=7860
GRADIO_SERVER_NAME=0.0.0.0
FORCE_CPU=false
TOP_K_RESULTS=5
LOG_LEVEL=INFO
```

### Scaling Configuration

**For High Traffic:**

```bash
# Increase workers (if using Gunicorn)
workers=4
worker_class=uvicorn.workers.UvicornWorker

# Increase vector DB cache
CHROMA_CACHE_SIZE=1000000

# Batch processing
BATCH_SIZE=256
```

---

## 📊 Monitoring

### Health Checks

```bash
# Docker health check
curl http://localhost:7860/

# Ollama health
curl http://localhost:11434/api/tags
```

### Logging

```python
# config/settings.py
LOG_LEVEL = "INFO"  # DEBUG, INFO, WARNING, ERROR
LOG_FILE = "logs/chatbot.log"
```

**View logs:**
```bash
# Docker
docker logs -f chatbot

# Local
tail -f logs/chatbot.log
```

### Monitoring Tools

**Prometheus + Grafana:**

```yaml
# docker-compose.yml
services:
  prometheus:
    image: prom/prometheus
    ports:
      - "9090:9090"
      
  grafana:
    image: grafana/grafana
    ports:
      - "3000:3000"
```

---

## 🔒 Security

### Production Security Checklist

- [ ] Use HTTPS (SSL/TLS certificates)
- [ ] Set up firewall rules
- [ ] Use environment variables for secrets
- [ ] Enable rate limiting
- [ ] Implement authentication
- [ ] Regular security updates
- [ ] Backup vector database
- [ ] Monitor logs for suspicious activity

### SSL/TLS Setup

```bash
# Using Nginx as reverse proxy
server {
    listen 443 ssl;
    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;
    
    location / {
        proxy_pass http://localhost:7860;
    }
}
```

---

## 🔄 CI/CD Pipeline

### GitHub Actions

```yaml
# .github/workflows/deploy.yml
name: Deploy

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Build Docker image
        run: docker build -t chatbot .
        
      - name: Run tests
        run: pytest tests/
        
      - name: Deploy to production
        run: |
          # Your deployment commands
```

---

## 🐛 Troubleshooting

### Common Issues

**Issue: Container Out of Memory**
```bash
# Increase Docker memory limit
docker run --memory="4g" ...
```

**Issue: Slow Response Times**
```bash
# Increase TOP_K_RESULTS
TOP_K_RESULTS=3

# Enable GPU
FORCE_CPU=false
```

**Issue: Port Already in Use**
```bash
# Change port
GRADIO_SERVER_PORT=8080
```

---

## 📈 Performance Tuning

### Vector Database Optimization

```python
# config/settings.py
BATCH_SIZE = 256  # Larger for faster processing
TOP_K_RESULTS = 3  # Fewer for faster retrieval
```

### Caching

```python
# Add caching layer
from functools import lru_cache

@lru_cache(maxsize=1000)
def get_cached_response(query):
    return chatbot.query(query)
```

---

## 🔄 Updates & Maintenance

### Updating the Application

```bash
# 1. Pull latest changes
git pull origin main

# 2. Update dependencies
pip install -r requirements.txt --upgrade

# 3. Rebuild vector database (if dataset changed)
python scripts/build_vector_db.py

# 4. Restart application
# Docker: docker-compose restart
# Local: Ctrl+C and python app.py
```

### Backup Strategy

```bash
# Backup vector database
tar -czf chroma_db_backup_$(date +%Y%m%d).tar.gz chroma_db/

# Backup data
tar -czf data_backup_$(date +%Y%m%d).tar.gz data/

# Backup logs
tar -czf logs_backup_$(date +%Y%m%d).tar.gz logs/
```

---

## 🎯 Production Checklist

Before deploying to production:

- [ ] Environment variables configured
- [ ] SSL/TLS certificates installed
- [ ] Firewall rules set up
- [ ] Monitoring enabled
- [ ] Logging configured
- [ ] Backups automated
- [ ] Health checks working
- [ ] Load testing completed
- [ ] Documentation updated
- [ ] Team trained on deployment

---

## 📞 Support

For deployment issues:
- 📖 Check documentation
- 🐛 Open GitHub issue
- 💬 Ask in discussions
- 📧 Contact maintainers

---

**Happy Deploying!** 🚀

*Last updated: October 2025*

