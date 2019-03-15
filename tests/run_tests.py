"""
Module for environment setup and tests runner
"""
import os
import sys
import unittest


def path_setup():
    test_dir = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(1, test_dir)
    sys.path.insert(1, os.path.dirname(test_dir))


def main():
    path_setup()
    verbose = 1
    suite = None
    loader = unittest.TestLoader()
    buf = True

    if "verbose" in sys.argv:
        verbose = 2

    if (len(sys.argv) > 1) and (sys.argv[1] not in ["verbose"]):
        suite = loader.loadTestsFromNames([sys.argv[1]])
        buf = False
    else:
        suite = loader.discover('test')

    sys.exit(
      0 if unittest.TextTestRunner(verbosity=verbose, buffer=buf).run(suite).wasSuccessful() else 1
    )


if __name__ == '__main__':
    main()
