from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.ticket import Ticket
from app.schemas.ticket import TicketCreate, TicketResponse, TicketUpdateStatus
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.ticket import Ticket
from app.schemas.ticket import TicketCreate, TicketResponse, TicketUpdateStatus

router = APIRouter(prefix="/tickets", tags=["Chamados de Suporte"])

@router.post("/", response_model=TicketResponse, status_code=status.HTTP_201_CREATED)
def criar_ticket(ticket_data: TicketCreate, db: Session = Depends(get_db)):
    novo_ticket = Ticket(**ticket_data.dict())
    db.add(novo_ticket)
    db.commit()
    db.refresh(novo_ticket)
    return novo_ticket

@router.get("/", response_model=List[TicketResponse])
def listar_tickets(setor: str = None, db: Session = Depends(get_db)):
    query = db.query(Ticket)
    if setor:
        query = query.filter(Ticket.setor == setor)
    return query.all()

@router.patch("/{ticket_id}/status", response_model=TicketResponse)
def atualizar_status_ticket(ticket_id: int, status_data: TicketUpdateStatus, db: Session = Depends(get_db)):
    ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket não encontrado.")
    
    ticket.status = status_data.status
    db.commit()
    db.refresh(ticket)
    return ticket

@router.post("/{ticket_id}/emergencia-intervencao")
def intervencao_emergencia(ticket_id: int, db: Session = Depends(get_db)):
    """
    Intervenção de Emergência:
    1. Localiza o ticket de emergência.
    2. Futura integração: Cancela o pedido, estorna o pagamento e devolve estoque (vinculado ao tenant_id).
    3. Altera o status do ticket para 'Resolvido - Intervenção Automática'.
    """
    ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket não encontrado.")
    
    # Lógica de segurança para cancelar o pedido e estornar estoque associado ao tenant_id
    # ... (implementar chamada ao serviço de pedidos/estoque aqui) ...

    # Fecha o chamado automaticamente após a intervenção
    ticket.status = "Resolvido - Intervenção Automática"
    db.commit()
    
    return {
        "message": "Intervenção de emergência executada com sucesso.",
        "ticket_id": ticket.id,
    }
