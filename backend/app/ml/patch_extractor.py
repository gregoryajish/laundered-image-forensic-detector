# ==============================================================================
# File: backend/app/ml/patch_extractor.py
# Owner: [P1 - ML Forensics Engineer]
# Priority: Priority 1 (Patch Extraction) & Priority 2 (Face ROI & Heatmap)
#
# PURPOSE:
#   Utility to extract N=800 random patches of size 96x96 from the input image.
#
# REQUIREMENTS FOR P1:
#   1. extract_random_patches(image_np, num_patches=800, patch_size=96, seed=21):
#      - Crops square patches across image bounds.
#      - Returns list of np.ndarray patches.
#   2. (Priority 2) extract_face_patches(image_np, facedet):
#      - Uses BlazeFace to locate face bounding box.
#      - Crops patches specifically within face region.
# ==============================================================================

# TODO [P1]: Implement in branch feat/p1-ml-core
