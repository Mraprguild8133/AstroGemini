# Docker Deployment Guide

This guide explains how to deploy your Multi-AI Telegram Bot using Docker containers.

## Quick Start

1. **Clone the repository and navigate to the project directory**
2. **Copy environment variables:**
   ```bash
   cp .env.example .env
   ```
3. **Edit `.env` file with your API keys**
4. **Run with Docker Compose:**
   ```bash
   docker-compose up -d
   ```

## Docker Setup Options

### Option 1: Docker Compose (Recommended)

**For Polling Mode (Default):**
```bash
# Start the bot in polling mode
docker-compose up -d telegram-bot

# View logs
docker-compose logs -f telegram-bot
```

**For Webhook Mode:**
```bash
# Set WEBHOOK_URL in .env file first
echo "WEBHOOK_URL=https://your-domain.com" >> .env

# Start webhook mode
docker-compose --profile webhook up -d telegram-bot-webhook

# View logs  
docker-compose logs -f telegram-bot-webhook
```

### Option 2: Direct Docker Commands

**Build the image:**
```bash
docker build -t telegram-gemini-bot .
```

**Run in polling mode:**
```bash
docker run -d \
  --name telegram-bot \
  --env-file .env \
  -v $(pwd)/logs:/app/logs \
  telegram-gemini-bot
```

**Run in webhook mode:**
```bash
docker run -d \
  --name telegram-bot-webhook \
  --env-file .env \
  -p 5000:5000 \
  -v $(pwd)/logs:/app/logs \
  telegram-gemini-bot python webhook_main.py
```

## Environment Variables

### Required Variables

Create a `.env` file with these required variables:

```bash
# Get from @BotFather on Telegram
TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here

# Get from Google AI Studio (https://aistudio.google.com)
GEMINI_API_KEY=your_gemini_api_key_here
```

### Optional Variables

```bash
# Together AI API Key (enables 4 additional AI models)
TOGETHER_API_KEY=your_together_api_key_here

# Webhook URL (required for webhook mode)
WEBHOOK_URL=https://your-domain.com

# Rate limiting (defaults shown)
RATE_LIMIT_REQUESTS=10
RATE_LIMIT_WINDOW=60

# Conversation settings
MAX_CONVERSATION_LENGTH=20

# AI model configuration
GEMINI_MODEL=gemini-2.5-flash
GEMINI_TEMPERATURE=0.7
GEMINI_MAX_TOKENS=1000

TOGETHER_DEFAULT_MODEL=meta-llama/Llama-2-70b-chat-hf
TOGETHER_TEMPERATURE=0.7
TOGETHER_MAX_TOKENS=1000
```

## Deployment Scenarios

### Local Development

```bash
# Start with logs visible
docker-compose up telegram-bot

# Stop
docker-compose down
```

### Production Server

```bash
# Start in background with restart policy
docker-compose up -d telegram-bot

# Check status
docker-compose ps

# View logs
docker-compose logs -f telegram-bot

# Update and restart
docker-compose pull
docker-compose up -d telegram-bot
```

### Cloud Deployment (VPS/Dedicated Server)

1. **Install Docker and Docker Compose on your server**
2. **Upload your project files**
3. **Configure environment variables:**
   ```bash
   cp .env.example .env
   nano .env  # Add your API keys
   ```
4. **Start the bot:**
   ```bash
   docker-compose up -d telegram-bot
   ```
5. **Set up automatic updates (optional):**
   ```bash
   # Create update script
   echo '#!/bin/bash
   cd /path/to/your/bot
   git pull
   docker-compose pull
   docker-compose up -d telegram-bot' > update-bot.sh
   chmod +x update-bot.sh
   
   # Add to crontab for daily updates
   crontab -e
   # Add: 0 2 * * * /path/to/update-bot.sh
   ```

### Webhook Mode for Production

For production webhook deployment:

1. **Set up a domain with SSL certificate**
2. **Configure reverse proxy (nginx example):**
   ```nginx
   server {
       listen 80;
       server_name your-domain.com;
       return 301 https://$server_name$request_uri;
   }
   
   server {
       listen 443 ssl;
       server_name your-domain.com;
       
       ssl_certificate /path/to/your/certificate.pem;
       ssl_certificate_key /path/to/your/private.key;
       
       location / {
           proxy_pass http://localhost:5000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
           proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
           proxy_set_header X-Forwarded-Proto $scheme;
       }
   }
   ```
