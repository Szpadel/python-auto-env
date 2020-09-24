# This module is to automatically maintain virtual env
# and run python application inside
# any changes to requirements.txt will recreate venv

# Usage:
# Place file next to your main.py and prepand main.py with this snippet:
#
# import auto_env
# import os

# current_file = os.path.abspath(__file__)
# current_dir = os.path.dirname(current_file)
# auto_env.run_in_venv(
#     "%s/.venv" % current_dir,
#     "%s/requirements.txt" % current_dir,
#     current_file
# )

from typing import Optional
import venv
import os
import sys
from pathlib import Path
import shutil
import subprocess

def _eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

def _are_requirements_up_to_date(venv_path: str, requirements: str) -> bool:
    installed_requirements = os.path.join(venv_path, "_installed_requirements.txt")
    installed = _try_read_file_content(installed_requirements)
    expected = _try_read_file_content(requirements)
    return installed is not None and installed == expected

def _try_read_file_content(file: str) -> Optional[str]:
    if os.path.exists(file):
        return Path(file).read_text()
    return None

def _bin_dir() -> str:
    if os.name == "posix":
        return "bin"
    elif os.name == "nt":
        return "Scripts"
    else:
        raise Exception("Unsupported OS")

def run_in_venv(venv_path: str, requirements: str, main: str):
    # abort execution if already inside venv (we are restarting ourself)
    if sys.prefix != sys.base_prefix:
        return

    if not _are_requirements_up_to_date(venv_path, requirements):
        if os.path.exists(venv_path):
            shutil.rmtree(venv_path)
        venv.create(venv_path, with_pip=True)
        venv_pip = os.path.join(venv_path, _bin_dir(), 'pip')
        proc = subprocess.run([
            venv_pip,
            "install",
            "-r",
            requirements,
        ])
        if proc.returncode == 0:
            installed_requirements = os.path.join(venv_path, "_installed_requirements.txt")
            shutil.copyfile(requirements, installed_requirements)
        else:
            _eprint("Failed to create virtual env")
            exit(1)

    venv_python = os.path.join(venv_path, _bin_dir(), 'python')
    proc = subprocess.run([
        venv_python,
        main,
    ] + sys.argv[1:])

    exit(proc.returncode)
