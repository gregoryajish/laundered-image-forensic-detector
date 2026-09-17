# Laundered Image Forensic Detector

A full-stack forensic web platform to detect **Stable Diffusion (SD) Laundered Images** and **Synthetic Images**.

---

## 📖 Engineering Specification & Architecture

This repository follows a strict multi-developer engineering specification dividing ownership across 5 tags (`P1` to `P5`).

👉 **Read the master specification**: [`docs/ENG_SPEC.md`](docs/ENG_SPEC.md)

---

## 👥 Team Ownership & Roles

| Tag | Member Role | Assigned Files / Folders | Primary Responsibility |
| :--- | :--- | :--- | :--- |
| **`P1`** | **ML Forensics Engineer** | `backend/app/ml/*`, `scripts/download_weights.py` | EfficientNet-B4 neural network models & 2-stage patch inference |
| **`P2`** | **Backend Core & API Engineer** | `backend/app/main.py`, `schemas.py`, `config.py`, `api/*` | FastAPI app, Pydantic schemas, and REST endpoints |
| **`P3`** | **Pipeline & Services Engineer** | `backend/app/services/*`, `backend/app/db/*` | 2-Stage pipeline orchestrator & PDF forensic certificates |
| **`P4`** | **Frontend Core & Upload Engineer** | `frontend/src/App.tsx`, `api/client.ts`, `components/Dropzone.tsx` | React/Vite shell, Axios client, drag-and-drop upload |
| **`P5`** | **Frontend Forensics UI Engineer** | `frontend/src/pages/*`, `components/StageCard.tsx`, `components/ScoreGauge.tsx` | Forensics dashboard, diagnostic verdict cards, confidence gauges |

---

## 🚀 Quickstart

### 1. Download Model Weights
```bash
python scripts/download_weights.py
```

### 2. Backend Setup
```bash
cd backend
pip install -r requirements.txt
uvicorn backend.app.main:app --reload --port 8000
```

### 3. Frontend Setup
```bash
cd frontend
npm install
npm run dev
```
Open `http://localhost:5173` in your browser.
