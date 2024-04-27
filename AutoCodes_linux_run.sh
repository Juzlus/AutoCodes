#!/bin/bash

reset='\033[0m'
cyan='\033[0;36m'
red='\033[0;31m'
black='\033[0;90m'
magenta='\033[0;35m'
green='\033[0;32m'
yellow='\033[0;33m'

water_mark() {
    echo -e "$cyan  _  __          _____                                       _         _____          _            "
    echo -e " | |/ /         |  __ \                  _        /\        | |       / ____|        | |           "
    echo -e " | ' / ___ _   _| |  | |_ __ ___  _ __ _| |_     /  \  _   _| |_ ___ | |     ___   __| | ___  ___  "
    echo -e " |  < / _ \ | | | |  | | '__/ _ \| '_ \_   _|   / /\ \| | | | __/ _ \| |    / _ \ / _\` |/ _ \/ __| "
    echo -e " | . \  __/ |_| | |__| | | | (_) | |_) ||_|    / ____ \ |_| | || (_) | |___| (_) | (_| |  __/\__ \ "
    echo -e " |_|\_\___|\__, |_____/|_|  \___/| .__/       /_/    \_\__,_|\__\___/ \_____\___/ \__,_|\___||___/ "
    echo -e "            __/ |                | |                                                               "
    echo -e "           |___/                 |_|                                                               "
    echo
    echo -e Keydrop+ Auto Codes automatically searches for gold codes from Telegram and enters them on key-drop.com. You can find the source code on GitHub: https://github.com/Juzlus/KeydropPlusAutoCodes
    echo -e If you have any Feedback or questions, please contact me at juzlus.biznes@gmail.com or Discord: juzlus.$reset
    echo
}

check_python() {
    echo -e "$black[$(date +'%d.%m.%Y, %T')]$reset Checking installed packages..." 
    echo -en "$black[$(date +'%d.%m.%Y, %T')]$reset Checking installed Python3:"
    command -v python3 > /dev/null 2>&1
    if [ $? -ne 0 ]; then
        echo -e "$red Python3 is not installed. Install Python3 before running this script.$reset"
        exit 1
    else
        echo -e "$green Success$reset"
    fi
}

check_package_installation() {
    package_name=$1
    echo -en "$black[$(date +'%d.%m.%Y, %T')]$reset Checking installed $package_name:" 
    python3 -c "import $package_name" > /dev/null 2>&1
    if [ $? -ne 0 ]; then
        echo -e "$yellow The '$package_name' package is not installed. Starting the installation process...$reset"
        if [ "$package_name" == "dotenv" ]; then
            python3 -m pip install python-dotenv
        else
            python3 -m pip install $package_name
        fi
        check_installation $package_name
    else
        echo -e "$green Success$reset"
    fi
}

check_installation() {
    package_name=$1
    echo -en "$black[$(date +'%d.%m.%Y, %T')]$reset"
    python3 -c "import $package_name" > /dev/null 2>&1
    if [ $? -eq 0 ]; then
        echo -e "$green The '$package_name' package has been successfully installed.$reset"
    else
        echo -e "$red Installation of the '$package_name' package failed. Check internet availability and try installing manually.$reset"
        exit 1
    fi
}

run_auto_codes() {
    echo
    cd data || exit
    python3 main.py
}

water_mark
check_python
check_package_installation psutil
check_package_installation asyncio
check_package_installation dotenv
check_package_installation pyppeteer
check_package_installation pyppeteer_stealth
check_package_installation telethon
run_auto_codes