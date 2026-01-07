from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from telethon import TelegramClient
import asyncio
import json

app = FastAPI()

# Разрешаем запросы отовсюду
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Простейший Telegram клиент
client = None

@app.on_event("startup")
async def startup():
    """Простая инициализация"""
    global client
    client = TelegramClient("session", 123456, "your_api_hash_here")  # Вставьте свои данные
    await client.start()
    print("✅ Telegram подключен")

@app.get("/")
async def root():
    """Главная страница - отдаем HTML"""
    with open("index.html", "r") as f:
        return HTMLResponse(f.read())

@app.get("/api/user/{username}")
async def get_user(username: str):
    """Получить информацию о пользователе"""
    try:
        user = await client.get_entity(username)
        return {
            "id": user.id,
            "username": user.username,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "is_bot": user.bot
        }
    except Exception as e:
        return {"error": str(e)}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """Простой WebSocket"""
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        await websocket.send_text(f"Получено: {data}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
