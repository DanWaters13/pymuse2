import numpy as np
from src.core.geometry import Vector, matrices_equal_with_tolerance
from src.core.camera import Camera
from src.core.log import log

def test_camera(indent="", verbose=True) -> bool:
    try:
        log("Testing Camera class...", indent, verbose)

        # Flat Perspective Test
        log("Testing Flat Perspective...", indent + "  ", verbose)
        camera_flat = Camera(mode=None)
        vector = Vector(1, 2, 3)
        transformed_flat = camera_flat.apply(vector)
        assert transformed_flat == (1, 2, 3), "Flat Perspective transformation failed."
        log("Flat Perspective test passed.", indent + "  ", verbose)

        # Orthographic Projection Test
        log("Testing Orthographic Projection...", indent + "  ", verbose)
        camera_ortho = Camera(
            mode="ortho", left=-1, right=1, bottom=-1, top=1, near=1, far=10
        )
        expected_ortho_matrix = np.array([
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, -0.22222222, -1.22222222],
            [0, 0, 0, 1],
        ], dtype=np.float32)
        assert matrices_equal_with_tolerance(camera_ortho.matrix, expected_ortho_matrix), "Orthographic transformation failed."
        log("Orthographic Projection test passed.", indent + "  ", verbose)

        # Frustum Projection Test
        log("Testing Frustum Projection...", indent + "  ", verbose)
        camera_frustum = Camera(mode="frustum", near=1, far=10, fov=90)
        transformed_frustum = camera_frustum.apply(Vector(1, 1, -5))
        assert len(transformed_frustum) == 3, "Frustum transformation failed."
        log("Frustum Projection test passed.", indent + "  ", verbose)

        log("All Camera tests passed successfully.", indent, verbose)
        return True
    except Exception as e:
        log(f"Camera tests failed: {e}", indent, verbose)
        return False