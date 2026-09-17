# ==============================================================================
# File: backend/app/api/detect.py
# Owner: [P2 - Backend Core & API Engineer]
# Priority: Priority 1 (Stage 3 - Detection API)
#
# PURPOSE:
#   Expose POST /api/v1/detect endpoint for single image forensic analysis.
#
# CONTRACT:
#   Endpoint: POST /api/v1/detect
#   Content-Type: multipart/form-data
#   Form Parameters:
#     - file: UploadFile (Required. Allowed: image/jpeg, image/png, image/webp)
#     - select_face: bool (Optional, default: False)
#     - m_patches: int (Optional, default: 600, range: 200-800)
#
#   Response:
#     - 200 OK: DetectionResponse (from backend.app.schemas)
#     - 400 Bad Request: ErrorEnvelope
#     - 500 Server Error: ErrorEnvelope
#
# IMPLEMENTATION LOGIC:
#   1. Validate file MIME type.
#   2. Read file bytes and pass to run_forensic_pipeline() in services/pipeline.py.
#   3. Return DetectionResponse.
# ==============================================================================

# TODO [P2]: Implement in branch feat/p2-backend-api
