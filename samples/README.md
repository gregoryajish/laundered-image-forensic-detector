# ==============================================================================
# Directory: samples/
# Owner: [P1 - ML Forensics Engineer]
# Purpose: Benchmark sample images for local validation and testing.
# ==============================================================================

Place test images here for quick end-to-end testing:
1. `test_real.jpg`: Pristine camera photograph (Ground truth: REAL, sI1 <= 0).
2. `test_synthetic.jpg`: Text-to-image AI generated image (Ground truth: FULLY_SYNTHETIC, sI1 > 0, sI2 <= 0).
3. `test_laundered.jpg`: Pristine photograph passed through Stable Diffusion autoencoders with strength s=0 (Ground truth: LAUNDERED, sI1 > 0, sI2 > 0).
