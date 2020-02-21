@ECHO OFF

for %%f in (*.po) do "bin\msgfmt.exe" -o ..\RU\LC_MESSAGES\%%~nf.mo %%~nf.po
PAUSE