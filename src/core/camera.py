import numpy as np

class Camera:
    def __init__(self, mode=None, **kwargs):
        """
        Initialize the Camera object.

        Args:
            mode: Camera mode (`None` for flat perspective, "ortho" for orthographic, "frustum" for perspective).
            kwargs: Parameters for the specific camera mode.
                - Ortho: left, right, bottom, top, near, far.
                - Frustum: near, far, fov (field of view in degrees).
        """
        self.mode = mode
        self.matrix = None

        if self.mode is None:
            # Flat perspective (no transformation matrix)
            self.matrix = None
        elif self.mode == "ortho":
            self._initialize_ortho(**kwargs)
        elif self.mode == "frustum":
            self._initialize_frustum(**kwargs)
        else:
            raise ValueError(f"Unsupported mode: {self.mode}")

    def _initialize_ortho(self, left, right, bottom, top, near, far):
        """Sets up an orthographic projection matrix."""
        self.matrix = np.array([
            [2 / (right - left), 0, 0, -(right + left) / (right - left)],
            [0, 2 / (top - bottom), 0, -(top + bottom) / (top - bottom)],
            [0, 0, -2 / (far - near), -(far + near) / (far - near)],
            [0, 0, 0, 1],
        ], dtype=np.float32)

    def _initialize_frustum(self, near, far, fov):
        """Sets up a perspective projection matrix using a frustum."""
        aspect_ratio = 1.0  # Default aspect ratio (can be modified later)
        f = 1 / np.tan(np.radians(fov) / 2)
        depth = far - near

        self.matrix = np.array([
            [f / aspect_ratio, 0, 0, 0],
            [0, f, 0, 0],
            [0, 0, -(far + near) / depth, -2 * far * near / depth],
            [0, 0, -1, 0],
        ], dtype=np.float32)

    def get_matrix(self):
        """Returns the current transformation matrix."""
        return self.matrix

    def apply(self, vector):
        """
        Transforms a Vector using the camera's transformation matrix.
        Args:
            vector: A Vector object with 3D coordinates.

        Returns:
            Transformed Vector as a tuple of (x, y, z).
        """
        if self.matrix is None:
            # Flat perspective: no transformation
            return vector.coords

        if len(vector.coords) != 3:
            raise ValueError("Camera transformations require 3D vectors.")

        # Apply the matrix transformation
        vec = np.array([*vector.coords, 1], dtype=np.float32)  # Homogeneous coordinates
        transformed = self.matrix @ vec

        # Normalize by the w-component (perspective division)
        if transformed[3] != 0:
            transformed = transformed / transformed[3]

        return tuple(transformed[:3])

    def __repr__(self):
        return f"Camera(mode={self.mode}, matrix={self.matrix})"
