import os

import sys
import webbrowser


def resource_path(relative_path):
    """
    The method returns root to the requested resource, based on the abstract path and element name.
    :param relative_path: relative path resource
    :return: join path to resource
    """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, 'res', relative_path)


def open_web_page(path):
    webbrowser.open(path)
