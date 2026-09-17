# ==============================================================================
# File: backend/app/ml/synthetic_detector.py
# Owner: [P1 - ML Forensics Engineer]
# Priority: Priority 1 (Stage 1 - Real vs Synthetic Detector)
#
# PURPOSE:
#   Performs Stage 1 inference to distinguish Pristine Real images from Synthetic images.
#
# FUNCTION SIGNATURE TO IMPLEMENT:
#   def predict_real_vs_synthetic(
#       image_np: np.ndarray, 
#       m_patches: int = 600, 
#       select_face: bool = False
#   ) -> tuple[float, int]:
#
# WHAT TO IMPLEMENT HERE:
#   1. Load checkpoint from settings.STAGE1_WEIGHTS_PATH (weights/synth_vs_real.pth).
#   2. Extract N=800 patches of size 96x96 via patch_extractor.py.
#   3. Apply ImageNet normalization and run model inference on CUDA/CPU.
#   4. Sort patch logits in descending order, take top M=600, compute arithmetic mean.
#   5. Return (mean_score, m_patches).
#      - If score > 0  --> Synthetic (Proceeds to Stage 2)
#      - If score <= 0 --> Pristine Real Photograph (Pipeline halts)
# ==============================================================================
