from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from google.api_core import exceptions as google_exceptions
from google import genai

from app.config import GEMINI_API_KEY, GEMINI_MODEL

router = APIRouter(prefix="/ai", tags=["ai"])

class AIRequest(BaseModel):
    prompt: str = Field(..., description="Texto de entrada para o modelo de IA")

class AIResponse(BaseModel):
    output: str = Field(..., description="Resposta gerada pela IA")

@router.post("/chat", response_model=AIResponse)
def ai_chat(data: AIRequest):
    if not GEMINI_API_KEY:
        raise HTTPException(status_code=500, detail="GEMINI_API_KEY não configurada")
    
    try:
        genai.configure(api_key=GEMINI_API_KEY)
        model = genai.GenerativeModel(GEMINI_MODEL)

        response = model.generate_content(
            data.prompt,
            generation_config={
                "temperature": 0.7,
            }
        )
    except google_exceptions.ResourceExhausted:
        raise HTTPException(
            status_code=429,
            detail=(
                "Quota do Gemini excedida. Verifique billing, limites da conta "
                "e tente novamente mais tarde."
            ),
            headers={"Retry-After": "30"},
        )
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Erro ao chamar Gemini: {e}")
    
    try:
        output_text = response.text
    except Exception:
        raise HTTPException(status_code=502, detail="Resposta do Gemini veio vazia ou em formato inesperado")
    
    return AIResponse(output=output_text)
