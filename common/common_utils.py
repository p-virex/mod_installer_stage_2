import os

import sys
import webbrowser

from common.constants import g_PYTHON_START


def resource_path(relative_path):
    """
    Функция для получения пути к ресурсам, все не .py файлы обязаны храниться в директории res.
    Такая зависимость обусловлена особенностями упаковки с помощью pyinstaller, т.к root меняется при запуске из .ехе
    """
    if not g_PYTHON_START:
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, 'res', relative_path)


def open_web_page(path):
    webbrowser.open(path)
