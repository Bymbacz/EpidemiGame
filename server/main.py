from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from server.api import router as api_router
from server.websocket import router as ws_router

app = FastAPI()

# 1. Zdefiniuj dozwolone originy
origins = [
    "http://localhost:5173",  # Twój frontend
    "http://127.0.0.1:5173"   # Alternatywny adres
]

# 2. Dodaj middleware CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,            # lub ["*"] dla developmentu
    allow_credentials=True,           # jeśli używasz ciastek/autoryzacji
    allow_methods=["*"],              # GET, POST, OPTIONS itd.
    allow_headers=["*"],              # Content-Type, Authorization itd.
    expose_headers=["*"],             # jeśli chcesz ujawnić nagłówki w odpowiedzi
    max_age=600                       # cache preflight na 10 minut
)

# 3. Zarejestruj routery
app.include_router(api_router)
app.include_router(ws_router)
