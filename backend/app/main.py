from datetime import date
from typing import List, Optional
from fastapi import FastAPI, HTTPException, Header
from pydantic import BaseModel

app = FastAPI(title="Patas da Esperança API", version="1.0.0")

class VacinaRegistro(BaseModel):
    animal_id: int
    nome_vacina: str
    data_aplicacao: date
    proxima_dose: date

class Animal(BaseModel):
    id: int
    nome: str
    especie: str
    porte: str
    status_adocao: str = "disponivel"
    status_sanitario: str = "em_dia"

ANIMAIS_DB: List[Animal] = [
    Animal(id=1, nome="Pipoca", especie="Canina", porte="Médio", status_sanitario="pendente"),
    Animal(id=2, nome="Thor", especie="Canina", porte="Grande", status_sanitario="em_dia"),
]
VACINAS_DB: List[VacinaRegistro] = []

def classificar_prioridade_sanitaria(proxima_dose: date, referencia: date) -> str:
    dias = (proxima_dose - referencia).days
    if dias < 0:
        return "ATRASADO"
    if dias <= 7:
        return "PENDENTE"
    return "EM_DIA"

@app.get("/api/vitrine", response_model=List[Animal])
def listar_vitrine_publica():
    return [a for a in ANIMAIS_DB if a.status_adocao == "disponivel"]

@app.post("/api/prontuario/vacinas", status_code=201)
def registrar_vacina(registro: VacinaRegistro, authorization: Optional[str] = Header(None)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Token JWT ausente ou inválido")
    animal = next((a for a in ANIMAIS_DB if a.id == registro.animal_id), None)
    if not animal:
        raise HTTPException(status_code=404, detail="Animal não encontrado")
    VACINAS_DB.append(registro)
    animal.status_sanitario = "em_dia"
    return {"mensagem": "Vacina registada com sucesso", "prioridade": classificar_prioridade_sanitaria(registro.proxima_dose, date.today())}

@app.patch("/api/animais/{animal_id}/adotar")
def confirmar_adocao(animal_id: int, authorization: Optional[str] = Header(None)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Token JWT ausente ou inválido")
    animal = next((a for a in ANIMAIS_DB if a.id == animal_id), None)
    if not animal:
        raise HTTPException(status_code=404, detail="Animal não encontrado")
    animal.status_adocao = "adotado"
    return {"id": animal.id, "status_adocao": animal.status_adocao}
