# Laundered Image Forensic Detector — Engineering Specification

This is the single source of truth for this project: what it is, how it's built, who owns what, and the exact contracts every piece must follow. It is written to be handed to an AI coding assistant along with a statement of which part a developer owns (P1 through P5), so the assistant can generate correct, consistent code without inventing anything that would clash with the other four people's work.

---

## 0. How to Use This Document (Read This Section First)

You are being given this document by one developer on a **5-person team**, each building a different, non-overlapping part of the same system. Before writing any code:

1. **Tag Identification**: Ask the developer which tag they are (**P1 through P5**) if they haven't said so. Look up that tag in Section 10 to find exactly which files they own and what those files need to do.
2. **Strict File Ownership**: Only write code for files owned by that tag, per the ownership table in Section 3. Never create, rename, restructure, or modify a file owned by a different tag — if their work needs something from another file, call the function or hit the endpoint using the exact signature given in Section 6; do not edit that file.
3. **Fixed Contracts**: Treat the Pydantic schemas (Section 4), API contracts (Section 5), and function signatures (Section 6) as fixed. Do not change a field name, add an undeclared field, or alter a response shape — every other developer's code is being generated against these exact shapes independently. Any deviation breaks integration.
4. **Priority 1 Before Priority 2**: Build Priority 1 work before Priority 2 work for that tag, unless the developer explicitly says Priority 1 is already done and merged. If asked for Priority 2 code, verify that it fails safe to its Priority 1 fallback if dependencies are unbuilt.
5. **Coding Conventions**: Follow the coding conventions in Section 9 exactly — this keeps five independently generated codebases mergeable into one.
6. **No Invented Contracts**: If something a developer asks for isn't covered by this document, ask them to confirm the addition rather than inventing it.
7. **Definition of Done**: When you finish a piece of work, check it against Section 11 before handing it back, then fill in the per-feature doc for it per Section 12.

---

## 1. Project Overview

### What It Is
A full-stack forensic web platform to detect **Stable Diffusion (SD) Laundered Images** and **Synthetic Images**. It identifies whether an image is a pristine photograph, a text-to-image/noise synthetic creation, or a real image that has been passed through SD autoencoders ($s=0$) to wash out camera fingerprints and disguise sensitive content.

### What the System Must Do
1. **Stage 1 (Real vs. Synthetic Detection)**: Extract random patches ($N=800$, size $96\times96$) and classify whether the input image is pristine real ($s_I \le 0$) or synthetic ($s_I > 0$).
2. **Stage 2 (Laundered vs. Fully Synthetic Detection)**: If synthetic, analyze patch residuals to classify whether the image is fully synthetic from text prompts ($s_I \le 0$) or a laundered copy of real content ($s_I > 0$).
3. **Forensic Transparency**: Output numerical confidence scores, patch count metrics ($M \in [200, 600]$), execution time, and SHA-256 integrity hash.
4. **Visual & Report Outputs**: Provide a modern web UI with confidence gauges, stage decision flow, optional face-region cropping, and exportable forensic PDF certificates.

### Why This Architecture
Passing real images through SD autoencoders with strength $s=0$ leaves semantic content virtually intact while destroying camera PRNU and sensor noise fingerprints. Traditional single-stage AI detectors classify laundered images as "synthetic", causing content moderation pipelines to mistakenly dismiss real sensitive materials. The two-stage patch-aggregation architecture directly isolates the latent autoencoder resampling traces from both pristine camera artifacts and pure text-to-image noise distributions.

### Non-Functional Requirements
- **Traceability**: Every detection request is assigned a unique UUID `scan_id` and SHA-256 hash.
- **Graceful Hardware Degradation**: If CUDA GPU is unavailable, inference runs on CPU without failing.
- **Memory Efficiency**: Model weights (`synth_vs_real.pth`, `fully-synth_vs_laundered.pth`) are loaded into GPU/CPU memory once on application startup as singletons.
- **Strict Boundary Decoupling**: Frontend and Backend interact strictly through the `/api/v1` REST contract.

