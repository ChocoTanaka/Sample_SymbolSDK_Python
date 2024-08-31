# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['IoTtest_symbol.py'],
    pathex=[],
    //これがどのような拡張子ファイルかわからないが、pip show ripemd-hash でディレクトリを探す
    binaries=[('/*directory*/\\_ripemd160*.pyd', 'ripemd')],
    datas=[],
    hiddenimports=[],
    hookspath=['/hooks'],
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
    name='IoTtest_symbol',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
