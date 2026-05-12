# Main Entry
import json
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.config import config
from app.handlers.feishu import feishu_handler


@asynccontextmanager
async def lifespan(app: FastAPI):
    print(f"Bot starting on port {config.SERVER_PORT}")
    yield
    print("Bot shutting down")


app = FastAPI(title="Workplace Mouthpiece", version="1.0.0", lifespan=lifespan)


@app.get("/")
async def root():
    return {"status": "ok", "message": "Workplace Mouthpiece Bot"}


@app.get("/health")
async def health():
    return {"status": "healthy"}

@app.post("/")
async def webhook(request: Request):
    """飞书事件订阅入口 - 处理消息事件和卡片回调"""
    try:
        body = await request.body()
        event = json.loads(body)
        
        if event.get("type") == "url_verification":
            return {"challenge": event.get("challenge")}
        
        # 检测是否为卡片回调（飞书可能把回调发到 / 而不是 /callback）
                if event.get("action"):
            card = await feishu_handler.handle_card_callback(event)
            if card:
                return JSONResponse(content=card)
            return JSONResponse(content={})
        
        # Handle message event
        result = await feishu_handler.handle_event(event)


@app.post("/callback")
async def callback(request: Request):
    """飞书卡片回调入口 - 处理按钮点击"""
    try:
        body = await request.body()
        event = json.loads(body)
        
        await feishu_handler.handle_card_callback(event)
        
        # 飞书卡片回调必须返回这个格式
        return JSONResponse(content={"toast": {"type": "success", "content": ""}})
    
    except Exception as e:
        print(f"Callback error: {e}")
        return JSONResponse(
            content={"toast": {"type": "error", "content": "处理失败"}},
            status_code=500
        )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=config.SERVER_PORT)
