@echo off
setlocal

where python3 > nul 2>&1
if %errorlevel% neq 0 (
    echo Python3 is not installed. Install Python3 before running this script.
    pause
    exit /b 1
)

call :check_package_installation dotenv
call :check_package_installation pyppeteer
call :check_package_installation pyppeteer_stealth
call :check_package_installation telethon
call :run_auto_codes

endlocal
pause

:check_package_installation
set package_name=%1
python3 -c "import %package_name%" > nul 2>&1
if %errorlevel% neq 0 (
    echo The '%package_name%' package is not installed. Starting the installation process...
    if "%package_name%" equ "dotenv" (
        python3 -m pip install python-dotenv
    ) else (
        python3 -m pip install %package_name%
    )
    call :check_installation %package_name%
)
goto :eof

:check_installation
set package_name=%1
python3 -c "import %package_name%" > nul 2>&1
if %errorlevel% equ 0 (
    echo The '%package_name%' package has been successfully installed.
) else (
    echo Installation of the '%package_name%' package failed. Check internet availability and try installing manually.
    pause
    exit /b 1
)
goto :eof

:run_auto_codes
cd data
python3 main.py
goto :eof