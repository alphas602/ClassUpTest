REM @echo off
REM .venv環境を有効化し、main.pyを実行するバッチファイル

REM .venvのScriptsディレクトリを有効化
call "%~dp0.venv\Scripts\activate.bat"

REM main.pyを実行
python csv-ui-tool\src\main.py

REM 終了時に一時停止
pause