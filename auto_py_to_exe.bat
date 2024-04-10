echo off
cls
set "py_path=%1"
set "script_dir=%~dp0"
if "%py_path%"=="" (
    py -m auto_py_to_exe -nc -lang zh_tw -o "%script_dir%dist" -c "default_cofg.json"
) else (
    py -m auto_py_to_exe -nc -lang zh_tw -o "%script_dir%dist" -c "default_cofg.json" "%py_path%"
    copy /v /y dist\dol美化模组自动生成器.exe .
)
@REM pause
exit 0