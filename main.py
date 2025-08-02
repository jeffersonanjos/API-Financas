# main.py
from fastapi import FastAPI, Depends, HTTPException, Query
from typing import List, Optional
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import func
from sqlmodel import select, Session
from datetime import datetime
from pydantic import parse_obj_as

from database import create_db_and_tables, get_session
from models.transaction import (
    Transaction, TransactionCreate, TransactionUpdate, TransactionResponse, 
    TransactionSummary, TransactionType, Category
)
from models.goal import Goal, GoalCreate, GoalUpdate, GoalResponse, GoalStatus

# Configuração da aplicação
app = FastAPI(
    title="API de Finanças Pessoais",
    description="Sistema de gestão financeira pessoal com controle de transações e metas",
    version="1.0.0"
)

# Configuração CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Evento de inicialização
@app.on_event("startup")
def on_startup():
    create_db_and_tables()

# ============================================================================
# ENDPOINTS DE TRANSAÇÕES
# ============================================================================

@app.get("/", tags=["Root"])
def read_root():
    """Endpoint raiz da API"""
    return {
        "message": "Bem-vindo à API de Finanças Pessoais!",
        "version": "1.0.0",
        "docs": "/docs"
    }

@app.post("/transactions/", response_model=TransactionResponse, tags=["Transações"])
def create_transaction(
    *, 
    session: Session = Depends(get_session), 
    transaction: TransactionCreate
):
    """Criar uma nova transação"""
    db_transaction = Transaction.from_orm(transaction)
    session.add(db_transaction)
    session.commit()
    session.refresh(db_transaction)
    return db_transaction

@app.get("/transactions/", response_model=List[TransactionResponse], tags=["Transações"])
def read_transactions(
    *, 
    session: Session = Depends(get_session), 
    offset: int = 0, 
    limit: int = Query(default=100, le=100),
    transaction_type: Optional[TransactionType] = None,
    category: Optional[Category] = None
):
    """Listar transações com filtros opcionais"""
    statement = select(Transaction).offset(offset).limit(limit)
    
    if transaction_type:
        statement = statement.where(Transaction.type == transaction_type)
    
    if category:
        statement = statement.where(Transaction.category == category)
        
    transactions = session.exec(statement).all()
    return transactions

@app.get("/transactions/{transaction_id}", response_model=TransactionResponse, tags=["Transações"])
def read_transaction(
    *, 
    session: Session = Depends(get_session), 
    transaction_id: int
):
    """Buscar uma transação específica"""
    transaction = session.get(Transaction, transaction_id)
    if not transaction:
        raise HTTPException(status_code=404, detail="Transação não encontrada")
    return transaction

@app.put("/transactions/{transaction_id}", response_model=TransactionResponse, tags=["Transações"])
def update_transaction(
    *, 
    session: Session = Depends(get_session), 
    transaction_id: int, 
    transaction: TransactionUpdate
):
    """Atualizar uma transação"""
    db_transaction = session.get(Transaction, transaction_id)
    if not db_transaction:
        raise HTTPException(status_code=404, detail="Transação não encontrada")
    
    transaction_data = transaction.dict(exclude_unset=True)
    for key, value in transaction_data.items():
        setattr(db_transaction, key, value)
    
    session.add(db_transaction)
    session.commit()
    session.refresh(db_transaction)
    return db_transaction

@app.delete("/transactions/{transaction_id}", tags=["Transações"])
def delete_transaction(
    *, 
    session: Session = Depends(get_session), 
    transaction_id: int
):
    """Deletar uma transação"""
    transaction = session.get(Transaction, transaction_id)
    if not transaction:
        raise HTTPException(status_code=404, detail="Transação não encontrada")
    
    session.delete(transaction)
    session.commit()
    return {"message": "Transação deletada com sucesso"}

@app.get("/transactions/summary/category", response_model=List[TransactionSummary], tags=["Relatórios"])
def get_transactions_summary_by_category(
    *, 
    session: Session = Depends(get_session)
):
    """Obter resumo de transações agrupadas por categoria"""
    statement = (
        select(
            Transaction.category,
            func.sum(Transaction.amount).label("total_amount"),
            func.count(Transaction.id).label("transaction_count")
        )
        .group_by(Transaction.category)
    )
    results = session.exec(statement).all()
    
    return [
        TransactionSummary(
            category=r.category, 
            total_amount=r.total_amount,
            transaction_count=r.transaction_count
        ) 
        for r in results
    ]

