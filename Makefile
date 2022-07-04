.PHONY: build start-rviz2 start-simulation vel-test clean

SHELL := /usr/bin/bash

build:
	rosdep install -i --from-path src --rosdistro galactic -y
	colcon build --symlink-install --packages-select \
	    dribot_description \
	    dribot_simulation

start-rviz:
	source install/setup.bash && ros2 launch dribot_description rviz_launch.py

start-simulation:
	source install/setup.bash && ros2 launch dribot_simulation gazebo_launch.py

# Run a velocity test command.
vel-test:
	./scripts/vel-test.sh

clean:
	rm -rf build log install
