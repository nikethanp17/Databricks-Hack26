from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import random

# Initialize FastAPI app
app = FastAPI(title="Kirana Store Demand Predictor")

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class PredictionRequest(BaseModel):
    product: str
    day_type: str
    time_slot: str
    inventory: int

class PredictionResponse(BaseModel):
    predicted_demand: float
    restock: int
    explanation: str

# Product base demands
BASE_DEMANDS = {
    'milk': 40, 'bread': 30, 'rice': 25, 'eggs': 35, 'flour': 20,
    'sugar': 15, 'tea': 20, 'biscuits': 25, 'oil': 18, 'salt': 12
}

def predict_demand(product, day_type, time_slot):
    """Simple rule-based prediction for demo"""
    base = BASE_DEMANDS.get(product, 20)
    
    # Weekend multiplier
    if day_type == 'weekend':
        base *= random.uniform(1.2, 1.4)
    
    # Time slot multiplier
    if time_slot == 'evening':
        base *= random.uniform(1.2, 1.5)
    elif time_slot == 'afternoon':
        base *= random.uniform(0.9, 1.1)
    else:  # morning
        base *= random.uniform(0.8, 1.0)
    
    # Add noise
    base *= random.uniform(0.85, 1.15)
    
    return round(base, 1)

def generate_explanation(product, day_type, time_slot, predicted_demand, inventory, restock):
    """Generate explanation for the prediction"""
    parts = []
    parts.append(f"Predicted demand for {product} is {predicted_demand:.1f} units.")
    
    if day_type == 'weekend':
        parts.append("Demand is typically 20-40% higher on weekends due to increased customer traffic.")
    else:
        parts.append("This is a regular weekday with standard traffic patterns.")
    
    if time_slot == 'evening':
        parts.append("Evening hours (5-9 PM) see peak demand as customers shop after work.")
    elif time_slot == 'afternoon':
        parts.append("Afternoon hours show moderate demand with steady customer flow.")
    else:
        parts.append("Morning hours typically have lower demand with fresh stock purchases.")
    
    if restock > 0:
        buffer = int(predicted_demand * 0.2)
        parts.append(
            f"With current inventory of {inventory} units, we recommend restocking {restock} units "
            f"to meet predicted demand plus a {buffer}-unit safety buffer (20%)."
        )
    else:
        parts.append(
            f"Current inventory of {inventory} units is sufficient to meet predicted demand. "
            "No immediate restocking needed."
        )
    
    return " ".join(parts)

@app.post("/predict", response_model=PredictionResponse)
async def predict(request: PredictionRequest):
    """Predict demand and generate restock recommendation"""
    
    # Predict demand
    predicted_demand = predict_demand(
        request.product,
        request.day_type,
        request.time_slot
    )
    
    # Calculate restock
    restock = max(int((predicted_demand * 1.2) - request.inventory), 0)
    
    # Generate explanation
    explanation = generate_explanation(
        request.product,
        request.day_type,
        request.time_slot,
        predicted_demand,
        request.inventory,
        restock
    )
    
    return PredictionResponse(
        predicted_demand=predicted_demand,
        restock=restock,
        explanation=explanation
    )

@app.get("/")
async def root():
    return {"message": "Kirana Store Demand Predictor API", "status": "running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
