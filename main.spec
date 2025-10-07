# main.spec

import subprocess
import os

# --- INÍCIO DO CÓDIGO ADICIONADO ---
# Pega o caminho de onde o Playwright instalou os navegadores.
# Este comando é a forma oficial recomendada pelo Playwright.
try:
    playwright_browsers_path = subprocess.check_output(
        ['playwright', 'print-browsers-path'],
        shell=True,
        text=True
    ).strip()
except Exception as e:
    print(f"Erro ao obter o caminho dos navegadores do Playwright: {e}")
    # Define um caminho padrão ou encerra se não conseguir encontrar.
    playwright_browsers_path = ''

    
a = Analysis(
    ['main.py'],
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
    [],
    exclude_binaries=True,
    name='main',
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
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='main',
)
