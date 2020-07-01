# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['main.py'],
             pathex=['C:\\Users\\Nick\\PycharmProjects\\family_book'],
             binaries=[],
             datas=[],
             hiddenimports=["pkg_resources.py2_warn"],
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
          a.binaries,
          a.zipfiles,
          a.datas,
          Tree('C:\\Users\\Nick\\PycharmProjects\\family_book\\venv\\share\\sdl2\\bin\\'),
          Tree('C:\\Users\\Nick\\PycharmProjects\\family_book\\venv\\share\\glew\\bin\\'),
          [],
          name='main',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=False )
