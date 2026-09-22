from fastapi import FastAPI, HTTPException, Security, Depends
from fastapi.security.api_key import APIKeyHeader
from pydantic import BaseModel
from core.cognitive.meta_controller import MetaController
import os

API_KEY = os.getenv("ASTRA_API_KEY", "voss_default_secure_key_2026")
api_key_header = APIKeyHeader(name="X-API-Key")

app = FastAPI(title="GPT ASTRA 2.0 API", description="Production Frontier Gateway")

class QueryRequest(BaseModel):
    prompt: str
    stream: bool = False

astra = MetaController()

async def get_api_key(api_key: str = Security(api_key_header)):
    if api_key == API_KEY:
        return api_key
    raise HTTPException(status_code=403, detail="Could not validate credentials")

@app.post("/v1/reason")
async def reason(request: QueryRequest, authenticated: str = Depends(get_api_key)):
    try:
        result = await astra.process(request.prompt)
        return {"status": "success", "cognitive_state": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
