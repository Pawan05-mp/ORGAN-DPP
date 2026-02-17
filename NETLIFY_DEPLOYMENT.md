# ORGAN-DPP Netlify Deployment Guide

## Prerequisites

1. **Netlify Account** - Sign up at [netlify.com](https://netlify.com)
2. **GitHub Repository** - Project must be pushed to GitHub (✅ Already done!)
3. **Git** - Version control (✅ Already installed!)

## Deployment Steps

### Step 1: Connect GitHub to Netlify

1. Go to [netlify.com/app](https://netlify.com/app)
2. Click **"New site from Git"**
3. Choose **GitHub** as your Git provider
4. Authorize Netlify to access your GitHub account
5. Select the **`organdpp`** repository

### Step 2: Configure Build Settings

When prompted, use these settings:

- **Base directory**: `frontend`
- **Build command**: `npm run build`
- **Publish directory**: `.next`

These are already configured in `netlify.toml`, so they should auto-populate.

### Step 3: Deploy

1. Click **"Deploy"**
2. Netlify will automatically:
   - Install dependencies
   - Build the Next.js frontend
   - Deploy Netlify Functions for the API
   - Set up HTTPS and DNS

### Step 4: View Your Site

Once deployed, you'll get a URL like:
```
https://organdpp-[random].netlify.app
```

## Project Structure for Netlify

```
organ-dpp/
├── frontend/              # Next.js frontend (published)
│   ├── src/
│   ├── package.json
│   └── ...
├── netlify/
│   └── functions/
│       └── generate.ts   # Serverless API endpoint
├── netlify.toml          # Netlify configuration
└── README.md
```

## API Endpoints

### Local Development
- Backend: `http://127.0.0.1:8000`
- Frontend: `http://localhost:3000`

### Netlify Production
- Frontend: `https://yourdomain.netlify.app`
- API: `https://yourdomain.netlify.app/.netlify/functions/generate`

The frontend automatically detects environment and uses the correct API endpoint.

## Current Features

✅ **Frontend Deployed**
- Next.js 16 with TypeScript
- Tailwind CSS styling
- Interactive UI for molecule generation
- Real-time results display

✅ **Backend API**
- Netlify Functions for serverless computation
- Mock molecular generation (ready for real ML models)
- Full CORS support
- Batch generation with configurable parameters

## Next Steps (Production Enhancements)

1. **Connect Real ML Models**
   - Replace mock generation with actual LSTM/CNN models
   - Use TensorFlow.js or WebAssembly for in-browser inference
   - Or call external ML services from Netlify Functions

2. **Add Environment Variables**
   - Create `.env.production` for production settings
   - Manage secrets in Netlify dashboard

3. **Enable Analytics**
   - Netlify Analytics for site performance
   - Monitor function execution times

4. **Set Custom Domain**
   - In Netlify dashboard → Domain settings
   - Add your custom domain

## Troubleshooting

### Build fails with "npm not found"
- Netlify uses Node.js 16 by default
- We've set `NODE_VERSION = "24"` in `netlify.toml`

### Functions not working
- Check `netlify/functions/` directory exists
- Verify `netlify.toml` configuration
- Check Netlify build logs for errors

### API calls failing
- Ensure `process.env.NODE_ENV` is properly set
- Check browser console for CORS errors
- Verify Netlify Functions deployment status

## Environment Variables

Add these in Netlify Dashboard → Site Settings → Build & Deploy → Environment:

```
NODE_VERSION=24
NEXT_SKIP_ENV_VALIDATION=true
```

## Support

- [Netlify Documentation](https://docs.netlify.com)
- [Next.js on Netlify](https://docs.netlify.com/integrations/frameworks/next-js)
- [Netlify Functions](https://docs.netlify.com/functions/overview)
