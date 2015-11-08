import logging
import sys
import os
import platform

logging.basicConfig(level=logging.DEBUG)

platform = platform.system()
OPERATING_SYSTEM = str(platform).lower()
ARCHITECTURES = ['x32', 'x64']
ARCHITECTURE = None
if sys.maxsize <= 2**32:
    ARCHITECTURE = ARCHITECTURES[0]
elif sys.maxsize > 2**32:
    ARCHITECTURE = ARCHITECTURES[1]

script_dir = os.path.dirname(os.path.realpath(__file__))
PYPELYNE2_ROOT = os.path.dirname(os.path.dirname(script_dir))
PLUGINS_DIR = os.path.join(PYPELYNE2_ROOT, 'src', 'conf', 'plugins')
PLUGINS_FILES = [x for x in os.listdir(PLUGINS_DIR) if not x.startswith('_') and not os.path.isdir(x) and x.endswith('.json')]
TASKS_FILE = os.path.join(PYPELYNE2_ROOT, 'src', 'conf', 'tasks', 'tasks.json')
# TASKS_FILE = [x for x in os.listdir(TASKS_DIR) if x.endswith('.json')]
