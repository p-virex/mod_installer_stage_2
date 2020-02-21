import os

import sys
import webbrowser

EXCLUDE_REL_RES = ()


def resource_path(relative_path):
    """
    The method returns root to the requested resource, based on the abstract path and element name.
    :param relative_path: relative path resource
    :return: join path to resource
    """

    # def resource_path(relative_path):
    # """ Get absolute path to resource, works for dev and for PyInstaller """
    # if hasattr(sys, '_MEIPASS'):
    #     return os.path.join(sys._MEIPASS, relative_path)
    #
    # return os.path.join(os.path.abspath("."), relative_path)
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
        if os.path.isfile(os.path.join(base_path, 'start_python')):
            if relative_path not in EXCLUDE_REL_RES:
                # sed to debug when starting source code
                base_path = os.path.join(os.path.abspath("."), 'res')
    return os.path.join(base_path, relative_path)


def open_web_page(path):
    webbrowser.open(path)
