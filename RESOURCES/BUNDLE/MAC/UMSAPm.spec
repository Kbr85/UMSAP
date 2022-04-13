# -*- mode: python -*-

block_cipher = None


a = Analysis(['UMSAP.py'],
             pathex=['/Users/bravo/TEMP-GUI/BORRAR-UMSAP/'],
             binaries=[],
             datas=[ ('RESOURCES', '.') ],
             hiddenimports=['wx._xml'],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name='UMSAP',
          debug=False,
          strip=False,
          upx=True,
          console=False , icon='ndowed')
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='UMSAP')
app = BUNDLE(coll,
             name='UMSAP.app',
             icon='RESOURCES/IMAGES/icon.icns',
             bundle_identifier=None,
             info_plist={
               'NSHighResolutionCapable': 'True',
               'NSPrincipleClass': 'NSApplication',
               'NSAppleScriptEnabled': False,
               'CFBundleShortVersionString': '2.2.0',
               'CFBundleDocumentTypes': [
                  {
                    'CFBundleTypeName': 'My File Format',
                    'CFBundleTypeIconFile': 'MyFileIcon.icns',
                    'LSItemContentTypes': ['com.example.myformat'],
                    'LSHandlerRank': 'Owner'
                    }
                ]
            },
            )
