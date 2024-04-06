#!/bin/bash

check_python() {
    command -v python3 > /dev/null 2>&1
    if [ $? -ne 0 ]; then
        echo "Python3 is not installed. Install Python3 before running this script."
        exit 1
    fi
}

check_package_installation() {
    package_name=$1
    python3 -c "import $package_name" > /dev/null 2>&1
    if [ $? -ne 0 ]; then
        echo "The '$package_name' package is not installed. Starting the installation process..."
        if [ "$package_name" == "dotenv" ]; then
            python3 -m pip install python-dotenv
        else
            python3 -m pip install $package_name
        fi
        check_installation $package_name
    fi
}

check_installation() {
    package_name=$1
    python3 -c "import $package_name" > /dev/null 2>&1
    if [ $? -eq 0 ]; then
        echo "The '$package_name' package has been successfully installed."
    else
        echo "Installation of the '$package_name' package failed. Check internet availability and try installing manually."
        exit 1
    fi
}

run_auto_codes() {
    cd data || exit
    python3 main.py
}

check_python
check_package_installation dotenv
check_package_installation pyppeteer
check_package_installation pyppeteer_stealth
check_package_installation telethon
run_auto_codes