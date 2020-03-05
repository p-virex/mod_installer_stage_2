# -*- mode: python ; coding: utf-8 -*-
import os
import json

path_cwd = os.getcwd()

mods_info = json.load(open(os.path.join(path_cwd, 'res', 'mods_config.json')))

block_cipher = None

a = Analysis(['mods_install.py'],
             pathex=['E:\\my_project\\mod_installer_stage_2'],
             binaries=[],
             datas=[('res/locales/RU/LC_MESSAGES/ru.mo', 'res/locales/RU/LC_MESSAGES')],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)

for name, mod_info in mods_info.items():
    for mods, info in mod_info.items():
        if mods in ("checkBox", ):
            continue
        a_path, zip_mods = info[0], info[1]
        full_path_image = os.path.normpath(os.path.join(path_cwd, 'res', a_path))
        full_path_zip = os.path.normpath(os.path.join(path_cwd, 'res', zip_mods))
        a.datas += [('res/' + a_path, full_path_image, 'DATA')]
        a.datas += [('res/' + zip_mods, full_path_zip, 'DATA')]
        print('Added: image > {}, zip > {}'.format(full_path_image, full_path_zip))

a.datas += [('res/mods_config.json', os.path.join(path_cwd, 'res', 'mods_config.json'), 'DATA')]
a.datas += [('res/preset.json', os.path.join(path_cwd, 'res', 'preset.json'), 'DATA')]
a.datas += [('res/res_image/main.ico', os.path.join(path_cwd, 'res', 'res_image', 'main.ico'), 'DATA')]
a.datas += [('res/res_image/logo_600_100.png', os.path.join(path_cwd, 'res', 'res_image', 'logo_600_100.png'), 'DATA')]
a.datas += [('res/res_image/logo_600x500.png', os.path.join(path_cwd, 'res', 'res_image', 'logo_600x500.png'), 'DATA')]
a.datas += [('res/res_image/not_found.jpg', os.path.join(path_cwd, 'res', 'res_image', 'not_found.jpg'), 'DATA')]

pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='Sharewax',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=False, icon=os.path.join(path_cwd, 'res\\res_image\\main.ico'), version='version.txt')
