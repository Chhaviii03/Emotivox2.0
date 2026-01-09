# Deployment Guide for Render

This guide will help you deploy the Flask backend to Render.

## Prerequisites

1. A GitHub account
2. Your code pushed to a GitHub repository
3. A Render account (free at https://render.com)

## Step-by-Step Deployment

### 1. Prepare Your Repository

Make sure all the following files are in your `Backend/` directory:
- `app.py` - Your Flask application
- `requirements.txt` - Python dependencies
- `Procfile` - Tells Render how to run your app
- `runtime.txt` - Specifies Python version

### 2. Push to GitHub

```bash
git add .
git commit -m "Prepare for Render deployment"
git push origin main
```

### 3. Deploy on Render

1. Go to https://dashboard.render.com
2. Click "New +" → "Web Service"
3. Connect your GitHub repository
4. Configure the service:
   - **Name**: `emotivox-backend` (or your preferred name)
   - **Region**: Choose closest to your users
   - **Branch**: `main` (or your default branch)
   - **Root Directory**: `Backend` (important!)
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app --bind 0.0.0.0:$PORT --timeout 300`
   - **Instance Type**: Free (for testing)

5. Click "Create Web Service"

### 4. Environment Variables (Optional)

You can add environment variables in Render dashboard:
- Go to your service → Environment tab
- Add any needed variables

### 5. Wait for Deployment

- First deployment may take 15-30 minutes (TTS model download)
- Monitor the logs for any errors
- The service will be available at `https://your-service-name.onrender.com`

### 6. Update Your React App

1. In Netlify dashboard, go to your site settings
2. Navigate to "Environment Variables"
3. Add: `VITE_API_URL` = `https://your-service-name.onrender.com`
4. Redeploy your React app

## Important Notes

⚠️ **Free Tier Limitations:**
- Services spin down after 15 minutes of inactivity
- First request after spin-down takes ~30 seconds (cold start)
- The TTS model is large (~1-2GB) - first build/download will take time

💡 **Tips:**
- Use the `/health` endpoint to keep your service alive
- Consider upgrading to a paid plan for better performance
- Monitor your logs for any issues

## Testing

Test your deployed backend:
```bash
# Health check
curl https://your-service-name.onrender.com/health

# Test clone endpoint (with proper form data)
curl -X POST https://your-service-name.onrender.com/clone \
  -F "text=Hello world" \
  -F "voiceFiles=@test.wav"
```

## Troubleshooting

### Build fails with dependency errors
- Check `requirements.txt` syntax
- Ensure all dependencies are compatible with Python 3.10
- Check Render logs for specific error messages

### Timeout errors
- Increase timeout in Procfile (currently 300 seconds)
- Consider using lazy model loading (already implemented)

### CORS errors
- Make sure CORS is configured in `app.py` (already set to allow all origins)
- Verify your React app is using the correct API URL

### Model download fails
- Check Render logs for download progress
- The first deployment will take longer due to model download
- Ensure sufficient disk space (free tier has limits)

## Support

For issues:
1. Check Render dashboard logs
2. Verify all files are in correct locations
3. Test locally first with: `gunicorn app:app --bind 0.0.0.0:5000`

