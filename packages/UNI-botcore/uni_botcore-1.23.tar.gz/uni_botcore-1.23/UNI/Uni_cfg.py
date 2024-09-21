# import builtins
# import subprocess
# import sys
# import importlib
# import pkgutil
# import sysconfig

# # Список встроенных модулей Python
# BUILTIN_MODULES = set(sys.builtin_module_names)

# # Дополнительные модули, которые могут быть встроенными в некоторых системах
# ADDITIONAL_BUILTINS = {
#     'posix', 'termios', 'fcntl', 'tty', 'pty', 'grp', 'pwd', 'spwd', 'crypt', 'zlib', 'math',
#     'syslog', 'resource', 'signal', 'winloop'
# }
# BUILTIN_MODULES.update(ADDITIONAL_BUILTINS)

# # Проверка, является ли модуль встроенным или уже установленным
# def is_builtin_or_installed(module_name):
#     if module_name in BUILTIN_MODULES:
#         return True
#     # Проверяем, установлен ли модуль
#     return pkgutil.find_loader(module_name) is not None

# # Сохраняем оригинальную функцию __import__
# original_import = builtins.__import__

# def custom_import(name, *args, **kwargs):
#     try:
#         # Пытаемся импортировать модуль с использованием оригинальной функции

#         if is_builtin_or_installed(name):
#             print(f"[UNI][LOG] package '{name}' is a built-in or already installed.")
#             return original_import(name, *args, **kwargs)

#         return original_import(name, *args, **kwargs)
#     except ImportError:
#         # Проверяем, является ли модуль встроенным или уже установленным

#         try:
#             # Если модуль не найден, пытаемся его установить через pip
#             print(f"[UNI][LOG] package '{name}' not found. Installing...")
#             subprocess.check_call([sys.executable, "-m", "pip", "install", name])
#             # Пытаемся снова импортировать модуль после установки
#             return original_import(name, *args, **kwargs)
#         except Exception as e:
#             print(f"[UNI][ERROR] Could not install or import module '{name}'. Error: {e}")

# # Заменяем встроенную функцию __import__ на свою
# builtins.__import__ = custom_import





import asyncio
import aiohttp
from argparse import Namespace
import traceback
import json
from decimal import Decimal
import inspect
import time
from typing import List, Optional
import types
from os.path import basename, splitext
import functools
from functools import wraps
import textwrap
from random import randint
import httpx
from urllib.parse import urlparse
from typing import Optional, Callable, Dict, Any, List, Set
import paramiko
import os
import urllib.request as urllib_request
import importlib.util as importlib_util
import sys
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import importlib

# from methods import texts, keyboards

# from Data_ import Packs as Custom_Packs

UNI_Handlers = {}
pre_UNI_Handlers = {}

Bot_Object = None

texts, keyboards = None, None
Custom_Packs = None

v_ = '1.23'