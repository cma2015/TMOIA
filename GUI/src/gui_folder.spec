# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(
    ['gui.py', 'main.py', 'utils_gui.py', 'utils.py'],
    pathex=[],
    binaries=[],
    datas=[('model.cfg', '.'), ('tmoia.ui', '.'), ('tmoia.png', '.'), ('tmoia.ico', '.')],
    hiddenimports=['sklearn.metrics._pairwise_distances_reduction', 'sklearn.metrics._pairwise_distances_reduction._middle_term_computer', 'sklearn.metrics._pairwise_distances_reduction._datasets_pair'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
for d in a.datas:
	if '_C.cp310-win_amd64.pyd' in d[0]:
		a.datas.remove(d)
		break
for d in a.datas:
    if '_C_flatbuffer.cp310-win_amd64.pyd' in d[0]:
        a.datas.remove(d)
        break

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='TMOIA-GUI',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['tmoia.ico'],
)
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='TMOIA-GUI',
)
