# -*- mode: python -*-

block_cipher = None


a = Analysis(['UMSAP.py'],
             pathex=['C:\\Users\\bravo\\Desktop\\SharedFolders\\BORRAR-GUI'],
             binaries=[],
             datas=[
                ('RESOURCES', 'RESOURCES/.'),
                ('C:\\Users\\bravo\\AppData\\Local\\Continuum\\miniconda3\\envs\\wxapps-3.9\\Lib\\site-packages\\Bio\\Align\\substitution_matrices\\data\\BLOSUM62', 'Bio\\Align\\substitution_matrices\\data\\'),
                ('C:\\Users\\bravo\\AppData\\Local\\Continuum\\miniconda3\\envs\\wxapps-3.9\\Lib\\site-packages\\matplotlib\\backends\\backend_svg.py',              'matplotlib\\backends\\'),
                ('C:\\Users\\bravo\\AppData\\Local\\Continuum\\miniconda3\\envs\\wxapps-3.9\\Lib\\site-packages\\matplotlib\\backends\\backend_mixed.py',            'matplotlib\\backends\\'),
             ],
             hiddenimports=['wx._xml'],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='UMSAP',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          icon='RESOURCES/IMAGES/icon2.ico',
          console=False,
          version='version.txt')
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='UMSAP')
