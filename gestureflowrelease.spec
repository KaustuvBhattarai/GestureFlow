# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['gestureflowrelease.py'],
    pathex=[],
    binaries=[],
    datas=[('hand_icon.png', '.'), ('no_hand_icon.png', '.'), ('C:\\Users\\MeetK\\AppData\\Local\\Programs\\Python\\Python311\\Lib\\site-packages\\mediapipe', 'mediapipe/')],
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
    name='gestureflowrelease',
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
    codesign_identity=None,
    entitlements_file=None,
    icon=['gfico.ico'],
)
