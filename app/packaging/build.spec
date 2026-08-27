# -*- mode: python ; coding: utf-8 -*-
"""
build.spec

PyInstaller spec for packaging the app into a single offline executable.

Build with:
    pyinstaller packaging/build.spec --distpath dist --workpath build

Notes:
  - app_root is computed from SPECPATH (the directory this spec file lives
    in), so the build works regardless of what directory you run
    `pyinstaller` from.
  - content.huff is added as a bundled data file (not the raw content/
    folder) - this is what main.py's resolve_content_dir() looks for via
    sys._MEIPASS at runtime when frozen.
  - onefile mode is used for simplest distribution (one file to download),
    at the cost of slightly slower startup (self-extracts to a temp dir
    each launch). onedir is the alternative if startup time matters more
    than single-file simplicity.
"""

from pathlib import Path

app_root = Path(SPECPATH).parent

block_cipher = None

a = Analysis(
    [str(app_root / "main.py")],
    pathex=[str(app_root)],
    binaries=[],
    datas=[
        (str(app_root / "content.huff"), "."),
    ],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    cipher=block_cipher,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name="sudopy",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
