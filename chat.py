from fastapi import FastAPI, WebSocket
import redis
import json

app = FastAPI()
redis_client = redis.Redis(host='localhost', port=6379, db=0)

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        redis_client.publish('chat_channel', data)
        await websocket.send_text(f"Message text was: {data}")

@app.on_event("startup")
async def startup():
    pubsub = redis_client.pubsub()
    pubsub.subscribe('chat_channel')
    async def listen_to_channel():
        for message in pubsub.listen():
            if message['type'] == 'message':
                await websocket.send_text(message['data'])
    await listen_to_channel()
