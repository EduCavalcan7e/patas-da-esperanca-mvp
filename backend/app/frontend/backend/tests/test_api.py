from datetime import date, timedelta
from fastapi.testclient import TestClient
from app.main import app, classificar_prioridade_sanitaria

client = TestClient(app)

def test_classificacao_prioridade_sanitaria():
    hoje = date(2026, 11, 17)
    assert classificar_prioridade_sanitaria(hoje - timedelta(days=1), hoje) == "ATRASADO"
    assert classificar_prioridade_sanitaria(hoje + timedelta(days=3), hoje) == "PENDENTE"
    assert classificar_prioridade_sanitaria(hoje + timedelta(days=30), hoje) == "EM_DIA"

def test_vitrine_publica_e_bloqueio_sem_jwt():
    res_vitrine = client.get("/api/vitrine")
    assert res_vitrine.status_code == 200
    res_sem_auth = client.post("/api/prontuario/vacinas", json={
        "animal_id": 1, "nome_vacina": "Antirrábica", "data_aplicacao": "2026-11-17", "proxima_dose": "2027-11-17"
    })
    assert res_sem_auth.status_code == 401
