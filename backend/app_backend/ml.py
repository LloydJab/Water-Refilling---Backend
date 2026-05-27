import pandas as pd
import numpy as np
from sklearn.linear_model import SGDRegressor
import joblib
from app_backend.models import Order
import os
from django.conf import settings

MODEL_PATH = os.path.join(settings.BASE_DIR, "app_backend", "sales_model.pkl")

def initialize_model():
    """Initialize a fresh incremental model."""
    model = SGDRegressor(max_iter=1000, tol=1e-3)
    joblib.dump(model, MODEL_PATH)
    return model

def update_model_with_order(order):
    print(f"Updating ML model with order {order.id}, amount={order.totalAmount}")
    try:
        model = joblib.load(MODEL_PATH)
    except FileNotFoundError:
        model = initialize_model()

    # Feature engineering
    parsed_date = pd.to_datetime(order.date, format='%m/%d/%Y')
    day_of_week = parsed_date.dayofweek
    day_of_month = parsed_date.day
    month = parsed_date.month
    is_weekend = 1 if day_of_week >= 5 else 0
    order_type_encoded = 1 if order.orderType == 'delivery' else 0

    X = np.array([[day_of_week, day_of_month, month, is_weekend, order_type_encoded]])
    y = np.array([order.totalAmount])

    model.partial_fit(X, y)
    joblib.dump(model, MODEL_PATH)

def update_model_with_batch(orders):
    try:
        model = joblib.load(MODEL_PATH)
    except FileNotFoundError:
        model = initialize_model()

    df = pd.DataFrame(list(orders.values('date','totalAmount','orderType')))
    df['parsed_date'] = pd.to_datetime(df['date'], format='%m/%d/%Y')
    df['day_of_week'] = df['parsed_date'].dt.dayofweek
    df['day_of_month'] = df['parsed_date'].dt.day
    df['month'] = df['parsed_date'].dt.month
    df['is_weekend'] = df['day_of_week'].apply(lambda x: 1 if x >= 5 else 0)
    df['order_type_encoded'] = df['orderType'].apply(lambda x: 1 if x == 'delivery' else 0)

    X = df[['day_of_week','day_of_month','month','is_weekend','order_type_encoded']].values
    y = df['totalAmount'].values

    model.partial_fit(X, y)
    joblib.dump(model, MODEL_PATH)