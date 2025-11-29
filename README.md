# MindOS — 사고 감각형 OS (미니멀 데모)

연상 기반 그래프, 맥락 스택/타임라인, 간단 추천, FastAPI + 브라우저 UI/CLI 포함.

## 요구 사항
- Python 3.10
- pip

## 설치
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
python app/ui/cli.py
pytest -q
