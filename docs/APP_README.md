# 🏪 Kirana Supply Chain Optimizer - Hackathon MVP

AI-powered demand prediction and inventory optimization system for Kirana stores.

## 🚀 Features

✅ **Login System** - Secure authentication with session management  
✅ **Animated Landing Page** - Beautiful intro with typewriter effects  
✅ **AI Predictions** - Real-time demand forecasting  
✅ **Smart Restocking** - Intelligent inventory recommendations  
✅ **Responsive Design** - Modern, clean UI with smooth animations

---

## 📁 Project Structure

```
kirana-app/
├── login.html          # Authentication page
├── landing.html        # Animated landing/intro page
├── dashboard.html      # Main application dashboard
├── app.py              # FastAPI backend
├── requirements.txt    # Python dependencies
└── README.md           # This file
```

---

## 🔧 Setup & Installation

### **Step 1: Install Dependencies**

```bash
cd kirana-app
pip install -r requirements.txt
```

### **Step 2: Start the Backend Server**

```bash
python app.py
```

You should see:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
```

Keep this terminal running!

---

## 🌐 Running the Application

### **Option 1: Direct File Opening (Recommended)**

1. Navigate to the `kirana-app` folder
2. Double-click `login.html` to open in your browser
3. Or right-click → "Open with" → Your browser

### **Option 2: Using a Local Server**

```bash
# In a NEW terminal (keep backend running)
cd kirana-app
python -m http.server 8080
```

Then open: `http://localhost:8080/login.html`

---

## 🔐 Demo Credentials

**Username:** `admin`  
**Password:** `1234`

---

## 🎯 How to Use

### **Step 1: Login**
- Open `login.html`
- Enter credentials: `admin` / `1234`
- Click "Login"

### **Step 2: Landing Page**
- Watch the animated introduction
- See the typewriter effect for the tagline
- Click "Enter Dashboard →"

### **Step 3: Dashboard**
- Select a product (milk, bread, rice, etc.)
- Choose day type (weekday/weekend)
- Select time slot (morning/afternoon/evening)
- Enter current inventory
- Click "Get Prediction"

### **Step 4: View Results**
- Predicted demand
- Restock recommendation
- AI-generated explanation

### **Step 5: Logout**
- Click "Logout" button in top-right
- Returns to login page

---

## 📊 Test Scenarios

### **Scenario 1: High Demand Evening**
- Product: Milk
- Day: Weekend
- Time: Evening
- Inventory: 20
- Expected: ~55-60 units demand

### **Scenario 2: Low Demand Morning**
- Product: Salt
- Day: Weekday
- Time: Morning
- Inventory: 30
- Expected: ~10-12 units demand

### **Scenario 3: Sufficient Stock**
- Product: Any
- Day: Any
- Time: Any
- Inventory: 100
- Expected: 0 restock needed

---

## 🎨 Features Breakdown

### **1. Login System**
- Hardcoded authentication (admin/1234)
- Session management with localStorage
- Auto-redirect if already logged in
- Error handling with shake animation

### **2. Landing Page**
- Full-screen animated introduction
- Typewriter effect for tagline
- Floating icon animations
- Fade-in transitions
- Smooth page transition to dashboard

### **3. Dashboard**
- Clean, modern interface
- Real-time API integration
- Loading spinner during predictions
- Animated result display
- Logout functionality

### **4. Backend API**
- FastAPI framework
- CORS enabled for frontend
- Rule-based prediction logic
- JSON request/response
- Health check endpoint

---

## 🔄 Application Flow

```
login.html 
    ↓ (authenticate)
landing.html 
    ↓ (enter dashboard)
dashboard.html 
    ↓ (make prediction)
API (app.py) 
    ↓ (return results)
dashboard.html 
    ↓ (display results)
```

---

## 🛠️ Tech Stack

- **Frontend:** HTML5, CSS3, JavaScript (Vanilla)
- **Backend:** FastAPI, Python
- **Storage:** localStorage (session management)
- **Styling:** Custom CSS with animations
- **API:** RESTful JSON endpoints

---

## 📡 API Endpoints

### **POST /predict**
Predict demand and generate restock recommendation

**Request:**
```json
{
  "product": "milk",
  "day_type": "weekend",
  "time_slot": "evening",
  "inventory": 20
}
```

**Response:**
```json
{
  "predicted_demand": 58.2,
  "restock": 49,
  "explanation": "Predicted demand for milk is 58.2 units..."
}
```

### **GET /**
Health check endpoint

**Response:**
```json
{
  "message": "Kirana Store Demand Predictor API",
  "status": "running"
}
```

---

## 🎨 Animations & Effects

1. **Fade In/Up** - Smooth element appearance
2. **Typewriter** - Text typing animation
3. **Float** - Floating icon effect
4. **Shake** - Error message animation
5. **Fade Out** - Smooth page transitions
6. **Spinner** - Loading animation

---

## 🐛 Troubleshooting

### **API Connection Error**
- Make sure `app.py` is running
- Check if port 8000 is available
- Verify CORS is enabled

### **Login Not Working**
- Clear browser localStorage
- Check console for errors
- Verify credentials: admin/1234

### **Page Not Redirecting**
- Clear browser cache
- Check if localStorage is enabled
- Try incognito mode

---

## 🚀 Deployment Options

### **Local Demo (Current Setup)**
- Open HTML files directly
- Run backend locally
- Perfect for hackathons

### **Production Deployment**
- Deploy backend to Heroku/AWS/Azure
- Host frontend on Netlify/Vercel
- Use environment variables
- Add database for real authentication

---

## 📝 Future Enhancements

- Real ML model integration (Spark MLlib)
- Database for user management
- Historical data tracking
- Multi-store dashboard
- Mobile app
- Advanced analytics
- Report generation

---

## 👥 Credits

Built for **Databricks Hackathon 2026**  
Project: Hyper-Local Supply Chain Optimizer for Kirana Stores

---

## 📄 License

MIT License - Feel free to use for your hackathon!

---

## 🎉 Enjoy the Demo!

For questions or issues, check the console logs in your browser (F12).
