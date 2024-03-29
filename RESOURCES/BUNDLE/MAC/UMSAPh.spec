# -*- mode: python -*-

block_cipher = None


a = Analysis(['UMSAP.py'],
             pathex=['/Users/kenny/TEMP/BORRAR-GUI/'],
             binaries=[],
             datas=[ ('RESOURCES/', '.') ],
             hiddenimports=[],
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
             icon='RESOURCES/mac-icon.icns',
             bundle_identifier=None,
             info_plist={
               'NSHighResolutionCapable': 'True',
               'NSPrincipleClass': 'NSApplication',
               'NSAppleScriptEnabled': False,
               'CFBundleShortVersionString': '2.1.1',
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
