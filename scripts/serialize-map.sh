#!/usr/bin/env bash

BASEDIR=$(dirname "$(readlink -f "$0")")

ros2 service call \
    /slam_toolbox/serialize_map \
    slam_toolbox/srv/SerializePoseGraph "filename: '${BASEDIR}/../src/dribot_slam/res/house_map'"
