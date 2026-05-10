# Main Entry
import json
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.config import config
from app.handlers.feishu import feishu_handler


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Bot starting on port", config.SERVER_PORT)
    yield
    print("Bot shutting down")


app = FastAPI(title="Workplace Mouthpiece", version="1.0.0", lifespan=lifespan)


@app.get("/")
async def root():
    return {"status": "ok", "message": "Workplace Mouthpiece Bot"}


@app.get("/health")
async def health():
    return {"status": "healthy"}


@app.get("/debug")
async def debug():
    aid = config.FEISHU_APP_ID
    ase = config.FEISHU_APP_SECRET
    return {
        "app_id_set": aid != "",
        "app_id_len": len(aid) if aid else 0,
        "app_id_preview": aid[:10] + "..." if aid and len(aid) > 10 else aid,
        "app_secret_set": ase != "",
        "app_secret_len": len(ase) if ase else 0,
    }


@app.post("/")
async def webhook(request: Request):
    try:
        body = await request.body()
        event = json.loads(body)
        
        print("DEBUG: Received POST to /")
        print("DEBUG: event type =", event.get("type"))
        
        # URL verification
        if event.get("type") == "url_verification":
            return {"challenge": event.get("challenge")}
        
        # Handle event
        result = await feishu_handler.handle_event(event)
        
        if result:
            return JSONResponse(content=result)
        
        return JSONResponse(content={"status": "ok"})
    
    except Exception as e:
        print("ERROR:", str(e))
        import traceback
        traceback.print_exc()
        return JSONResponse(status_code=500, content={"error": str(e)})


@app.post("/callback")
async def callback(request: Request):
    try:
        body = await request.body()
        event = json.loads(body)
        
        print("DEBUG: Received card callback")
        
        await feishu_handler.handle_card_callback(event)
        
        return JSONResponse(content={"toast": {"type": "success", "content": "OK"}})
    
    except Exception as e:
        print("ERROR:", str(e))
        return JSONResponse(status_code=500, content={"error": str(e)})


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=config.SERVER_PORT)
