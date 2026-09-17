// =============================================================================
// File: frontend/src/api/client.ts
// Owner: [P4 - Frontend Core & Upload Engineer]
// Priority: Priority 1 (Stage 5 - Type-Safe API Client)
//
// PURPOSE:
//   Axios client matching backend schemas (DetectionResponse, StageResult).
//
// INTERFACES TO DEFINE (FIXED):
//   export interface StageResult {
//     score: number;
//     threshold: number;
//     prediction: string;
//     confidence: number;
//     num_patches_evaluated: number;
//   }
//   export interface DetectionResponse {
//     scan_id: string;
//     filename: string;
//     image_sha256: string;
//     final_verdict: "REAL" | "FULLY_SYNTHETIC" | "LAUNDERED";
//     summary: string;
//     face_only_applied: boolean;
//     stage1_real_vs_synthetic: StageResult;
//     stage2_laundered_vs_fullysynth?: StageResult;
//     processing_time_ms: number;
//   }
//
// FUNCTIONS TO IMPLEMENT:
//   - detectImage(file: File, selectFace: boolean, mPatches: number): Promise<DetectionResponse>
//   - getHealth(): Promise<HealthResponse>
// =============================================================================

// TODO [P4]: Implement in branch feat/p4-frontend-upload
