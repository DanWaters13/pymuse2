from src.core.log import log
from src.core.geometry import *
import pygame
import traceback as tb
import sys


def log(msg, indent="", verbose=True):
    if verbose:
        print(f"{indent}{msg}")


def test_geometry(indent="", verbose=True) -> bool:
    try:
        log("Testing Geometry module...", indent, verbose)

        # Test Vector
        log("Testing Vector...", indent + "  ", verbose)
        v2d = Vector(3, 4)
        v3d = Vector(1, 2, 2)
        assert v2d.length() == 5.0, "2D Vector length calculation failed."
        assert v3d.length() == 3.0, "3D Vector length calculation failed."
        log("Vector tests passed.", indent + "  ", verbose)

        # Test Triangle
        log("Testing Triangle...", indent + "  ", verbose)
        tri = Triangle(Vector(0, 0), Vector(10, 0), Vector(5, 5))
        assert tri.contains(5, 2), "Triangle.contains() failed for inside point."
        assert not tri.contains(10, 10), "Triangle.contains() failed for outside point."
        bounds_tri = tri.bounds()
        assert isinstance(bounds_tri, Rect), "Triangle.bounds() failed."
        log("Triangle tests passed.", indent + "  ", verbose)

        # Test Ellipse
        log("Testing Ellipse...", indent + "  ", verbose)
        ellipse = Ellipse(Vector(0, 0), Vector(5, 0), Vector(0, 3))
        assert ellipse.contains(3, 1), "Ellipse.contains() failed for inside point."
        assert not ellipse.contains(6, 0), "Ellipse.contains() failed for outside point."
        bounds_ellipse = ellipse.bounds()
        assert isinstance(bounds_ellipse, Rect), "Ellipse.bounds() failed."
        log("Ellipse tests passed.", indent + "  ", verbose)

        # Test Rect and bounds()
        log("Testing Rect and bounds()...", indent + "  ", verbose)
        rect = Rect(Vector(0, 0), Vector(10, 5))
        bounds = rect.bounds()
        assert bounds == rect, "Rect bounds() method failed."
        pygame_rect = rect.to_pygame_rect()
        assert isinstance(pygame_rect, pygame.Rect), "Rect.to_pygame_rect() failed."
        log("Rect tests passed.", indent + "  ", verbose)

        # Test contains() for 3D Shapes
        log("Testing contains() for Shape3D...", indent + "  ", verbose)
        rect3d = Rect3D(Vector(0, 0, 0), Vector(3, 4))
        assert rect3d.contains(1, 1, 0), "Rect3D.contains() failed for inside point."
        assert not rect3d.contains(11, 1, 0), "Rect3D.contains() failed for outside point."
        log("Shape3D contains() tests passed.", indent + "  ", verbose)

        # Test Shape3D transformations (basic translation)
        log("Testing Shape3D transformations...", indent + "  ", verbose)
        shape3d = Ellipse3D(Vector(0, 0, 0), Vector(5, 0), Vector(0, 3))
        assert shape3d.contains(0, 0, 0), "Ellipse3D.contains() failed."
        log("Shape3D tests passed.", indent + "  ", verbose)

        log("All Geometry tests passed successfully.", indent, verbose)
        return True
    except Exception as e:
        log(f"Geometry tests failed: {e}", indent, verbose)
        exec_type, exec_value, third = sys.exc_info()
        print(exec_type.__name__)
        print(exec_value)
        tb.print_tb(third)
        return False
