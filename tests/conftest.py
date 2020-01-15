"""
Module for environment setup and tests runner
"""
import os
import sys


def path_setup():
    test_dir = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(1, test_dir)
    sys.path.insert(1, os.path.dirname(test_dir))
