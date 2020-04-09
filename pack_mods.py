import os
import zipfile

ONLY_INT_VERSION = '1.8.0.2'

PATH_TO_UNPACK_MODS = os.path.join(os.getcwd(), 'mods_unpack')


def make_zipfile(output_filename, source_dir, name_pack):
    relroot = os.path.abspath(os.path.join(source_dir, os.pardir))
    with zipfile.ZipFile(output_filename, "w", zipfile.ZIP_DEFLATED) as zip:
        for root, dirs, files in os.walk(source_dir):
            zip_relative = os.path.relpath(root, relroot)
            if os.path.relpath(root, zip_relative.lstrip(name_pack)).startswith('mods_unpack'):
                continue
            zip.write(root, os.path.relpath(root, zip_relative.lstrip(name_pack)))
            for file in files:
                filename = os.path.join(root, file)
                if ONLY_INT_VERSION not in filename.split('\\') and 'configs' not in filename.split('\\'):
                    print('[WARNING] Mod not pack, version folder for mods have diff: {}'.format(filename))
                    continue
                if os.path.isfile(filename):  # regular files only
                    arcname = os.path.join(zip_relative.lstrip(name_pack), file)
                    zip.write(filename, arcname)


for mods_pack in os.listdir(PATH_TO_UNPACK_MODS):
    if mods_pack in ('readme.txt',):
        continue
    path_to_mods = os.path.join(os.getcwd(), 'res', 'mods', mods_pack)
    make_zipfile('{}.zip'.format(path_to_mods), os.path.join(PATH_TO_UNPACK_MODS, mods_pack), mods_pack)
    print('[INFO]: Mod {} pack'.format(mods_pack))
