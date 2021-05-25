# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(['src\\__init__.py'],
             datas=[('C:\\Users\\Dell\\Desktop\\Amit\\Parallel-Huffman-Compression\\src\\res\\compress.ico', 'data')],
             pathex=['C:\\Users\\Dell\\Desktop\\Amit\\Parallel-Huffman-Compression'],
             binaries=[],
             hiddenimports=[],
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
          name='Fast CompDe',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=False , icon='src\\res\\compress.ico')
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='Fast CompDe')
