import os
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import List
import google.generativeai as genai
from app.auth import get_tenant_from_header

router = APIRouter(
    prefix="/api/ai", 
    tags=["Inteligência Artificial (IA)"], 
    dependencies=[Depends(get_tenant_from_header)]
)

genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

@router.post("/previsao-demanda")
def prever_demanda(historico_vendas: dict, tenant_id: int = Depends(get_tenant_from_header)):
    if not historico_vendas:
        raise HTTPException(status_code=400, detail="Envie o histórico de vendas para a IA prever a demanda.")
    
    prompt = f"""
    Você é um especialista em gestão de estoque e cadeia de suprimentos para pequenas empresas.
    Analise o seguinte histórico de vendas recentes:
    {historico_vendas}
    """
    return {"status": "processado"}

@router.post("/promocao-dinamica")
def gerar_promocao_dinamica(produto_nome: str, tenant_id: int = Depends(get_tenant_from_header)):
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(f"Gerar promoção para {produto_nome}")
        return {"mensagem": "Promoção dinâmica gerada", "promocao": response.text, "tenant_id": tenant_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao comunicar com a IA: {str(e)}")

class MensagemCliente(BaseModel):
    telefone: str
    mensagem: str

@router.post("/enviar-mensagem-cliente")
def enviar_mensagem(dados: MensagemCliente, tenant_id: int = Depends(get_tenant_from_header)):
    return {"status": "Mensagem enviada", "tenant_id": tenant_id}