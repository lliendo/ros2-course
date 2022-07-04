import rclpy

from time import time
from rclpy.node import Node
from geometry_msgs.msg import Twist


class VelocityMultiplexer(Node):

    input_check_timeout = 0.1  # 100ms.
    publisher_timeout = 0.04  # 40ms (25Hz).
    default_qos = 10

    def __init__(self):
        super().__init__('vel_mux')

        # Configure pusblisher and subscribers. Add a "/" and you're screwed, e.g: "/cmd", "/vel_high_priority", etc. Why?
        self._publisher = self.create_publisher(Twist, 'cmd_vel', self.default_qos)
        self.create_subscription(Twist, 'vel_high_priority', self._high_velocity_handler, self.default_qos)
        self.create_subscription(Twist, 'vel_low_priority', self._low_velocity_handler, self.default_qos)

        # Create timers.
        self.create_timer(self.publisher_timeout, self._publish_velocity)
        # Has been commented out as this callback will not behave correctly
        # and constantly stop the robot.
        #self.create_timer(self.input_check_timeout, self._check_inputs)

        self._accept_inputs = True
        self._input = {
            'high_priority': None,
            'low_priority': None,
        }

    def _set_velocity(self, priority, velocity):
        self._input[priority] = {
            'timestamp': time(),
            'velocity': velocity,
        }

    def _high_velocity_handler(self, message):
        print('Received high priority message')
        self._set_velocity('high_priority', message)

    def _low_velocity_handler(self, message):
        print('Received low priority message')
        self._set_velocity('low_priority', message)

    def _no_input_on(self, priority, now):
        return self._input[priority] and ((now - self._input[priority]['timestamp']) > self.input_check_timeout)

    def _check_inputs(self):
        now = time()

        if self._no_input_on('high_priority', now) or self._no_input_on('low_priority', now):
            self._accept_inputs = False

    def _publish_stop(self):
        zero_velocity = Twist()
        zero_velocity.linear.x = 0.0
        zero_velocity.linear.y = 0.0
        zero_velocity.linear.z = 0.0
        zero_velocity.angular.x = 0.0
        zero_velocity.angular.y = 0.0
        zero_velocity.angular.z = 0.0

        self._publisher.publish(zero_velocity)
        self._input.update({
            'high_priority': None,
            'low_priority': None,
        })

    def _received_velocity_on(self, priority, now):
        return self._input[priority] and ((now - self._input[priority]['timestamp']) < self.publisher_timeout)

    def _publish_velocity(self):
        if self._accept_inputs:
            now = time()

            if self._received_velocity_on('high_priority', now):
                self._publisher.publish(self._input['high_priority']['velocity'])
            elif self._received_velocity_on('low_priority', now):
                self._publisher.publish(self._input['low_priority']['velocity'])
            else:
                self._publish_stop()


def main(args=None):
    rclpy.init(args=args)
    rclpy.spin(VelocityMultiplexer())
    rclpy.shutdown()


if __name__ == '__main__':
    main()
