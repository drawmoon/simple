import os
import platform
import shutil
import sys

from cx_Freeze import Executable, setup

NAME = "simple"
DESCRIPTION = "simple"
VERSION = "0.0.1"


if __name__ == "__main__":
    os_family = {"Windows": "win", "Darwin": "mac", "Linux": "linux"}[platform.system()]
    sys.argv[:] = [sys.argv[0], "build"]

    buildOptions = dict(
        packages=[],
        excludes=[],
        include_files=[("assets", "assets"), ("source/data", "source/data")],
    )

    target = Executable(
        "main.py",
        base={"win": "Win32GUI", "mac": None, "linux": None}[os_family],
        targetName=NAME,
        icon="assets/icon." + {"win": "ico", "mac": "icns", "linux": "ico"}[os_family],
        copyright="Drawmoon",
    )

    setup(
        name=NAME,
        version=VERSION,
        description=DESCRIPTION,
        options={"build_exe": buildOptions},
        executables=[target],
    )

    # zip files
    build_dir = "build/" + os.listdir("build")[-1]
    shutil.make_archive(f"build/{NAME}_{os_family}_v{VERSION}", "zip", build_dir)
