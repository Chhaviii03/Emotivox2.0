# Quick Start: Deploy Flask Backend to Render

## ✅ What's Been Done

Your Flask backend is now ready for Render deployment! Here's what was configured:

### Files Created/Updated:

1. ✅ **Backend/Procfile** - Tells Render how to run your Flask app
2. ✅ **Backend/runtime.txt** - Specifies Python 3.10.12
3. ✅ **Backend/app.py** - Updated with:
   - Lazy TTS model loading (prevents timeout)
   - CORS enabled for all origins
   - Port handling from environment variable
   - Better error handling
   - Health check endpoint
4. ✅ **Backend/requirements.txt** - Cleaned up and optimized
5. ✅ **src/components/VoiceCloning.jsx** - Updated to use environment variable for API URL
6. ✅ **.gitignore** - Updated to ignore outputs and env files

## 🚀 Deploy to Render (5 Steps)

### Step 1: Push to GitHub
```bash
git add .
git commit -m "Ready for Render deployment"
git push origin main
```

### Step 2: Create Render Account
- Go to https://render.com
- Sign up/login with GitHub

### Step 3: Create Web Service
1. Click **"New +"** → **"Web Service"**
2. Connect your GitHub repository
3. Select your repository

### Step 4: Configure Service
Use these exact settings:

| Setting | Value |
|---------|-------|
| **Name** | `emotivox-backend` (or your choice) |
| **Region** | Choose closest to you |
| **Branch** | `main` |
| **Root Directory** | `Backend` ⚠️ **IMPORTANT!** |
| **Runtime** | `Python 3` |
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `gunicorn app:app --bind 0.0.0.0:$PORT --timeout 300` |
| **Instance Type** | Free (for testing) |

### Step 5: Deploy
- Click **"Create Web Service"**
- Wait 15-30 minutes for first deployment (TTS model download)
- Your backend will be at: `https://your-service-name.onrender.com`

## 🔗 Connect to Netlify Frontend

### Step 1: Get Your Render URL
- Copy your Render service URL (e.g., `https://emotivox-backend.onrender.com`)

### Step 2: Update Netlify Environment Variable
1. Go to https://app.netlify.com
2. Select your site → **Site Settings** → **Environment Variables**
3. Add/Update: `VITE_API_URL` = `https://your-render-url.onrender.com`
4. **Redeploy** your Netlify site

## 🧪 Test Your Deployment

### Test Backend:
```bash
# Health check
curl https://your-service-name.onrender.com/health

# Should return: {"status": "healthy", "message": "Backend is running"}
```

### Test Frontend:
- Open your Netlify site
- Try the Voice Cloning feature
- Check browser console for any errors

## ⚠️ Important Notes

### Free Tier Limitations:
- **Cold starts**: Service sleeps after 15 min inactivity
- **First request**: Takes ~30 seconds after wake-up
- **Build time**: First deployment takes 15-30 min (model download)

### Performance Tips:
- Use `/health` endpoint periodically to keep service awake
- Consider upgrading to paid plan for better performance
- Monitor logs in Render dashboard

## 🐛 Troubleshooting

### Build Fails?
- Check Render logs for specific errors
- Verify `Backend/requirements.txt` syntax
- Ensure Root Directory is set to `Backend`

### CORS Errors?
- Backend already configured with `CORS(app, resources={r"/*": {"origins": "*"}})`
- Verify Netlify `VITE_API_URL` is correct

### Model Loading Issues?
- First load takes time (this is normal)
- Check Render logs for download progress
- Ensure sufficient disk space (free tier: 512MB)

### API Not Working?
- Verify Render service is running (green status)
- Check Netlify environment variable is set correctly
- Look at browser console for API errors

## 📚 Additional Resources

- Full deployment guide: `Backend/DEPLOYMENT.md`
- Netlify setup: `NETLIFY_SETUP.md`
- Render docs: https://render.com/docs

## ✨ Next Steps

1. ✅ Deploy to Render
2. ✅ Update Netlify environment variable
3. ✅ Test the integration
4. 🎉 Enjoy your deployed app!

---

**Need help?** Check the logs in Render dashboard or the detailed guides mentioned above.

