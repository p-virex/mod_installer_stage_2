@ECHO OFF

for %%f in (*.po) do "bin\msgfmt.exe" -o %%~nf.mo %%~nf.po
PAUSE