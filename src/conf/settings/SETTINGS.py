import logging
import socket
import sys
import os
import platform

# global logging setting
logging.basicConfig(level=logging.INFO)

# system information
platform = platform.system()
OPERATING_SYSTEM = str(platform).lower()
ARCHITECTURES = ['x32', 'x64']
ARCHITECTURE = None
if sys.maxsize <= 2**32:
    ARCHITECTURE = ARCHITECTURES[0]
elif sys.maxsize > 2**32:
    ARCHITECTURE = ARCHITECTURES[1]

here = os.path.dirname(os.path.realpath(__file__))
PYPELYNE2_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(here)))
ICONS_DIR = os.path.join(PYPELYNE2_ROOT, 'src', 'icons')

ICON_X32 = os.path.join(ICONS_DIR, 'icon_x32.png')
ICON_X64 = os.path.join(ICONS_DIR, 'icon_x64.png')

# Plugin module
PLUGINS_DIR = os.path.join(PYPELYNE2_ROOT, 'src', 'conf', 'plugins')
PLUGINS_FILES = [x for x in os.listdir(PLUGINS_DIR) if not x.startswith('_') and not os.path.isdir(x) and x.endswith('.json')]
PLUGINS_ICONS = os.path.join(PLUGINS_DIR, '_icons')
PLUGINS_DEFAULT_ICON = os.path.join(ICONS_DIR, 'default_plugin_icon.png')
PLUGINS_ICON_HEIGHT = 60
ICON_HEIGHT = 20

# dockwidget_plugins module
DISPLAY_ONLY_AVAILABLE = False

# Task module
TASKS_DIR = os.path.join(PYPELYNE2_ROOT, 'src', 'conf', 'tasks')
TASKS_FILE = os.path.join(TASKS_DIR, 'tasks.json')
# TASKS_FILE = [x for x in os.listdir(TASKS_DIR) if x.endswith('.json')]

# Server and Client modules
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(('8.8.8.8', 80))
    ip = s.getsockname()[0]
    s.close()
except Exception, e:
    print 'could not get local ip: %s' % e
    ip = '127.0.0.1'
SERVER_IP = ip
SERVER_PORT = 5678

# ScreenGrabber module
FPS = 1
CURSOR_ICON = os.path.join(ICONS_DIR, 'cursor_reddot.png')
CURSOR = True
CURSOR_SIZE = 30
PADDING = 10
SCALE_FACTOR = 0.5
GRABBER_FORMAT = 'PNG'
# min 0, max 100, default -1
GRABBER_QUALITY = -1

# MainWindow
SPLASH = True
SPLASH_ICON = os.path.join(ICONS_DIR, 'pypelyne.png')
SHOW_OUTPUT_WINDOWS = True
TABIFY_OUTPUT_WINDOWS = True
CLOSE_DOCK_AFTER_PLUGIN_CLOSE = False

# Resources
REFRESH_INTERVAL = 100
