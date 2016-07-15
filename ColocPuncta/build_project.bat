rd /s /q build
rd /s /q dist
pyinstaller GUI.py --windowed --icon="files/icon.ico" -D
mkdir "dist/GUI/files"
XCOPY /s files "dist/GUI/files"
ie4uinit.exe -show