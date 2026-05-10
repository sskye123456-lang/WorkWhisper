"""
职场嘴替 - 主入口
"""
import json
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.config import config
from app.handlers.feishu import feishu_handler


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Bot starting... host=" + config.SERVER_HOST + " port=" + str(config.SERVER_PORT))
    yield
    print("Bot shutting down...")


app = FastAPI(title="zhichang-zuiti", version="1.0.0", lifespan=lifespan)


@app.get("/")
async def root_get():
    return {"status": "ok"}


@app.post("/")
async def root_post(request: Request):
    try:
        body = await request.body()
        event = json.loads(body)
        
        if event.get("type") == "url_verification":
            return {"challenge": event.get("challenge")}
        
        result = await feishu_handler.handle_event(event)
        
        if result:
            return JSONResponse(content=result)
        
        return JSONResponse(content={"status": "ok"})
    
    except Exception as e:
        print("Webhook error: " + str(e))
        return JSONResponse(status_code=500, content={"error": str(e)})


@app.get("/health")
async def health():
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=config.SERVER_PORT)
