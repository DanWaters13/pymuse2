from src.tests.test_sound import *

def test_main(indent, verbose):
  tests = {
    "sound": (test_sound, True),
  }
  results = {}
  for n,(f,v) in tests.items:
    if f("", v):
      print(f"Test {n} passed")
      results[n] = True
    print(f"Test {n} failed")
    results[n] = False
    break
      
  
