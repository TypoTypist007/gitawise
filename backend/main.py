from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import logging
from config import settings
from rag_pipeline import get_rag_pipeline
from utils_safety import check_query_safety

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title=settings.API_TITLE, version=settings.API_VERSION)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatMessage(BaseModel):
    role: str
    content: str

class AskRequest(BaseModel):
    question: str
    language: str = "english"
    chat_history: Optional[List[ChatMessage]] = None

class AskResponse(BaseModel):
    answer: str
    citations: List[dict]
    confidence: float
    language: str
    warning: Optional[str] = None

@app.get("/")
async def root():
    return {"name": "GitaWise API", "status": "operational"}

@app.get("/health")
async def health():
    return {"status": "healthy"}

@app.post("/chat/ask", response_model=AskResponse)
async def ask_question(request: AskRequest) -> AskResponse:
    try:
        is_safe, msg = check_query_safety(request.question)
        if not is_safe:
            raise HTTPException(status_code=400, detail=msg)
        
        rag = get_rag_pipeline()
        result = await rag.answer_question(request.question, request.language)
        
        return AskResponse(
            answer=result.get("answer", ""),
            citations=result.get("citations", []),
            confidence=result.get("confidence", 0.0),
            language=request.language,
            warning="AI interpretation - consult qualified scholars"
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/verse/chapters")
async def list_chapters():
    chapters = [
        {"number": 1, "title": "Arjuna Visada Yoga", "verses": 47},
        {"number": 2, "title": "Sankhya Yoga", "verses": 72},
        {"number": 18, "title": "Moksha Sannyasa Yoga", "verses": 78},
    ]
    return {"total_chapters": 18, "chapters": chapters}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=settings.DEBUG)
