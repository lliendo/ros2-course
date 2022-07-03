.PHONY: build start-rviz2 clean

SHELL := /usr/bin/bash

build:
	rosdep install -i --from-path src --rosdistro galactic -y
	colcon build --symlink-install --packages-select \
	    dribot_description

start-rviz:
	source install/setup.bash && ros2 launch dribot_description rviz_launch.py

clean:
	rm -rf build log install
