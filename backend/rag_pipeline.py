from typing import List, Dict, Any
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain.prompts import PromptTemplate
from config import settings
from vector_db import get_vector_db
import logging

logger = logging.getLogger(__name__)

SYSTEM_PROMPT = """You are GitaWise, an AI companion explaining Bhagavad Gita wisdom.

RULES:
1. ALWAYS cite chapter:verse numbers
2. Explain in modern context
3. NEVER claim to be Krishna
4. Provide scholarly context for sensitive topics
5. REFUSE harmful interpretations

VERSES:
{context}

QUESTION: {question}

Provide a thoughtful response."""

class GitaWiseRAG:
    def __init__(self):
        self.embeddings = OpenAIEmbeddings(
            openai_api_key=settings.OPENAI_API_KEY,
            model="text-embedding-3-small"
        )
        
        if settings.LLM_MODEL.startswith("gpt"):
            self.llm = ChatOpenAI(
                api_key=settings.OPENAI_API_KEY,
                model=settings.LLM_MODEL,
                temperature=0.7
            )
        else:
            self.llm = ChatAnthropic(
                api_key=settings.ANTHROPIC_API_KEY,
                model=settings.LLM_MODEL,
                temperature=0.7
            )
        
        self.vector_db = get_vector_db()
    
    async def answer_question(self, question: str, language: str = "english") -> Dict[str, Any]:
        try:
            query_embedding = self.embeddings.embed_query(question)
            verses = self.vector_db.search_verses(query_embedding=query_embedding, top_k=3)
            
            if not verses:
                return {"answer": "No relevant verses found.", "citations": [], "confidence": 0.0}
            
            context = self._format_context(verses)
            prompt = SYSTEM_PROMPT.format(context=context, question=question)
            response = self.llm.invoke(prompt)
            
            confidence = sum(v.get("score", 0) for v in verses) / len(verses)
            
            return {
                "answer": response.content,
                "citations": [{"verse_id": v.get("id"), "score": v.get("score")} for v in verses],
                "confidence": confidence
            }
        except Exception as e:
            logger.error(f"Error: {e}")
            return {"answer": "An error occurred.", "citations": [], "confidence": 0.0}
    
    def _format_context(self, verses: List[Dict[str, Any]]) -> str:
        context = "VERSES:\n\n"
        for verse in verses:
            meta = verse.get("metadata", {})
            context += f"Bhagavad Gita {meta.get('chapter')}.{meta.get('verse')}\n"
            context += f"Text: {meta.get('text')}\n\n"
        return context

_rag_pipeline = None

def get_rag_pipeline() -> GitaWiseRAG:
    global _rag_pipeline
    if _rag_pipeline is None:
        _rag_pipeline = GitaWiseRAG()
    return _rag_pipeline
