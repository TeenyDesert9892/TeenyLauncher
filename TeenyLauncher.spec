# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['main_window.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='TeenyLauncher',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity='TeenyDesert9892',
    entitlements_file=None,
    version='C:\\Users\\algab\\AppData\\Local\\Temp\\bd3dc2ec-43b7-403b-854e-8908d4b40b85',
    icon=['assets\\images\\Icon.png'],
)
