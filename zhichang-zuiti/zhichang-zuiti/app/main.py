"""
职场嘴替 - 主入口
"""
import json
import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse

from app.config import config
from app.handlers.feishu import feishu_handler


@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期"""
    # 启动时
    print(f"🚀 职场嘴替 Bot 启动中...")
    print(f"📝 配置: {config.SERVER_HOST}:{config.SERVER_PORT}")
    yield
    # 关闭时
    print("👋 职场嘴替 Bot 关闭中...")


app = FastAPI(
    title="职场嘴替",
    description="飞书Bot - 帮你把想说的话说出口",
    version="1.0.0",
    lifespan=lifespan,
)


@app.get("/")
async def root():
    """健康检查"""
    return {"status": "ok", "message": "职场嘴替 Bot is running"}


@app.get("/health")
async def health():
    """健康检查"""
    return {"status": "healthy"}


@app.post("/webhook")
async def webhook(request: Request):
    """飞书Webhook入口"""
    try:
        body = await request.body()
        event = json.loads(body)
        
        # 处理事件
        result = await feishu_handler.handle_event(event)
        
        if result:
            # 返回消息卡片
            return JSONResponse(content={
                "msg_type": "interactive",
                "card": result
            })
        
        return JSONResponse(content={"status": "ok"})
    
    except Exception as e:
        print(f"❌ Webhook error: {e}")
        return JSONResponse(
            status_code=500,
            content={"error": str(e)}
        )


@app.post("/callback")
async def callback(request: Request):
    """飞书卡片回调入口"""
    try:
        body = await request.body()
        event = json.loads(body)
        
        # 处理卡片回调
        result = await feishu_handler._handle_card_callback(event)
        
        if result:
            return JSONResponse(content={
                "toast": {"type": "success", "content": "操作成功"},
                "card": result
            })
        
        return JSONResponse(content={"toast": {"type": "success", "content": "操作成功"}})
    
    except Exception as e:
        print(f"❌ Callback error: {e}")
        return JSONResponse(
            status_code=500,
            content={"error": str(e)}
        )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=config.SERVER_HOST,
        port=config.SERVER_PORT,
        reload=True,
    )
