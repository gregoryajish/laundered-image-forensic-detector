# ==============================================================================
# File: backend/app/schemas.py
# Owner: [P2 - Backend Core & API Engineer]
# Priority: Priority 1 (Core Contracts)
#
# PURPOSE:
#   Single source of truth for Pydantic models crossing API and module boundaries.
#
# WHAT TO IMPLEMENT HERE:
#   1. VerdictEnum (str, Enum):
#      - REAL: "REAL"
#      - FULLY_SYNTHETIC: "FULLY_SYNTHETIC"
#      - LAUNDERED: "LAUNDERED"
#
#   2. PatchAttribution (BaseModel):
#      - patch_index: int
#      - top: int
#      - left: int
#      - score: float
#
#   3. StageResult (BaseModel):
#      - score: float (Mean aggregated patch score)
#      - threshold: float (Default: 0.0)
#      - prediction: str
#      - confidence: float (0.0 to 100.0)
#      - num_patches_evaluated: int (Default: 600)
#      - patch_attributions: Optional[List[PatchAttribution]] (Default: None)
#
#   4. DetectionResponse (BaseModel):
#      - scan_id: str (UUID)
#      - filename: str
#      - image_sha256: str
#      - final_verdict: VerdictEnum
#      - summary: str
#      - face_only_applied: bool (Default: False)
#      - stage1_real_vs_synthetic: StageResult
#      - stage2_laundered_vs_fullysynth: Optional[StageResult] (Default: None)
#      - processing_time_ms: float
#
#   5. HealthResponse (BaseModel):
#      - status: str (Default: "healthy")
#      - cuda_available: bool
#      - device: str
#      - stage1_model_loaded: bool
#      - stage2_model_loaded: bool
#
#   6. ErrorEnvelope (BaseModel):
#      - error: str
#      - detail: str
# ==============================================================================
