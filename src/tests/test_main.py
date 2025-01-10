from src.core.log import log
from src.tests.test_sound import test_sound
from src.tests.test_style import test_style
from src.tests.test_json_manager import test_json_manager
from src.tests.test_style import test_style
from src.tests.test_camera import test_camera
from src.tests.test_geometry import test_geometry
from src.tests.test_view import test_view

def test_main(indent=""):
  log("Testing main", indent, True)
  tests = {
    #"sound": (test_sound, True),
    "style": (test_style, True),
    "json manager": (test_json_manager, True),
    "camera": (test_camera, True),
    "geometry": (test_geometry, True),
    "view": (test_view, True),
  }
  print(f"{len(tests)}")
  results = {}
  for n in tests:
    f,v = tests[n]
    if f("\t", v) == True:
      print(f"Test {n} passed")
      results[n] = True
      continue
    print(f"Test {n} failed")
    results[n] = False
    break