@app.get("/transactions/summary/balance", tags=["Relatórios"])
def get_balance_summary(*, session: Session = Depends(get_session)):
    """Obter resumo do saldo (receitas - despesas)"""
    # Total de receitas
    receitas_statement = (
        select(func.sum(Transaction.amount))
        .where(Transaction.type == TransactionType.receita)
    )
    total_receitas = session.exec(receitas_statement).first() or 0
    
    # Total de despesas
    despesas_statement = (
        select(func.sum(Transaction.amount))
        .where(Transaction.type == TransactionType.despesa)
    )
    total_despesas = session.exec(despesas_statement).first() or 0
    
    saldo = total_receitas - total_despesas
    
    return {
        "total_receitas": total_receitas,
        "total_despesas": total_despesas,
        "saldo": saldo
    }

# ============================================================================
# ENDPOINTS DE METAS
# ============================================================================

@app.post("/goals/", response_model=GoalResponse, tags=["Metas"])
def create_goal(*, session: Session = Depends(get_session), goal: GoalCreate):
    """Criar uma nova meta financeira"""
    db_goal = Goal.from_orm(goal)
    session.add(db_goal)
    session.commit()
    session.refresh(db_goal)
    return db_goal

@app.get("/goals/", response_model=List[GoalResponse], tags=["Metas"])
def read_goals(
    *, 
    session: Session = Depends(get_session),
    status: Optional[GoalStatus] = None
):
    """Listar metas com filtro opcional por status"""
    statement = select(Goal)
    
    if status:
        statement = statement.where(Goal.status == status)
        
    goals = session.exec(statement).all()
    return goals

@app.get("/goals/{goal_id}", response_model=GoalResponse, tags=["Metas"])
def read_goal(*, session: Session = Depends(get_session), goal_id: int):
    """Buscar uma meta específica"""
    goal = session.get(Goal, goal_id)
    if not goal:
        raise HTTPException(status_code=404, detail="Meta não encontrada")
    return goal

@app.put("/goals/{goal_id}", response_model=GoalResponse, tags=["Metas"])
def update_goal(
    *, 
    session: Session = Depends(get_session), 
    goal_id: int, 
    goal: GoalUpdate
):
    """Atualizar uma meta"""
    db_goal = session.get(Goal, goal_id)
    if not db_goal:
        raise HTTPException(status_code=404, detail="Meta não encontrada")
    
    goal_data = goal.dict(exclude_unset=True)
    for key, value in goal_data.items():
        setattr(db_goal, key, value)
    
    session.add(db_goal)
    session.commit()
    session.refresh(db_goal)
    return db_goal

@app.delete("/goals/{goal_id}", tags=["Metas"])
def delete_goal(*, session: Session = Depends(get_session), goal_id: int):
    """Deletar uma meta"""
    goal = session.get(Goal, goal_id)
    if not goal:
        raise HTTPException(status_code=404, detail="Meta não encontrada")
    
    session.delete(goal)
    session.commit()
    return {"message": "Meta deletada com sucesso"}

@app.put("/goals/{goal_id}/progress", response_model=GoalResponse, tags=["Metas"])
def update_goal_progress(
    *, 
    session: Session = Depends(get_session), 
    goal_id: int, 
    amount: float = Query(..., description="Valor a ser adicionado ao progresso")
):
    """Atualizar o progresso de uma meta"""
    db_goal = session.get(Goal, goal_id)
    if not db_goal:
        raise HTTPException(status_code=404, detail="Meta não encontrada")
    
    if db_goal.status != GoalStatus.ativa:
        raise HTTPException(status_code=400, detail="Só é possível atualizar metas ativas")
    
    db_goal.current_amount += amount
    
    # Verificar se a meta foi atingida
    if db_goal.current_amount >= db_goal.target_amount:
        db_goal.status = GoalStatus.concluida
    
    session.add(db_goal)
    session.commit()
    session.refresh(db_goal)
    return db_goal
