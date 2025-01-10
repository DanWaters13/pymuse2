from abc import ABC, abstractmethod
import math
from typing import Union, List, Optional
import numpy as np

def matrices_equal_with_tolerance(mat1, mat2, tol=1e-6):
    return np.allclose(mat1, mat2, atol=tol)

class Vector:
    def __init__(self, *coords: Union[float, int]):
        if len(coords) not in [2, 3]:
            raise ValueError("Vector must be 2D or 3D.")
        self.coords = tuple(float(c) for c in coords)
    def x(self):
        return self.coords[0]
    def y(self):
        return self.coords[1]
    def z(self):
        if len(self.coords) < 3:
            raise AttributeError("This vector does not have a z-coordinate.")
        return self.coords[2]
    
    def project_to_2d(self) -> 'Vector':
        return Vector(self.coords[0], self.coords[1])

    def __len__(self) -> float:
        return self.length()

    def length(self) -> float:
        return math.sqrt(sum(c**2 for c in self.coords))

    def __repr__(self):
        return f"Vector({', '.join(map(str, self.coords))})"

    def __add__(self, other: 'Vector') -> 'Vector':
        if len(self.coords) != len(other.coords):
            raise ValueError("Vectors must have the same dimensions.")
        return Vector(*(a + b for a, b in zip(self.coords, other.coords)))

    def __sub__(self, other: 'Vector') -> 'Vector':
        if len(self.coords) != len(other.coords):
            raise ValueError("Vectors must have the same dimensions.")
        return Vector(*(a - b for a, b in zip(self.coords, other.coords)))


class Shape(ABC):
    def __init__(self):
        self.style = None  # Placeholder for style

    @abstractmethod
    def bounds(self):
        pass

    @abstractmethod
    def contains(self, x, y, z=None, mat=None) -> bool:
        pass

class Shape2D(Shape):
    def __init__(self):
        super().__init__()

    def bounds(self):
        raise NotImplementedError("Must be implemented in subclasses.")

    def contains(self, x, y, z=None, mat=None) -> bool:
        return self.bounds().contains(x, y)

class Shape3D(Shape):
    def __init__(self):
        super().__init__()
        self.rotation_matrix = None  # Placeholder for rotation
        self.translation_vector = None  # Placeholder for translation

    def bounds(self):
        raise NotImplementedError("Must be implemented in subclasses.")

    def contains(self, x, y, z=None, mat=None) -> bool:
        # Apply transformation matrix if provided
        return self.bounds().contains(x, y)

class Rect(Shape2D):
    def __init__(self, top_left: Vector, dims: Vector):
        super().__init__()
        self.top_left = top_left
        self.width = dims.coords[0]
        self.height = dims.coords[1]

    def bounds(self):
        return self  # Rect is its own bounds

    def contains(self, x, y, z=None, mat=None) -> bool:
        return (
            self.top_left.coords[0] <= x <= self.top_left.coords[0] + self.width and
            self.top_left.coords[1] <= y <= self.top_left.coords[1] + self.height
        )

    def to_pygame_rect(self):
        from pygame import Rect as PygameRect
        return PygameRect(
            int(self.top_left.coords[0]),
            int(self.top_left.coords[1]),
            int(self.width),
            int(self.height)
        )

class Rect3D(Shape3D):
    def __init__(self, plane_origin: Vector, dims: Vector):
        super().__init__()
        self.plane_origin = plane_origin
        self.width = dims.coords[0]
        self.height = dims.coords[1]

    def bounds(self):
        # Project the plane onto the XY plane and return a Rect
        projected_top_left = Vector(self.plane_origin.coords[0], self.plane_origin.coords[1])
        return Rect(projected_top_left, Vector(self.width, self.height))

    def contains(self, x, y, z=None, mat=None) -> bool:
        # Apply transformation to determine containment
        return self.bounds().contains(x, y)

class Ellipse(Shape2D):
    def __init__(self, center: Vector, radii_x: Vector, radii_y: Vector):
        super().__init__()
        self.center = center
        self.radii_x = radii_x  # Vector defining horizontal radius
        self.radii_y = radii_y  # Vector defining vertical radius

    def contains(self, x: float, y: float, z=None, mat=None) -> bool:
        """Check if a point (x, y) is inside the ellipse."""
        if z is not None or mat is not None:
            raise ValueError("Ellipses are 2D shapes; z and mat are not applicable.")

        # Transform the point if necessary
        point = Vector(x, y)
        if mat:
            point = mat @ point

        # Ellipse equation: ((x - h)/a)^2 + ((y - k)/b)^2 <= 1
        rx = self.radii_x.length()
        ry = self.radii_y.length()
        relative = point - self.center
        return (relative.coords[0]/rx) ** 2 + (relative.coords[1]/ ry) ** 2 <= 1

    def bounds(self) -> Rect:
        """Returns the bounding rectangle of the ellipse."""
        top_left = self.center - Vector(self.radii_x.length(), self.radii_y.length())
        bottom_right = self.center + Vector(self.radii_x.length(), self.radii_y.length())
        return Rect(top_left, bottom_right - top_left)

