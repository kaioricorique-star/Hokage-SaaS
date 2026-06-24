from fastapi import APIRouter, Depends, Response, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.auth import get_tenant_from_header
from app.models.financeiro import Financeiro
from sqlalchemy import func
from datetime import datetime, timedelta
import csv 
import io

router = APIRouter(
    prefix="/api/financeiro", 
    tags=["Financeiro"]
    # Dependência global removida para evitar o erro 401
)

@router.get("")
def listar_financeiro(db: Session = Depends(get_db), tenant_id: int = Depends(get_tenant_from_header)):
    return db.query(Financeiro).filter(Financeiro.tenant_id == tenant_id).all()

@router.post("")
def adicionar_transacao(descricao: str, valor: float, tipo: str, db: Session = Depends(get_db), tenant_id: int = Depends(get_tenant_from_header)):
    if tipo not in ['ENTRADA', 'SAIDA']:
        raise HTTPException(status_code=400, detail="O tipo deve ser 'ENTRADA' ou 'SAIDA'.")
        
    transacao = Financeiro(descricao=descricao, valor=valor, tipo=tipo, tenant_id=tenant_id)
    db.add(transacao)
    db.commit()
    return {"message": "Transação registrada"}

@router.get("/evolucao")
def obter_evolucao(db: Session = Depends(get_db), tenant_id: int = Depends(get_tenant_from_header)):
    hoje = datetime.utcnow().date()
    
    vendas_hoje = db.query(func.sum(Financeiro.valor)).filter(
        Financeiro.tenant_id == tenant_id,
        Financeiro.tipo == 'ENTRADA',
        func.date(Financeiro.data_criacao) == hoje
    ).scalar() or 0.0
    
    return {"faturamento_hoje": vendas_hoje}

@router.get("/resumo-categorias")
def resumo_categorias(dias: int, db: Session = Depends(get_db), tenant_id: int = Depends(get_tenant_from_header)):
    """
    Retorna o resumo financeiro para o dashboard.
    """
    data_limite = datetime.utcnow() - timedelta(days=dias)
    
    entradas = db.query(func.sum(Financeiro.valor)).filter(
        Financeiro.tenant_id == tenant_id,
        Financeiro.tipo == 'ENTRADA',
        Financeiro.data_criacao >= data_limite
    ).scalar() or 0.0
    
    saidas = db.query(func.sum(Financeiro.valor)).filter(
        Financeiro.tenant_id == tenant_id,
        Financeiro.tipo == 'SAIDA',
        Financeiro.data_criacao >= data_limite
    ).scalar() or 0.0
        
    return {
        "entradas": entradas,
        "despesas": saidas,
        "lucro_bruto": entradas - saidas
    }

@router.get("/exportar-csv")
def exportar_financeiro_csv(db: Session = Depends(get_db), tenant_id: int = Depends(get_tenant_from_header)):
    dados = db.query(Financeiro).filter(Financeiro.tenant_id == tenant_id).all()
    
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["ID", "Descricao", "Valor", "Tipo", "Data"])
    
    for d in dados:
        writer.writerow([d.id, d.descricao, d.valor, d.tipo, d.data_criacao])
        
    output.seek(0)
    return Response(
        output.getvalue(), 
        media_type="text/csv", 
        headers={"Content-Disposition": "attachment;filename=financeiro.csv"}
    )