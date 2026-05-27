# Water Refilling POS — Backend

Django REST Framework backend with JWT auth, WebSocket support, and ML sales forecasting.

## Stack
- Django 6 + Django REST Framework
- Django Channels (WebSocket)
- JWT Authentication (SimpleJWT)
- scikit-learn (SGDRegressor — 7-day revenue forecast)
- SQLite (dev) / PostgreSQL (prod)

## Team Members
- [your names here]

## Quickstart

git clone https://github.com/LloydJab/Water-Refilling---Backend.git
cd Water-Refilling---Backend/backend
python -m venv .venv
.venv\Scripts\activate        # Windows
pip install -r requirements.txt
python manage.py migrate
daphne -p 8000 backend.asgi:application

## API Endpoints
| Endpoint | Method | Description |
|---|---|---|
| /api/orders/ | GET, POST | Orders |
| /api/products/ | GET | Products |
| /api/maintenance/ | GET | Maintenance status |
| /api/predictions/ | GET | ML sales forecast |
| /api/token/ | POST | JWT login |

## WebSocket
ws://localhost:8000/ws/dashboard/
Broadcasts new_order events to all connected clients.

## Environment Variables
Create a .env file (never commit it):
SECRET_KEY=your-secret-key
DEBUG=False
ALLOWED_HOSTS=your-domain.com
