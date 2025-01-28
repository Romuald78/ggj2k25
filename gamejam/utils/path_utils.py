import sys
import os


def get_path(relative_path):
    if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
        bundle_dir = os.path.join(sys._MEIPASS, relative_path)
    else:
        bundle_dir = os.path.join(os.path.dirname(__file__), '..', '..', relative_path)
    return bundle_dir
