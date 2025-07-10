import os
import sys
import unittest

def main():
    # Add the source directory to PYTHONPATH
    src_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "src"))
    if src_path not in sys.path:
        sys.path.insert(0, src_path)

    # Discover and run tests
    loader = unittest.TestLoader()
    suite = loader.discover(start_dir=os.path.join(os.path.dirname(__file__), "test"))
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    sys.exit(not result.wasSuccessful())

if __name__ == "__main__":
    main()
