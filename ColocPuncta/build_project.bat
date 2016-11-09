rd /s /q build
rd /s /q dist
pyinstaller GUI.spec --icon="files/icon.ico" -D -d --hiddenimport skimage._shared.transform --hiddenimport ColocPuncta
mkdir "dist/GUI/files"
XCOPY /s files "dist/GUI/files"
ie4uinit.exe -show