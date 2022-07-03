#!/usr/bin/env bash

PACKAGE_NAME=$1

function main {
    mkdir -p ./src

    if [ -n "${PACKAGE_NAME}" ]; then
        cd ./src && ros2 pkg create --build-type ament_python "${PACKAGE_NAME}"
    else
        echo "Error - Usage: create-python-pkg.sh PACKAGE_NAME"
    fi
}

main
