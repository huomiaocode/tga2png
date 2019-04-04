#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import os
import shutil

params = (
    "C:\Python27\Scripts\pyinstaller.exe",
    "-F",
    "./tga2png.py"
)

os.system(" ".join(params))