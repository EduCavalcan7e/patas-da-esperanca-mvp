from datetime import date
from typing import List, Optional
from fastapi import FastAPI, HTTPException, Header
from pydantic import BaseModel, field_validator

app = FastAPI(title="Patas da Esperança API", version="1.1.0")

class VacinaRegistro(BaseModel):
    animal_id: int
    nome_vacina: str
    data_aplicacao: date
    proxima_dose: date

    @field_validator("proxima_dose")
    @classmethod
    def validar_cronologia_doses(cls, v: date, info):
        if "data_aplicacao" in info.data and v < info.data["data_aplicacao"]:
            raise ValueError("A data da próxima dose não pode ser anterior à aplicação.")
        return v

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

def validar_token_bearer(authorization: Optional[str]) -> str:
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Token JWT ausente ou formato inválido")
    token = authorization.removeprefix("Bearer ").strip()
    if len(token) < 20:
        raise HTTPException(status_code=401, detail="Token JWT malformado ou expirado")
    return token

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
    validar_token_bearer(authorization)
    animal = next((a for a in ANIMAIS_DB if a.id == registro.animal_id), None)
    if not animal:
        raise HTTPException(status_code=404, detail="Animal não encontrado")
    VACINAS_DB.append(registro)
    animal.status_sanitario = "em_dia"
    return {
        "mensagem": "Vacina registada com sucesso",
        "prioridade": classificar_prioridade_sanitaria(registro.proxima_dose, date.today()),
    }

@app.patch("/api/animais/{animal_id}/adotar")
def confirmar_adocao(animal_id: int, authorization: Optional[str] = Header(None)):
    validar_token_bearer(authorization)
    animal = next((a for a in ANIMAIS_DB if a.id == animal_id), None)
    if not animal:
        raise HTTPException(status_code=404, detail="Animal não encontrado")
    animal.status_adocao = "adotado"
    return {"id": animal.id, "status_adocao": animal.status_adocao}
