import sys
import warnings

# Check Python Version
if sys.version_info (2, 7) or (3, 0) <= sys.version_info (3, 4):
    print(f"[ERROR] python 2.7+ or 3.4+ required, you are using Python {sys.version_info.major}.{sys.version_info.minor}.", file = sys.stderr)
    sys.exit(1)

# Check Websocket Client
try:
    import websocket
except ImportError:
    warnings.warn(f"websocket not available, please run: {sys.executable} -m pip install websocket-client", file = sys.stderr)
    sys.exit(1)

# Check Python Dispatch
try:
    from pydispatch import Dispatcher
except ImportError:
    warnings.warn(f"pydispatch not available, please run: {sys.executable} -m pip install python-dispatch", file = sys.stderr)
    sys.exit(1)

import threading
import ssl
import time
import json
from datetime import datetime
from pathlib import path

# Environment Variables
from dotenv import load_dotenv
import os

load_dotenv()
print(os.environ["DATABASE_URL"])