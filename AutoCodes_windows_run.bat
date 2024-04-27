@echo off
setlocal

call :setESC
call :water_mark

set reset=%ESC%[0m
set cyan=%ESC%[36m
set red=%ESC%[31m
set black=%ESC%[90m
set magenta=%ESC%[35m
set green=%ESC%[32m
set yellow=%ESC%[33m

echo %black%[%DATE:~0,2%.%DATE:~3,2%.%DATE:~6,4%, %TIME:~0,8%]%reset% Checking installed packages... 
echo|set /p=%black%[%DATE:~0,2%.%DATE:~3,2%.%DATE:~6,4%, %TIME:~0,8%]%reset% Checking installed Python3: 
where python3 > nul 2>&1
if %errorlevel% neq 0 (
    echo %red%Python3 is not installed. Install Python3 before running this script.%reset%
    pause
    exit /b 1
) else (
    echo %green%Success%reset%
)

call :check_package_installation psutil
call :check_package_installation asyncio
call :check_package_installation dotenv
call :check_package_installation pyppeteer
call :check_package_installation pyppeteer_stealth
call :check_package_installation telethon
call :run_auto_codes

endlocal
pause

:water_mark
    echo  %ESC%[36m_  __          _____                                       _         _____          _           
    echo ^| ^|/ /         ^|  __ \                  _        /\        ^| ^|       / ____^|        ^| ^|          
    echo ^| ' / ___ _   _^| ^|  ^| ^|_ __ ___  _ __ _^| ^|_     /  \  _   _^| ^|_ ___ ^| ^|     ___   __^| ^| ___  ___ 
    echo ^|  ^< / _ \ ^| ^| ^| ^|  ^| ^| '__/ _ \^| '_ \_   _^|   / /\ \^| ^| ^| ^| __/ _ \^| ^|    / _ \ / _` ^|/ _ \/ __^|
    echo ^| . \  __/ ^|_^| ^| ^|__^| ^| ^| ^| (_) ^| ^|_) ^|^|_^|    / ____ \ ^|_^| ^| ^|^| (_) ^| ^|___^| (_) ^| (_^| ^|  __/\__ \
    echo ^|_^|\_\___^|\__, ^|_____/^|_^|  \___/^| .__/       /_/    \_\__,_^|\__\___/ \_____\___/ \__,_^|\___^|^|___/
    echo            __/ ^|                ^| ^|
    echo           ^|___/                 ^|_^|
    echo.
    echo Keydrop+ Auto Codes automatically searches for gold codes from Telegram and enters them on key-drop.com. You can find the source code on GitHub: https://github.com/Juzlus/KeydropPlusAutoCodes
    echo If you have any Feedback or questions, please contact me at juzlus.biznes@gmail.com or Discord: juzlus.%ESC%[0m
    echo.
goto :eof

:check_package_installation
set package_name=%1
echo|set /p=%ESC%[90m[%DATE:~0,2%.%DATE:~3,2%.%DATE:~6,4%, %TIME:~0,8%]%ESC%[0m Checking installed %package_name%: 
python3 -c "import %package_name%" > nul 2>&1
if %errorlevel% neq 0 (
    echo %ESC%[33mThe '%package_name%' package is not installed. Starting the installation process...%ESC%[0m
    if "%package_name%" equ "dotenv" (
        python3 -m pip install python-dotenv
    ) else (
        python3 -m pip install %package_name%
    )
    call :check_installation %package_name%
) else (
    echo %ESC%[32mSuccess%ESC%[0m
)
goto :eof

:check_installation
set package_name=%1
echo|set /p=%ESC%[90m[%DATE:~0,2%.%DATE:~3,2%.%DATE:~6,4%, %TIME:~0,8%]%ESC%[0m 
python3 -c "import %package_name%" > nul 2>&1
if %errorlevel% equ 0 (
    echo %ESC%[32mThe '%package_name%' package has been successfully installed.%ESC%[0m
) else (
    echo %ESC%[31mInstallation of the '%package_name%' package failed. Check internet availability and try installing manually.%ESC%[0m
    pause
    exit /b 1
)
goto :eof

:setESC
for /F "tokens=1,2 delims=#" %%a in ('"prompt #$H#$E# & echo on & for %%b in (1) do rem"') do (
  set ESC=%%b
  exit /B 0
)

:run_auto_codes
echo.
cd data
python3 main.py
goto :eof