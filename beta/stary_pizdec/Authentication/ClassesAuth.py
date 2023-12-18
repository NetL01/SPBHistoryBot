import os
import importlib

def call_check_in_all_modules(directory):
    for filename in os.listdir(directory):
        if filename.endswith(".py"):
            module_name = filename[:-3]
            module = importlib.import_module(f"{directory}.{module_name}")
            if hasattr(module, "check") and callable(getattr(module, "check")):
                module.check()

class Auth:

    def __init__(self):
