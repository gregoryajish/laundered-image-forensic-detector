# ==============================================================================
# File: backend/app/api/batch.py
# Owner: [P2 - Backend Core & API Engineer]
# Priority: Priority 2 (Stage 3b - Batch Upload API)
#
# PURPOSE:
#   Expose POST /api/v1/detect-batch endpoint to process multiple images.
#
# CONTRACT:
#   Endpoint: POST /api/v1/detect-batch
#   Content-Type: multipart/form-data
#   Form Parameters:
#     - files: List[UploadFile]
#     - select_face: bool (default: False)
#     - m_patches: int (default: 600)
#   Response:
#     - 200 OK: List[DetectionResponse]
# ==============================================================================

# TODO [P2]: Implement in branch feat/p2-backend-api