---

## 2. The Pipeline — Stages, Priority, and Ownership

- **Priority 1**: Core spine. Must work end-to-end (upload $\rightarrow$ 2-stage inference $\rightarrow$ verdict response $\rightarrow$ UI dashboard).
- **Priority 2**: Differentiators (visual heatmaps, batch uploads, PDF certificate export, face detection crop).
- **Priority 3**: Out of scope (real-time video stream inspection, model re-training).

| Stage | What | Priority | Owner | File(s) |
| :--- | :--- | :--- | :--- | :--- |
| **0** | Weights download & model loading (EfficientNet-B4 + BlazeFace) | Priority 1 | **P1** | `backend/app/ml/models/*`, `scripts/download_weights.py` |
| **1** | Patch sampling ($N=800$, $96\times96$) & Stage 1 Real vs Synthetic ($M=600$) | Priority 1 | **P1** | `backend/app/ml/synthetic_detector.py`, `patch_extractor.py` |
| **2** | Stage 2 Fully Synthetic vs Laundered detector | Priority 1 | **P1** | `backend/app/ml/laundered_detector.py` |
| **2b** | BlazeFace face-region extractor & patch heatmap coordinate mapping | Priority 2 | **P1** | `backend/app/ml/patch_extractor.py` |
| **3** | FastAPI app, CORS, settings, `/api/v1/detect` upload endpoint | Priority 1 | **P2** | `backend/app/main.py`, `config.py`, `schemas.py`, `api/detect.py` |
| **3b** | Batch upload endpoint (`/api/v1/detect-batch`) & `/api/v1/health` status | Priority 2 | **P2** | `backend/app/api/batch.py`, `api/health.py` |
| **4** | Forensic 2-Stage pipeline orchestrator & confidence calculation | Priority 1 | **P3** | `backend/app/services/pipeline.py` |
| **4b** | Forensic PDF certificate generator & scan audit database | Priority 2 | **P3** | `backend/app/services/report.py`, `backend/app/db/*` |
| **5** | Frontend Vite/React shell, Axios client, Drag-and-drop Dropzone | Priority 1 | **P4** | `frontend/src/App.tsx`, `api/client.ts`, `components/Dropzone.tsx` |
| **5b** | Multi-image batch queue UI & image preview zooming | Priority 2 | **P4** | `frontend/src/components/BatchQueue.tsx` |
| **6** | Forensics Results Dashboard, Stage 1 & 2 Cards, Score Gauge | Priority 1 | **P5** | `frontend/src/pages/DetectorPage.tsx`, `components/StageCard.tsx`, `ScoreGauge.tsx` |
| **6b** | Patch inspection heatmap overlay, PDF download trigger, About Page | Priority 2 | **P5** | `frontend/src/components/HeatmapViewer.tsx`, `pages/AboutPage.tsx` |

---

## 3. Repo Structure — One Owner Per File

