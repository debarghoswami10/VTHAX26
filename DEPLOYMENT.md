# 🚀 Vercel Deployment Guide

## Prerequisites
1. **Vercel Account**: Sign up at [vercel.com](https://vercel.com)
2. **GitHub Repository**: Your code should be pushed to GitHub
3. **Node.js**: Install from [nodejs.org](https://nodejs.org)

## Step 1: Install Vercel CLI
```bash
npm i -g vercel
```

## Step 2: Login to Vercel
```bash
vercel login
```

## Step 3: Deploy from your project directory
```bash
cd /Users/ashwinnimmala/test/VTHAX26
vercel
```

## Step 4: Follow the prompts
- **Set up and deploy?** → Yes
- **Which scope?** → Your account
- **Link to existing project?** → No
- **What's your project's name?** → woke-ai-platform (or your choice)
- **In which directory is your code located?** → ./

## Step 5: Set Environment Variables
In your Vercel dashboard:
1. Go to your project settings
2. Navigate to "Environment Variables"
3. Add these variables:
   - `SUPABASE_URL`: `https://civjbgjrknhaknietyth.supabase.co`
   - `SUPABASE_KEY`: `sb_secret_HEvjYo69xYMQ6dfBDKdz-A_sNx3CAKQ`

## Step 6: Redeploy
After setting environment variables:
```bash
vercel --prod
```

## 🌐 Your Live URLs
- **Main App**: `https://your-project-name.vercel.app`
- **API**: `https://your-project-name.vercel.app/api/`
- **Frontend**: `https://your-project-name.vercel.app/static/`

## 📁 Project Structure for Vercel
```
VTHAX26/
├── api/
│   └── index.py          # Vercel API handler
├── backend/
│   └── main.py           # FastAPI app
├── frontend/             # Static files
├── vercel.json           # Vercel configuration
├── requirements.txt      # Python dependencies
└── package.json         # Node.js dependencies
```

## 🔧 Troubleshooting

### If deployment fails:
1. Check that all files are committed to Git
2. Ensure environment variables are set correctly
3. Check the Vercel function logs in the dashboard

### If API calls fail:
1. Verify CORS settings in `main.py`
2. Check that Supabase credentials are correct
3. Ensure all endpoints are properly defined

## 🎉 Success!
Once deployed, your app will be live at the provided Vercel URL!
