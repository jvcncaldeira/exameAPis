from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime
from typing import List

app = FastAPI()

class Cliente(BaseModel):
    posicao: int
    nome: str
    data_chegada: datetime
    atendido: bool
    tipo_atendimento: str

fila_atendimento: List[Cliente] = [Cliente]

@app.get("/", response_model=str)
def rota_raiz():
    return "Bem-vindo à aplicação de filas!"

@app.get("/fila", response_model=List[Cliente])
def obter_fila():
    return fila_atendimento

@app.get("/fila/{id}", response_model=Cliente)
def obter_cliente_na_posicao(id: int):
    if id >= len(fila_atendimento) or id < 0:
        raise HTTPException(status_code=404, detail="Posição na fila não encontrada")
    return fila_atendimento[id]

@app.post("/fila", response_model=Cliente)
def adicionar_cliente_na_fila(cliente: Cliente):
    if len(cliente.nome) > 20:
        raise HTTPException(status_code=400, detail="O campo 'nome' deve ter no máximo 20 caracteres")
    if cliente.atendimento not in ["N", "P"]:
        raise HTTPException(status_code=400, detail="O campo 'atendimento' deve ser 'N' ou 'P'")
    
    novo_cliente = {
        "posicao": len(fila_atendimento),
        "nome": cliente.nome,
        "data_chegada": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),  # Convertendo para string
        "atendido": False,
        "tipo_atendimento": cliente.atendimento
    }
    
    fila_atendimento.append(novo_cliente)
    return novo_cliente

@app.put("/fila")
def atualizar_fila():
    if not fila_atendimento:
        raise HTTPException(status_code=400, detail="A fila está vazia")
    
    fila_atendimento[0]["posicao"] = -1
    fila_atendimento[0]["atendido"] = True
    
    for i in range(1, len(fila_atendimento)):
        fila_atendimento[i]["posicao"] -= 1
    
    return {"message": "Fila atualizada com sucesso"}

@app.delete("/fila/{id}", response_model=Cliente)
def remover_cliente_da_fila(id: int):
    if id >= len(fila_atendimento) or id < 0:
        raise HTTPException(status_code=404, detail="Posição na fila não encontrada")
    
    cliente_removido = fila_atendimento.pop(id)
    
    for i in range(id, len(fila_atendimento)):
        fila_atendimento[i]["posicao"] -= 1
    
    return cliente_removido