```text
repo/
├── backend/app/
│   ├── main.py                     [P2] — FastAPI application entrypoint & middleware
│   ├── config.py                   [P2] — Pydantic Settings (paths, device, defaults)
│   ├── schemas.py                  [P2] — Fixed Pydantic models for all boundaries
│   ├── deps.py                     [P2] — Shared dependencies (get_pipeline, get_settings)
│   │
│   ├── api/
│   │   ├── router.py               [P2] — Aggregates /api/v1 routers
│   │   ├── detect.py               [P2] — POST /api/v1/detect (Single image)
│   │   ├── batch.py                [P2] — POST /api/v1/detect-batch (Priority 2)
│   │   └── health.py               [P2] — GET /api/v1/health
│   │
│   ├── ml/                         [P1 — whole folder]
│   │   ├── synthetic_detector.py   — Stage 1 Real vs Synthetic inference
│   │   ├── laundered_detector.py   — Stage 2 Fully-Synth vs Laundered inference
│   │   ├── patch_extractor.py      — 96x96 patch sampling & BlazeFace cropping
│   │   └── models/
│   │       ├── efficientnet.py     — EfficientNet-B4 PyTorch definition
│   │       └── blazeface.py        — BlazeFace network loader
│   │
│   ├── services/                   [P3 — whole folder]
│   │   ├── pipeline.py             — Orchestrates 2-stage decision tree & scoring
│   │   └── report.py               — Generates JSON/PDF forensic certificates (P2)
│   │
│   └── db/                         [P3 — whole folder, Priority 2]
│       ├── database.py             — SQLite async database session
│       └── models.py               — Scan audit log table schema
│
├── frontend/src/
│   ├── main.tsx, App.tsx           [P4] — React entrypoint & routing layout
│   ├── api/client.ts               [P4] — Axios client matching backend schemas
│   ├── components/
│   │   ├── Dropzone.tsx            [P4] — Drag-and-drop file upload with preview
│   │   ├── BatchQueue.tsx          [P4] — Multi-image queue list (Priority 2)
│   │   ├── StageCard.tsx           [P5] — Stage 1 & Stage 2 breakdown card
│   │   ├── ScoreGauge.tsx          [P5] — Animated probability / confidence meter
│   │   └── HeatmapViewer.tsx       [P5] — Patch score visualizer (Priority 2)
│   └── pages/
│       ├── DetectorPage.tsx        [P5] — Main forensics analysis dashboard
│       └── AboutPage.tsx           [P5] — Methodology & research paper citation
│
├── backend/tests/                  [P2 for conftest; all tags write their module tests]
│   ├── conftest.py                 [P2] — Pytest fixtures and dummy test images
│   ├── test_ml_p1.py               [P1] — ML inference unit tests
│   ├── test_api_p2.py              [P2] — API endpoint integration tests
│   └── test_pipeline_p3.py         [P3] — 2-stage pipeline logic tests
│
├── scripts/
│   └── download_weights.py         [P1] — Downloads synth_vs_real.pth & fully-synth_vs_laundered.pth
│
└── samples/                        [P1] — Standard test images (real, synthetic, laundered)
```

---

## 4. Schemas — Fixed Contracts (`backend/app/schemas.py`)

```python
from pydantic import BaseModel, Field
from typing import Optional, List
from enum import Enum

class VerdictEnum(str, Enum):
    REAL = "REAL"
    FULLY_SYNTHETIC = "FULLY_SYNTHETIC"
    LAUNDERED = "LAUNDERED"

class StageResult(BaseModel):
    score: float = Field(..., description="Mean aggregated patch score")
    threshold: float = Field(default=0.0, description="Decision boundary threshold")
    prediction: str = Field(..., description="Classification result for this stage")
    confidence: float = Field(..., ge=0.0, le=100.0, description="Confidence percentage (0-100%)")
    num_patches_evaluated: int = Field(default=600, description="Number of aggregated patches (M)")

class DetectionResponse(BaseModel):
    scan_id: str
    filename: str
    image_sha256: str
    final_verdict: VerdictEnum
    summary: str
    face_only_applied: bool
    stage1_real_vs_synthetic: StageResult
    stage2_laundered_vs_fullysynth: Optional[StageResult] = None
    processing_time_ms: float

class HealthResponse(BaseModel):
    status: str
    cuda_available: bool
    device: str
    stage1_model_loaded: bool
    stage2_model_loaded: bool

class ErrorEnvelope(BaseModel):
    error: str
    detail: str
```

---

## 5. API Contracts — Fixed

### `POST /api/v1/detect` [P2]
- **Content-Type**: `multipart/form-data`
- **Parameters**:
  - `file`: `UploadFile` (Required. Image formats: `.jpg`, `.jpeg`, `.png`, `.webp`)
  - `select_face`: `bool` (Optional, default: `false`)
  - `m_patches`: `int` (Optional, default: `600`, range: `200` to `800`)
