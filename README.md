# Patas da Esperança — MVP

Sistema web *mobile-first* desenvolvido para a **Associação Patas da Esperança**, focado na gestão sanitária de animais resgatados e na transparência da vitrine pública de adoção (alinhado ao **ODS 3 — Saúde e Bem-Estar**).

## Funcionalidades Principais

- **Vitrine Pública de Adoção (Tela 1):** Listagem filtrável de animais disponíveis sem necessidade de autenticação.
- **Prontuário Sanitário e Triagem (Tela 2):** Registo rápido de vacinas e vermífugos em 1 a 2 toques, protegido por autenticação JWT.
- **Painel de Alertas e Sincronização Offline (Tela 3):** Classificação multimodal de prioridades sanitárias (cor + ícone + texto, atendendo ao requisito de acessibilidade `RNF04`) e fila local offline via `IndexedDB`.

## Arquitetura e Tecnologias

- **Backend:** Python 3.11+, FastAPI, Pydantic, PyJWT.
- **Frontend:** HTML5, CSS3 (*mobile-first*, contraste WCAG AA), JavaScript (ES6+ com `IndexedDB`).
- **Qualidade e CI:** Pytest (testes unitários e de integração) e GitHub Actions.

## Como Executar Localmente

1. Instale as dependências do backend:
   `pip install fastapi uvicorn pytest httpx`
2. Inicie o servidor FastAPI:
   `uvicorn backend.app.main:app --reload`
3. Execute os testes automatizados:
   `PYTHONPATH=backend pytest -v backend/tests`
