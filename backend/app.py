from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, field_validator
import random

# ── App init ─────────────────────────────────────────────────────────────────
app = FastAPI(
    title="Kirana Store Demand Predictor",
    description="AI-powered demand forecasting for Kirana stores",
    version="2.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Schemas ───────────────────────────────────────────────────────────────────
VALID_PRODUCTS   = {'milk','bread','rice','eggs','flour','sugar','tea','biscuits','oil','salt'}
VALID_DAY_TYPES  = {'weekday', 'weekend'}
VALID_TIME_SLOTS = {'morning', 'afternoon', 'evening'}

class PredictionRequest(BaseModel):
    product:   str = Field(..., description="Product name")
    day_type:  str = Field(..., description="weekday or weekend")
    time_slot: str = Field(..., description="morning, afternoon, or evening")
    inventory: int = Field(..., ge=0, description="Current stock (non-negative)")

    @field_validator('product')
    @classmethod
    def validate_product(cls, v):
        v = v.lower().strip()
        if v not in VALID_PRODUCTS:
            raise ValueError(f"Invalid product '{v}'. Choose from: {', '.join(sorted(VALID_PRODUCTS))}")
        return v

    @field_validator('day_type')
    @classmethod
    def validate_day_type(cls, v):
        v = v.lower().strip()
        if v not in VALID_DAY_TYPES:
            raise ValueError("day_type must be 'weekday' or 'weekend'")
        return v

    @field_validator('time_slot')
    @classmethod
    def validate_time_slot(cls, v):
        v = v.lower().strip()
        if v not in VALID_TIME_SLOTS:
            raise ValueError("time_slot must be 'morning', 'afternoon', or 'evening'")
        return v

class PredictionResponse(BaseModel):
    predicted_demand: float
    restock: int
    explanation: str

# ── Prediction Logic (unchanged ML rules) ─────────────────────────────────────
BASE_DEMANDS = {
    'milk': 40, 'bread': 30, 'rice': 25, 'eggs': 35, 'flour': 20,
    'sugar': 15, 'tea': 20, 'biscuits': 25, 'oil': 18, 'salt': 12
}

def predict_demand(product: str, day_type: str, time_slot: str) -> float:
    base = BASE_DEMANDS.get(product, 20)
    if day_type == 'weekend':
        base *= random.uniform(1.2, 1.4)
    if time_slot == 'evening':
        base *= random.uniform(1.2, 1.5)
    elif time_slot == 'afternoon':
        base *= random.uniform(0.9, 1.1)
    else:  # morning
        base *= random.uniform(0.8, 1.0)
    base *= random.uniform(0.85, 1.15)
    return round(base, 1)

# ── Feature 4 — Smart Explanation Logic ───────────────────────────────────────
PRODUCT_CONTEXT = {
    'milk':     "a high-frequency perishable",
    'bread':    "a daily staple with consistent demand",
    'rice':     "a bulk purchase item",
    'eggs':     "a breakfast essential with steady daily demand",
    'flour':    "a weekend baking staple",
    'sugar':    "a slow-moving commodity",
    'tea':      "a morning-heavy beverage",
    'biscuits': "a snack with impulse purchase patterns",
    'oil':      "a bulk-buy item replenished less frequently",
    'salt':     "a very slow-moving commodity"
}

def generate_explanation(
    product: str,
    day_type: str,
    time_slot: str,
    predicted_demand: float,
    inventory: int,
    restock: int
) -> str:
    parts = []
    ctx = PRODUCT_CONTEXT.get(product, "a common grocery item")
    product_display = product.capitalize()

    # 1. Product + demand opening
    parts.append(
        f"{product_display} is {ctx}. "
        f"Predicted demand is {predicted_demand:.1f} units."
    )

    # 2. Day-type reasoning
    if day_type == 'weekend':
        parts.append(
            f"Weekend shopping typically drives 20–40% higher footfall, "
            f"boosting {product_display.lower()} demand significantly."
        )
    else:
        parts.append("Weekday demand follows standard traffic patterns.")

    # 3. Time-slot reasoning
    if time_slot == 'evening':
        parts.append(
            "Evening hours (5–10 PM) are peak shopping time as customers "
            "return from work, pushing demand to its daily high."
        )
    elif time_slot == 'afternoon':
        parts.append(
            "Afternoon hours see moderate, steady demand with regular "
            "customer flow throughout the day."
        )
    else:
        parts.append(
            "Morning hours typically see lower demand, ideal for "
            "restocking shelves before the afternoon rush."
        )

    # 4. Inventory / restock reasoning
    safety_buffer = int(predicted_demand * 0.2)
    if restock > 0:
        stock_pct = (inventory / predicted_demand * 100) if predicted_demand else 0
        risk = "critically low" if stock_pct < 40 else "insufficient"
        parts.append(
            f"⚠️ Current inventory ({inventory} units) is {risk} to meet "
            f"predicted demand. Recommend ordering {restock} units to cover "
            f"demand plus a {safety_buffer}-unit safety buffer (20%)."
        )
    else:
        surplus = inventory - int(predicted_demand * 1.2)
        parts.append(
            f"✅ Current inventory ({inventory} units) comfortably covers "
            f"predicted demand with a surplus of ~{surplus} units. "
            "No restocking needed at this time."
        )

    return " ".join(parts)

# ── Endpoints ─────────────────────────────────────────────────────────────────
@app.post("/predict", response_model=PredictionResponse)
async def predict(request: PredictionRequest):
    """Predict demand and generate smart restock recommendation."""
    predicted_demand = predict_demand(request.product, request.day_type, request.time_slot)
    restock = max(int((predicted_demand * 1.2) - request.inventory), 0)
    explanation = generate_explanation(
        request.product, request.day_type, request.time_slot,
        predicted_demand, request.inventory, restock
    )
    return PredictionResponse(
        predicted_demand=predicted_demand,
        restock=restock,
        explanation=explanation
    )

@app.get("/")
async def root():
    return {"message": "Kirana Store Demand Predictor API v2", "status": "running"}

@app.get("/health")
async def health():
    return {"status": "ok", "version": "2.0.0"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