- **Success Response (200 OK)**: `DetectionResponse` (Section 4)
- **Error Response (400/500)**: `ErrorEnvelope` `{ "error": "INVALID_IMAGE", "detail": "..." }`

### `GET /api/v1/health` [P2]
- **Success Response (200 OK)**: `HealthResponse` (Section 4)

---

## 6. Function-Level Contracts and Call Order

### `backend/app/ml/synthetic_detector.py` [P1]
```python
def predict_real_vs_synthetic(
    image_np: np.ndarray, 
    m_patches: int = 600, 
    select_face: bool = False
) -> tuple[float, int]:
    """Runs Stage 1 detector on image numpy array (H, W, 3) RGB.
    Returns: (aggregated_score, num_patches). 
    Score > 0 implies Synthetic, <= 0 implies Real.
    """
```

### `backend/app/ml/laundered_detector.py` [P1]
```python
def predict_laundered_vs_fullysynth(
    image_np: np.ndarray, 
    m_patches: int = 600, 
    select_face: bool = False
) -> tuple[float, int]:
    """Runs Stage 2 detector on image numpy array (H, W, 3) RGB.
    Returns: (aggregated_score, num_patches). 
    Score > 0 implies Laundered, <= 0 implies Fully Synthetic.
    """
```

### `backend/app/services/pipeline.py` [P3]
```python
def run_forensic_pipeline(
    image_bytes: bytes, 
    filename: str, 
    select_face: bool = False, 
    m_patches: int = 600
) -> DetectionResponse:
    """Orchestrates 2-Stage pipeline execution:
    1. Computes SHA-256 and decodes image bytes to RGB numpy array.
    2. Calls P1 predict_real_vs_synthetic().
    3. If Stage 1 score <= 0: final_verdict = REAL, stage2 is omitted.
    4. If Stage 1 score > 0: Calls P1 predict_laundered_vs_fullysynth().
       - If Stage 2 score > 0: final_verdict = LAUNDERED
       - If Stage 2 score <= 0: final_verdict = FULLY_SYNTHETIC
    5. Formats and returns DetectionResponse.
    """
```

---

## 7. Refusal & Threshold Rules

1. **Stage 1 (Real vs Synthetic)**:
   - Score $s_{I1} \le 0.0 \implies$ **REAL** (Pristine photo). Stage 2 is skipped.
   - Score $s_{I1} > 0.0 \implies$ **SYNTHETIC**. Proceeds to Stage 2.
2. **Stage 2 (Fully Synthetic vs Laundered)**:
   - Score $s_{I2} > 0.0 \implies$ **LAUNDERED** (*Real photograph disguised through Stable Diffusion autoencoder*).
   - Score $s_{I2} \le 0.0 \implies$ **FULLY_SYNTHETIC** (*Pure text-to-image or random noise synthesis*).
3. **Confidence Mapping Formula**:
   $$\text{Confidence (\%)} = \frac{1}{1 + e^{-|s_I|}} \times 100$$

---

## 8. Hardware Notes

| Tag | Hardware Needed | Why |
| :--- | :--- | :--- |
| **P1 (ML Forensics)** | NVIDIA GPU (4GB+ VRAM) or CPU | Loads EfficientNet-B4 PyTorch models. Falls back to CPU. |
| **P2, P3, P4, P5** | Any standard PC / CPU | API server, service logic, and frontend run without GPU. |

---

## 9. Coding Conventions

- **Language & Runtime**: Python 3.10+, FastAPI (Backend); TypeScript, React 18, Vite (Frontend).
- **Type Hints**: Type annotations on every function parameter and return type.
- **Pydantic Everywhere**: All data crossing module or API boundaries must use models from `schemas.py`.
- **Logging**: Use Python `logging.getLogger(__name__)`. No `print()` in production backend code.
- **Settings**: All configuration reads from `config.py` (`Settings` object). Never call `os.environ` directly outside `config.py`.
- **Fail Safe Priority 2**: Wrap Priority 2 features in try/except blocks so failures fallback gracefully to Priority 1 behavior.

