# ⚡ Quick Start Guide

## 🎯 Goal
Get your Kirana Supply Chain Optimizer running in 5 minutes!

## Step 1: Download Project (1 min)

Download all files from Databricks:
```
/Workspace/Users/nikethanp17@gmail.com/Databricks-Hack26/
```

## Step 2: Push to GitHub (2 min)

```bash
cd Databricks-Hack26
chmod +x deploy.sh
./deploy.sh
```

Enter your GitHub credentials when prompted.

## Step 3: Test Locally (2 min)

### Terminal 1 - Backend:
```bash
cd backend
pip install -r requirements.txt
python app.py
```

### Terminal 2 - Frontend:
```bash
cd frontend
open login.html
```

### Or use Python server:
```bash
cd frontend
python -m http.server 8080
# Visit: http://localhost:8080/login.html
```

## Login Credentials
- Username: `admin`
- Password: `1234`

## Test Prediction

1. Product: **Milk**
2. Day Type: **Weekend**
3. Time Slot: **Evening**
4. Inventory: **20**

Expected Result: ~58 units demand, ~49 units restock

## 🌐 Deploy Online (Optional)

### GitHub Pages (Frontend - Free):
1. Go to repo Settings → Pages
2. Source: main branch
3. Visit: `https://nikethanp17.github.io/Databricks-Hack26/frontend/login.html`

### Render.com (Backend - Free):
1. Sign up at [render.com](https://render.com)
2. New Web Service → Connect GitHub
3. Root Directory: `backend`
4. Build: `pip install -r requirements.txt`
5. Start: `uvicorn app:app --host 0.0.0.0 --port $PORT`
6. Update API URL in `frontend/dashboard.html` line 127

## 📊 Project Stats

- **ML Accuracy:** 89.7% (R² Score: 0.897)
- **Training Data:** 800 rows
- **API Response Time:** <100ms
- **Files:** 12 total
- **Lines of Code:** ~1,500

## 🎥 Demo Flow

1. Login Page → Enter credentials
2. Landing Page → Animated intro (3 sec)
3. Dashboard → Make prediction
4. Results → View demand + restock + explanation

## ❓ Troubleshooting

**Backend won't start?**
```bash
pip install --upgrade pip
pip install -r requirements.txt --force-reinstall
```

**Frontend can't connect to API?**
- Check backend is running on port 8000
- Verify `http://localhost:8000/` returns API status
- Check browser console for CORS errors

**Login not working?**
- Clear browser cache (Cmd+Shift+R / Ctrl+Shift+R)
- Check credentials: admin / 1234
- Open browser console for errors

## 📚 More Help

- Full README: `README.md`
- Deployment Guide: `DEPLOYMENT.md`
- App Documentation: `docs/APP_README.md`

---

**Need Help?** Open an issue on GitHub!

🎉 **Happy Hacking!**