class Ellipse3D(Shape3D):
    def __init__(self, center: Vector, radii_x: Vector, radii_y: Vector):
        super().__init__()
        self.center = center
        self.radii_x = radii_x
        self.radii_y = radii_y
    def bounds(self) -> Rect:
        """
        Return the 2D bounding rectangle of the projected ellipse.
        """
        # Project center and radii onto the 2D plane
        projected_center = self.center.project_to_2d()
        radii_x_2d = self.radii_x.project_to_2d()
        radii_y_2d = self.radii_y.project_to_2d()

        # Calculate top-left and dimensions of the bounding box
        radii_x_length = radii_x_2d.length()
        radii_y_length = radii_y_2d.length()
        top_left = projected_center - Vector(radii_x_length, radii_y_length)
        dimensions = Vector(2 * radii_x_length, 2 * radii_y_length)

        return Rect(top_left, dimensions)

    def contains(self, x: float, y: float, z: float, mat=None) -> bool:
        """Check if a 3D point is inside the ellipse's plane."""
        point = Vector(x, y, z)
        if mat:
            point = mat @ point

        # Project the point onto the ellipse's plane and test using 2D logic
        projected_center = self.center.project_to_2d()
        radii_x_2d = self.radii_x.project_to_2d()
        radii_y_2d = self.radii_y.project_to_2d()
        ellipse_2d = Ellipse(projected_center, radii_x_2d, radii_y_2d)
        return ellipse_2d.contains(point.coords[0], point.coords[1])

    def bounds(self) -> Rect:
        """Return the 2D bounding rectangle of the projected ellipse."""
        # Project the center and radii to 2D
        projected_center = self.center.project_to_2d()
        radii_x_2d = self.radii_x.project_to_2d()
        radii_y_2d = self.radii_y.project_to_2d()
        
        # Calculate the furthest extents along x and y axes
        top_left = projected_center - Vector(abs(radii_x_2d.coords[0]), abs(radii_y_2d.coords[1]))
        bottom_right = projected_center + Vector(abs(radii_x_2d.coords[0]), abs(radii_y_2d.coords[1]))
        
        # Compute dimensions
        dimensions = bottom_right - top_left
        
        # Return the bounding Rect
        return Rect(top_left, dimensions)


class Triangle(Shape2D):
    def __init__(self, v1: Vector, v2: Vector, v3: Vector):
        super().__init__()
        self.vertices = [v1, v2, v3]

    def contains(self, x: float, y: float, z=None, mat=None) -> bool:
        """Check if a point (x, y) is inside the triangle."""
        if z is not None or mat is not None:
            raise ValueError("Triangles are 2D shapes; z and mat are not applicable.")

        point = Vector(x, y)
        if mat:
            point = mat @ point

        def sign(p1, p2, p3):
            return (p1.coords[0] - p3.coords[0]) * (p2.coords[1] - p3.coords[1]) \
                - (p2.coords[0] - p3.coords[0]) * (p1.coords[1] - p3.coords[1])

        b1 = sign(point, self.vertices[0], self.vertices[1]) < 0
        b2 = sign(point, self.vertices[1], self.vertices[2]) < 0
        b3 = sign(point, self.vertices[2], self.vertices[0]) < 0
        return b1 == b2 == b3

    def bounds(self) -> Rect:
        xs = [v.x() for v in self.vertices]
        ys = [v.y() for v in self.vertices]
        top_left = Vector(min(xs), min(ys))
        width = max(xs) - min(xs)
        height = max(ys) - min(ys)
        return Rect(top_left, Vector(width, height))

class Triangle3D(Shape3D):
    def __init__(self, v1: Vector, v2: Vector, v3: Vector):
        super().__init__()
        self.vertices = [v1, v2, v3]

    def contains(self, x: float, y: float, z: float, mat=None) -> bool:
        """Check if a 3D point is inside the triangle's plane."""
        point = Vector(x, y, z)
        if mat:
            point = mat @ point

        # Project the triangle onto a 2D plane and test using 2D logic
        vertices_2d = [v.project_to_2d() for v in self.vertices]
        point_2d = point.project_to_2d()
        triangle_2d = Triangle(*vertices_2d)
        return triangle_2d.contains(point_2d.coords[0], point_2d.coords[1])

    def bounds(self) -> Rect:
        """Return the 2D bounding rectangle of the projected triangle."""
        vertices_2d = [v.project_to_2d() for v in self.vertices]
        triangle_2d = Triangle(*vertices_2d)
        return triangle_2d.bounds()

