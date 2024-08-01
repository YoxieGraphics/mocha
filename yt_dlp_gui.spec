# -*- mode: python ; coding: utf-8 -*-

import os
import sys
from PyInstaller.utils.hooks import collect_submodules

block_cipher = None

# Function to collect additional binaries
def get_additional_binaries():
    additional_binaries = []
    # Add any other binaries or data files here if necessary
    return additional_binaries

a = Analysis(['main.py'],
             pathex=['.'],
             binaries=get_additional_binaries(),
             datas=[],
             hiddenimports=collect_submodules('yt_dlp'),
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='yt_dlp_gui',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=False)

coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='yt_dlp_gui')
