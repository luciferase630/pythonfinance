# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['UI/Start.py'],  # 使用正斜杠
    pathex=['.'],  # 指定项目根目录为搜索路径
    binaries=[],
    datas=[
        # 添加资源文件和文件夹
        ('Accountdata', 'Accountdata'),
        ('budgetData', 'budgetData'),
        ('FinancialData', 'FinancialData'),
        ('userDataFile', 'userDataFile'),
    ],
    hiddenimports=[
        # 添加所有需要的模块
        'auth.auth_system',
        'auth.storage',
        'auth.user',
        'budget.budget_setting',
        'budget.BudgetComparisonWindow',
        'FileSavingModule.SaveFileWindow',
        'finance.Finance_Data',
        'UI.entry_data_window',
        'UI.main_window',
        'UI.navigation',
        'UI.view_data_window',
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
    a.binaries,
    a.datas,
    [],
    name='Start',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # 如果你希望打开一个控制台窗口，可以将其设置为 True
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
