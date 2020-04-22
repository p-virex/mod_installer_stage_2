# -*- mode: python ; coding: utf-8 -*-
import os
import json

path_cwd = os.getcwd()

mods_info = json.load(open(os.path.join(path_cwd, 'res', 'mods_config.json')))

block_cipher = None

a = Analysis(['mods_install.py'],
             pathex=['E:\\my_project\\mod_installer_stage_2'],
             binaries=[],
             datas=[('res/locales/RU/LC_MESSAGES/ru.mo', 'res/locales/RU/LC_MESSAGES'), ('res/locales/EN/LC_MESSAGES/en.mo', 'res/locales/EN/LC_MESSAGES')],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)

for name, mod_info in mods_info.items():
    if isinstance(mod_info, dict):
        for mods, info in mod_info.items():
            if mods in ("checkBox", ):
                continue
            a_path, zip_mods = info[0], info[1]
            if a_path is not None:
                full_path_image = os.path.normpath(os.path.join(path_cwd, 'res', a_path))
                a.datas.append(('res/' + a_path, full_path_image, 'DATA'))
                print('Added image: {}'.format(full_path_image))
            full_path_zip = os.path.normpath(os.path.join(path_cwd, 'res', zip_mods))
            a.datas.append(('res/' + zip_mods, full_path_zip, 'DATA'))
            print('Added mod: {}'.format(full_path_zip))
    else:
        info = mods_info.get(name)
        a_path, zip_mods = info[0], info[1]
        if a_path is not None:
            full_path_image = os.path.normpath(os.path.join(path_cwd, 'res', a_path))
            a.datas.append(('res/' + a_path, full_path_image, 'DATA'))
            print('Added image: {}'.format(full_path_image))
        full_path_zip = os.path.normpath(os.path.join(path_cwd, 'res', zip_mods))
        a.datas.append(('res/' + zip_mods, full_path_zip, 'DATA'))
        print('Added mod: {}'.format(full_path_zip))

ADDED_FILES = ['mods_config.json', 'preset.json', 'res_image/main.ico', 'res_image/logo_600_100.png',
                'res_image/logo_600x500.png', 'res_image/not_found.jpg']

for file_name in ADDED_FILES:
    a.datas.append(('res/' + file_name, os.path.join(path_cwd, 'res', file_name), 'DATA'))
    print('Added: {}'.format(file_name))

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
          console=False,
          icon=os.path.join(path_cwd, 'res\\res_image\\main.ico'),
          version='version.txt')
