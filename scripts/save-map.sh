#!/usr/bin/env bash

BASEDIR=$(dirname "$(readlink -f "$0")")

ros2 service call \
    /slam_toolbox/save_map \
    slam_toolbox/srv/SaveMap "name: data: '${BASEDIR}/../src/dribot_slam/res/house_map'"
