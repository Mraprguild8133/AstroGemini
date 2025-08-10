# Render.com Deployment Guide

This guide explains how to deploy your Multi-AI Telegram Bot to Render.com using webhooks.

## Why Webhooks on Render.com?

**Polling vs Webhooks:**
- **Polling** (current setup): Bot continuously asks Telegram for updates
- **Webhooks**: Telegram sends updates directly to your server

**Benefits of Webhooks:**
- ⚡ Lower latency - instant message delivery
- 💰 Reduced server costs - no continuous polling
- 🚀 Better scalability - handles high message volumes
- 🔋 More efficient - less resource usage

## Deployment Steps

### 1. Prepare Your Repository

Your bot now includes webhook support with these files:
- `webhook_server.py` - Webhook server implementation
- `webhook_main.py` - Entry point for webhook mode
- `render.yaml` - Render.com configuration
- `DEPLOYMENT.md` - This deployment guide

### 2. Deploy to Render.com

**Option A: GitHub Integration (Recommended)**
1. Push your code to GitHub
2. Go to [Render.com](https://render.com) and sign up
3. Create a new Web Service
4. Connect your GitHub repository
5. Render will auto-detect Python and use the configuration

**Option B: Manual Deploy**
1. Go to [Render.com](https://render.com)
2. Create a new Web Service
3. Choose "Deploy from Git" 
4. Connect your repository
5. Configure the service settings

### 3. Environment Variables

Set these environment variables in Render.com dashboard:

**Required:**
```
TELEGRAM_BOT_TOKEN=your_bot_token_here
GEMINI_API_KEY=your_gemini_api_key_here  
WEBHOOK_URL=https://your-app-name.onrender.com
```

**Optional (for Together AI):**
```
TOGETHER_API_KEY=your_together_api_key_here
```

**Configuration (optional):**
```
RATE_LIMIT_REQUESTS=10
RATE_LIMIT_WINDOW=60
MAX_CONVERSATION_LENGTH=20
GEMINI_MODEL=gemini-2.5-flash
GEMINI_TEMPERATURE=0.7
GEMINI_MAX_TOKENS=1000
TOGETHER_DEFAULT_MODEL=meta-llama/Llama-2-70b-chat-hf
TOGETHER_TEMPERATURE=0.7
TOGETHER_MAX_TOKENS=1000
```

### 4. Service Configuration

**Build Command:** `pip install -r requirements.txt`
**Start Command:** `python webhook_main.py`
**Environment:** Python 3.11

### 5. Set Your Webhook URL

After deployment, your app will be available at:
`https://your-app-name.onrender.com`

Update the `WEBHOOK_URL` environment variable with your actual Render.com URL.

## Webhook Endpoints

Your deployed bot will have these endpoints:

- `GET /` - Health check endpoint
- `POST /webhook` - Telegram webhook endpoint  
- `POST /set_webhook` - Manual webhook setup (if needed)

## Testing Your Deployment

1. **Health Check:** Visit `https://your-app-name.onrender.com/`
   - Should return: `{"status": "ok", "bot": "running"}`

2. **Bot Commands:** Test in Telegram:
   - `/start` - Welcome message
   - `/status` - Should show "Webhook Mode"
   - `/help` - All available commands

3. **AI Switching:** 
   - `/ai together` - Switch to Together AI
   - `/models` - View available models

## Troubleshooting

### Common Issues:

**Bot not responding:**
- Check environment variables are set correctly
- Verify webhook URL is correct
- Check Render.com logs for errors

**Webhook not working:**
- Ensure WEBHOOK_URL matches your Render.com app URL
- Try the `/set_webhook` endpoint manually
- Check Telegram webhook status with BotFather

**AI services not working:**
- Verify API keys are valid and have quota
- Check logs for authentication errors
- Test individual AI services

### Render.com Specific:

**Free Tier Limitations:**
- Service sleeps after 15 minutes of inactivity
- 750 hours/month limit
- Slower cold starts

**Paid Tier Benefits:**
- Always-on service
- Faster performance
- More resources

## Monitoring

**Render.com Dashboard:**
- View deployment logs
- Monitor resource usage
- Check service health

**Bot Status:**
- Use `/status` command in Telegram
- Monitor response times
- Check error rates in logs

## File Structure for Deployment

```
├── webhook_server.py      # Webhook implementation
├── webhook_main.py        # Entry point
├── main.py               # Original polling version
├── bot.py                # Core bot logic
├── gemini_service.py     # Gemini AI integration
├── together_service.py   # Together AI integration
├── rate_limiter.py       # Rate limiting
├── config.py             # Configuration
├── render.yaml           # Render.com config
├── DEPLOYMENT.md         # This guide
├── README.md             # Project documentation
└── DEPENDENCIES.md       # Package requirements
```

## Cost Comparison

**Replit (Current):**
- Always-on: $20/month
- Development-focused
- Built-in editor and tools

**Render.com:**
- Free tier: $0/month (with limitations)
- Starter: $7/month (always-on)
- Production-focused
- Better for deployment

## Migration Benefits

✅ **Webhook Mode:** Faster, more efficient
✅ **Production Deployment:** Reliable cloud hosting
✅ **Cost Effective:** Free or low-cost options
✅ **Scalable:** Handles more users
✅ **Professional:** Custom domain support

Your bot will work exactly the same way for users, but with better performance and lower costs!