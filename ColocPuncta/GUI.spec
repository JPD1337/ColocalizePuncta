# -*- mode: python -*-

block_cipher = None

from distutils.sysconfig import get_python_lib
from os import path 
skimage_plugins = Tree(
    path.join(get_python_lib(), "skimage","io","_plugins"), 
    prefix=path.join("skimage","io","_plugins"),
    )

a = Analysis(['GUI.py'],
             pathex=['D:\\Daten\\GitHub\\ColocalizePuncta\\ColocPuncta'],
             binaries=None,
             datas=None,
             hiddenimports=['skimage._shared.transform', 'ColocPuncta'],
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
          name='GUI',
          debug=True,
          strip=False,
          upx=True,
          console=True , icon='files\\icon.ico')
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               skimage_plugins,
               strip=False,
               upx=True,
               name='GUI')
