# ==============================================================================
# File: backend/app/services/pipeline.py
# Owner: [P3 - Pipeline & Services Engineer]
# Priority: Priority 1 (Stage 4 - Forensic Pipeline Orchestrator)
#
# PURPOSE:
#   Orchestrates the 2-Stage forensic decision tree, SHA-256 integrity hash,
#   execution timer, and confidence calculation.
#
# FUNCTION SIGNATURE TO IMPLEMENT:
#   def run_forensic_pipeline(
#       image_bytes: bytes, 
#       filename: str, 
#       select_face: bool = False, 
#       m_patches: int = 600
#   ) -> DetectionResponse:
#
# WHAT TO IMPLEMENT HERE:
#   1. Decode image bytes to RGB numpy array & compute SHA-256 checksum.
#   2. Call P1: predict_real_vs_synthetic(img_np, m_patches, select_face).
#   3. Map logit score to calibrated confidence: sigmoid(|score|) * 100.
#   4. If Stage 1 score <= 0:
#      - final_verdict = REAL
#      - stage2_laundered_vs_fullysynth = None
#   5. If Stage 1 score > 0:
#      - Call P1: predict_laundered_vs_fullysynth(img_np, m_patches, select_face).
#      - If Stage 2 score > 0: final_verdict = LAUNDERED
#      - If Stage 2 score <= 0: final_verdict = FULLY_SYNTHETIC
#   6. Construct and return DetectionResponse (from backend.app.schemas).
# ==============================================================================
