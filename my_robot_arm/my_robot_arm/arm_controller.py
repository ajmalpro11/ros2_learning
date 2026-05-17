import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState
import math
import time

class ArmController(Node):

    def __init__(self):
        super().__init__('arm_controller')
        
        # Publisher to joint states topic
        self.publisher = self.create_publisher(JointState, '/joint_states', 10)
        
        # Timer - runs every 0.1 seconds
        self.timer = self.create_timer(0.1, self.move_arm)
        
        # Track time for smooth motion
        self.t = 0.0
        
        self.get_logger().info('Arm controller started!')

    def move_arm(self):
        msg = JointState()
        msg.header.stamp = self.get_clock().now().to_msg()
        
        # Joint names must match your URDF exactly
        msg.name = ['shoulder_joint', 'elbow_joint', 'wrist_joint']
        
        # Smooth wave motion using sine wave
        shoulder = 1.0 * math.sin(self.t)
        elbow    = 0.8 * math.sin(self.t + 1.0)
        wrist    = 0.5 * math.sin(self.t + 2.0)
        
        msg.position = [shoulder, elbow, wrist]
        
        self.publisher.publish(msg)
        self.t += 0.05  # increment time

def main():
    rclpy.init()
    node = ArmController()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()
