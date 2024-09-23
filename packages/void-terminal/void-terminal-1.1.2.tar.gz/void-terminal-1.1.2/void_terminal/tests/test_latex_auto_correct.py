"""
Test each plugin in the project。Running method：Run python tests/test_plugins.py directly
"""


import os, sys, importlib


def validate_path():
    dir_name = os.path.dirname(__file__)
    root_dir_assume = os.path.abspath(dir_name + "/..")
    os.chdir(root_dir_assume)
    sys.path.append(root_dir_assume)


validate_path()  # Return project root path

if __name__ == "__main__":
    plugin_test = importlib.import_module('test_utils').plugin_test


    plugin_test(plugin='crazy_functions.Latex_Function->TranslateChineseToEnglishInLatexAndRecompilePDF', main_input="2203.01927")
