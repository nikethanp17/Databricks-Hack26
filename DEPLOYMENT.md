# 🚀 Deployment Guide

## Quick Deploy to GitHub

### Option 1: Automated Script (Recommended)

1. **Download all files** from Databricks workspace:
   ```
   /Workspace/Users/nikethanp17@gmail.com/Databricks-Hack26/
   ```

2. **Run the deployment script**:
   ```bash
   cd Databricks-Hack26
   chmod +x deploy.sh
   ./deploy.sh
   ```

3. **Enter your GitHub credentials** when prompted (use Personal Access Token if 2FA is enabled)

### Option 2: Manual Push

```bash
# Navigate to project directory
cd Databricks-Hack26

# Initialize git
git init
git branch -M main

# Configure git
git config user.name "nikethanp17"
git config user.email "nikethanp17@gmail.com"

# Add files
git add .

# Commit
git commit -m "Initial commit: Kirana Supply Chain Optimizer"

# Add remote
git remote add origin https://github.com/nikethanp17/Databricks-Hack26.git

# Push
git push -u origin main
```

## Deploy Frontend to GitHub Pages

1. **Go to your repository** on GitHub

2. **Navigate to Settings → Pages**

3. **Configure Source**:
   - Source: Deploy from a branch
   - Branch: `main`
   - Folder: `/ (root)`

4. **Save** and wait ~1 minute

5. **Access your site**:
   ```
   https://nikethanp17.github.io/Databricks-Hack26/frontend/login.html
   ```

## Deploy Backend API

### Option 1: Render.com (Free)

1. **Create account** at [render.com](https://render.com)

2. **New Web Service** → Connect GitHub repo

3. **Configure**:
   - Name: `kirana-api`
   - Root Directory: `backend`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn app:app --host 0.0.0.0 --port $PORT`

4. **Deploy** - Get your API URL

5. **Update frontend** `dashboard.html` line 127:
   ```javascript
   const API_URL = 'https://kirana-api.onrender.com/predict';
   ```

### Option 2: Railway.app (Free)

1. **Create account** at [railway.app](https://railway.app)

2. **New Project** → Deploy from GitHub

3. **Select** your repository

4. **Configure**:
   - Root Directory: `/backend`
   - Start Command: `python app.py`

5. **Get URL** and update frontend

### Option 3: Heroku

```bash
# Install Heroku CLI
brew install heroku/brew/heroku  # macOS
# or download from heroku.com

# Login
heroku login

# Create app
cd backend
heroku create kirana-optimizer

# Deploy
git push heroku main

# Get URL
heroku open
```

### Option 4: AWS Lambda + API Gateway

1. **Install SAM CLI**

2. **Create `template.yaml`** in backend/:
   ```yaml
   AWSTemplateFormatVersion: '2010-09-09'
   Transform: AWS::Serverless-2016-10-31
   
   Resources:
     KiranaAPI:
       Type: AWS::Serverless::Function
       Properties:
         Handler: app.handler
         Runtime: python3.9
         Events:
           Predict:
             Type: Api
             Properties:
               Path: /predict
               Method: post
   ```

3. **Deploy**:
   ```bash
   sam build
   sam deploy --guided
   ```

## Deploy Full Stack on Vercel

1. **Install Vercel CLI**:
   ```bash
   npm install -g vercel
   ```

2. **Deploy**:
   ```bash
   cd Databricks-Hack26
   vercel
   ```

3. **Configure**:
   - Build Command: (leave empty for static)
   - Output Directory: `frontend`

4. **For backend**, create `vercel.json`:
   ```json
   {
     "functions": {
       "backend/app.py": {
         "runtime": "python3.9"
       }
     },
     "routes": [
       { "src": "/api/(.*)", "dest": "backend/app.py" },
       { "src": "/(.*)", "dest": "frontend/$1" }
     ]
   }
   ```

## Environment Variables

For production deployment, add these environment variables:

```bash
# Backend
ENVIRONMENT=production
API_KEY=your-secret-key
CORS_ORIGINS=https://nikethanp17.github.io

# Frontend (update in dashboard.html)
API_URL=https://your-backend-url.com/predict
```

## Testing Deployment

### Test Backend
```bash
curl -X POST "https://your-backend-url/predict" \
  -H "Content-Type: application/json" \
  -d '{"product": "milk", "day_type": "weekend", "time_slot": "evening", "inventory": 20}'
```

### Test Frontend
1. Open: `https://nikethanp17.github.io/Databricks-Hack26/frontend/login.html`
2. Login: admin / 1234
3. Navigate to dashboard
4. Make a prediction

## Troubleshooting

### CORS Errors
Update `backend/app.py`:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://nikethanp17.github.io"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### API Connection Failed
1. Check backend URL in `frontend/dashboard.html`
2. Verify backend is running: `curl https://your-backend/`
3. Check browser console for errors

### GitHub Pages 404
1. Ensure `index.html` exists or use full path
2. Wait 1-2 minutes after enabling Pages
3. Check Settings → Pages for deployment status

## Production Checklist

- [ ] Push code to GitHub
- [ ] Enable GitHub Pages
- [ ] Deploy backend to hosting service
- [ ] Update frontend with backend URL
- [ ] Test end-to-end flow
- [ ] Set up custom domain (optional)
- [ ] Add SSL certificate
- [ ] Configure monitoring (Sentry, LogRocket)
- [ ] Set up CI/CD pipeline
- [ ] Add API rate limiting
- [ ] Implement proper authentication
- [ ] Add analytics (Google Analytics)

## Custom Domain (Optional)

1. **Buy domain** (Namecheap, GoDaddy, Google Domains)

2. **Add CNAME record**:
   ```
   Type: CNAME
   Host: www
   Value: nikethanp17.github.io
   ```

3. **Configure in GitHub**:
   - Settings → Pages → Custom domain
   - Enter: `www.yourdomain.com`
   - Enable HTTPS

## Monitoring & Analytics

### Add Google Analytics
In `frontend/dashboard.html`:
```html
<!-- Google Analytics -->
<script async src="https://www.googletagmanager.com/gtag/js?id=GA_MEASUREMENT_ID"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'GA_MEASUREMENT_ID');
</script>
```

### Add Error Tracking (Sentry)
```bash
pip install sentry-sdk[fastapi]
```

In `backend/app.py`:
```python
import sentry_sdk
sentry_sdk.init(dsn="YOUR_SENTRY_DSN")
```

## Cost Estimate

 Service | Tier | Cost |
---------|------|------|
 GitHub Pages | Free | $0/month |
 Render.com | Free | $0/month |
 Railway.app | Starter | $5/month |
 Heroku | Hobby | $7/month |
 AWS Lambda | Free Tier | ~$0-5/month |
 Vercel | Free | $0/month |
 Custom Domain | Varies | ~$12/year |

## Support

For issues or questions:
- GitHub Issues: https://github.com/nikethanp17/Databricks-Hack26/issues
- Email: nikethanp17@gmail.com

---

Made with ❤️ for Databricks Hackathon 2026
