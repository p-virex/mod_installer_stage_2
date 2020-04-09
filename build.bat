echo Y| rmdir dist  /q /s
echo Y| rmdir build  /q /s
python pack_mods.py
pyinstaller mods_install.spec
pause