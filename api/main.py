from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from core.cognitive.meta_controller import MetaController
import asyncio

app = FastAPI(title="GPT ASTRA 2.0 API", description="Production Gateway")

class QueryRequest(BaseModel):
    prompt: str
    stream: bool = False

astra = MetaController()

@app.post("/v1/reason")
async def reason(request: QueryRequest):
    try:
        result = await astra.perceive(request.prompt)
        return {"status": "success", "cognitive_state": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