---

## 10. Per-Person Responsibilities

### **P1: ML Forensics Engineer**
- **Owns**: `backend/app/ml/*`, `scripts/download_weights.py`, `samples/*`
- **Priority 1**: Port `EfficientNetB4` architecture, load `.pth` checkpoints, implement `predict_real_vs_synthetic` and `predict_laundered_vs_fullysynth` with random patch sampling ($N=800$, $M=600$).
- **Priority 2**: BlazeFace face detection cropping mode, patch heatmap coordinate calculation.

### **P2: Backend Core & API Engineer**
- **Owns**: `backend/app/main.py`, `config.py`, `schemas.py`, `deps.py`, `api/*`, `backend/tests/conftest.py`
- **Priority 1**: FastAPI setup, CORS middleware, Pydantic schemas, `/api/v1/detect` single image endpoint.
- **Priority 2**: `/api/v1/detect-batch` multi-file endpoint, `/api/v1/health` system diagnostics.

### **P3: Pipeline & Services Engineer**
- **Owns**: `backend/app/services/*`, `backend/app/db/*`
- **Priority 1**: `pipeline.py` orchestrator (Stage 1 $\rightarrow$ Stage 2 conditional tree, timing, SHA-256, confidence calculation).
- **Priority 2**: PDF forensic certificate report export (`report.py`), scan audit SQLite logging (`db/*`).

### **P4: Frontend Core & Upload Engineer**
- **Owns**: `frontend/src/App.tsx`, `main.tsx`, `api/client.ts`, `components/Dropzone.tsx`, `components/BatchQueue.tsx`
- **Priority 1**: Vite + React + TypeScript setup, Axios API client, drag-and-drop Dropzone with file validation and image preview.
- **Priority 2**: Multi-image batch queue UI, image zoom/crop tool.

### **P5: Frontend Forensics UI Engineer**
- **Owns**: `frontend/src/pages/*`, `components/StageCard.tsx`, `components/ScoreGauge.tsx`, `components/HeatmapViewer.tsx`
- **Priority 1**: Forensic results dashboard (`DetectorPage.tsx`), Stage 1 & 2 diagnosis cards, animated confidence gauge.
- **Priority 2**: Patch attribution heatmap overlay (`HeatmapViewer.tsx`), PDF export button, About & Methodology page.

---

## 11. Definition of Done — Check Before Creating PR

- [ ] Only files owned by your tag were created or modified (Section 3).
- [ ] Every function matches its Section 6 signature and Section 4 Pydantic schema.
- [ ] Priority 1 core functionality is 100% working before attempting Priority 2.
- [ ] Priority 2 code fails safe to Priority 1 fallback if dependencies fail.
- [ ] No hardcoded paths or secrets — all settings go through `config.py`.
- [ ] Unit tests exist in `backend/tests/` and pass.
- [ ] A per-feature doc was created in `docs/features/`.

---

## 12. Per-Feature Documentation Template

Save each feature doc in `docs/features/<your-tag>_<stage>_<short-name>.md` (e.g., `P1_stage1_synthetic-detector.md`):

```markdown
# [Feature Name]
**Owner:** [P1 - P5]
**Stage:** [0 - 6, per Section 2]
**Priority:** [1 / 2]
**Files:** [Exact file paths owned]

## What It Does
[2-3 sentences explaining what this feature accomplishes.]

## Example
**Input:** [Input data or file]
**Output:** [Returned data or UI state]

## Depends On / Called By
[Which other tags' functions or endpoints this interacts with]

## Fallback Behavior
[If Priority 2: how it falls back safely. If Priority 1: N/A - core spine.]

## Status
[Not Started / In Progress / Done / Blocked]

## Tests
[Path to test file]
```
