# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[
        'tkinter', 'tkinter.ttk', 'tkinter.font',
        'tkinter.messagebox', 'tkinter.scrolledtext',
        'problems.algebra.linear_equations',
        'problems.algebra.inequalities',
        'problems.algebra.quadratics',
        'problems.algebra.exponents_radicals',
        'problems.algebra.word_problems',
        'problems.geometry.angles_lines',
        'problems.geometry.triangles',
        'problems.geometry.polygons',
        'problems.geometry.circles',
        'problems.geometry.coordinate_geometry',
        'content.algebra.linear_equations',
        'content.algebra.inequalities',
        'content.algebra.quadratics',
        'content.algebra.exponents_radicals',
        'content.algebra.word_problems',
        'content.geometry.angles_lines',
        'content.geometry.triangles',
        'content.geometry.polygons',
        'content.geometry.circles',
        'content.geometry.coordinate_geometry',
    ],
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
    name='MathFoundationBuilder',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
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
    name='MathFoundationBuilder',
)
app = BUNDLE(
    coll,
    name='MathFoundationBuilder.app',
    icon=None,
    bundle_identifier=None,
)
