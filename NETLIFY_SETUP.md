# Netlify Deployment Setup for React Frontend

## Environment Variable Configuration

Since your React app is already deployed on Netlify, you need to update the environment variable to point to your Render backend.

### Steps:

1. **Go to Netlify Dashboard**
   - Visit https://app.netlify.com
   - Select your deployed site

2. **Add Environment Variable**
   - Click on **Site Settings** → **Environment Variables**
   - Click **Add a variable**
   - Add the following:
     - **Key**: `VITE_API_URL`
     - **Value**: `https://your-backend-name.onrender.com` (replace with your actual Render URL)
   - Click **Save**

3. **Redeploy Your Site**
   - Go to **Deploys** tab
   - Click **Trigger deploy** → **Deploy site**
   - Or push a new commit to trigger automatic deployment

### For Local Development

Create a `.env.local` file in your project root:

```
VITE_API_URL=http://127.0.0.1:5000
```

**Note**: This file is already in `.gitignore` so it won't be committed.

### Verify Configuration

After redeploying, check the browser console to ensure API calls are going to the correct backend URL.

## Build Settings (if not already configured)

Your Netlify build settings should be:
- **Build command**: `npm run build`
- **Publish directory**: `dist`
- **Node version**: `18.x` or `20.x`