3. **Set WEBHOOK_URL in .env:**
   ```bash
   WEBHOOK_URL=https://your-domain.com
   ```
4. **Start webhook mode:**
   ```bash
   docker-compose --profile webhook up -d telegram-bot-webhook
   ```

## Container Management

### Basic Commands

```bash
# Check running containers
docker-compose ps

# View logs (last 100 lines)
docker-compose logs --tail=100 telegram-bot

# Follow logs in real-time
docker-compose logs -f telegram-bot

# Restart the bot
docker-compose restart telegram-bot

# Stop the bot
docker-compose stop telegram-bot

# Remove containers and networks
docker-compose down

# Remove containers, networks, and volumes
docker-compose down -v
```

### Health Checks

The containers include health checks:

```bash
# Check container health
docker-compose ps
# Look for "healthy" status

# Manual health check
docker exec telegram-gemini-bot python -c "print('Bot is healthy')"
```

### Resource Monitoring

```bash
# Check resource usage
docker stats telegram-gemini-bot

# View detailed container info
docker inspect telegram-gemini-bot
```

## Troubleshooting

### Common Issues

**Bot not starting:**
```bash
# Check logs for errors
docker-compose logs telegram-bot

# Verify environment variables
docker-compose config
```

**API key issues:**
```bash
# Verify environment file
cat .env

# Check if variables are loaded
docker exec telegram-gemini-bot env | grep -E "(TELEGRAM|GEMINI|TOGETHER)"
```

**Webhook not working:**
```bash
# Check if webhook mode is running
docker-compose ps telegram-bot-webhook

# Test webhook endpoint
curl https://your-domain.com/

# Check webhook logs
docker-compose logs -f telegram-bot-webhook
```

**Performance issues:**
```bash
# Check resource usage
docker stats telegram-gemini-bot

# Increase resource limits in docker-compose.yml
# Edit the deploy.resources section
```

### Log Analysis

```bash
# Search logs for errors
docker-compose logs telegram-bot | grep -i error

# Search logs for specific user
docker-compose logs telegram-bot | grep "user_id_here"

# Export logs to file
docker-compose logs telegram-bot > bot-logs.txt
```

## Security Best Practices

1. **Use non-root user in container** (already implemented)
2. **Keep secrets in environment file:**
   ```bash
   chmod 600 .env  # Restrict access to .env file
   ```
3. **Regular updates:**
   ```bash
   # Update base images regularly
   docker-compose pull
   docker-compose up -d telegram-bot
   ```
4. **Network isolation:**
   ```bash
   # The compose file creates an isolated network
   docker network ls | grep telegram-bot-network
   ```
5. **Resource limits** (already configured in compose file)

## Backup and Recovery

### Backup Configuration

```bash
# Backup environment and compose files
tar -czf bot-config-backup.tar.gz .env docker-compose.yml

# Backup logs
tar -czf bot-logs-backup.tar.gz logs/
```

### Recovery

```bash
# Restore configuration
tar -xzf bot-config-backup.tar.gz

# Rebuild and start
docker-compose up -d telegram-bot
```

## Scaling and High Availability

### Multiple Instances

```bash
# Scale up (polling mode only - webhook needs single instance)
docker-compose up -d --scale telegram-bot=3
```

### Load Balancer Setup

For webhook mode with multiple instances, use a load balancer:

```yaml
# Add to docker-compose.yml
nginx:
  image: nginx:alpine
  ports:
    - "80:80"
    - "443:443"
  volumes:
    - ./nginx.conf:/etc/nginx/nginx.conf
  depends_on:
    - telegram-bot-webhook
```

## Monitoring and Alerts

### Basic Monitoring

```bash
# Create monitoring script
cat > monitor-bot.sh << 'EOF'
#!/bin/bash
if [ "$(docker inspect -f '{{.State.Health.Status}}' telegram-gemini-bot)" != "healthy" ]; then
    echo "Bot unhealthy - restarting..."
    docker-compose restart telegram-bot
fi
EOF

chmod +x monitor-bot.sh

# Run every 5 minutes
echo "*/5 * * * * /path/to/monitor-bot.sh" | crontab -
```

Your dual AI Telegram bot is now fully containerized and ready for professional deployment across any Docker-compatible environment!