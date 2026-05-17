import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState

class PickAndPlace(Node):

    def __init__(self):
        super().__init__("pick_and_place")
        self.publisher = self.create_publisher(JointState, "/joint_states", 10)
        self.timer = self.create_timer(0.05, self.run)
        self.positions = {
            "home":  [0.0,  0.0,  0.0],
            "reach": [0.8,  0.5,  0.0],
            "pick":  [0.8,  1.0,  0.5],
            "place": [-0.8, 0.5,  0.0],
        }
        self.sequence = ["home", "reach", "pick", "reach", "place", "home"]
        self.current_step = 0
        self.current_angles = [0.0, 0.0, 0.0]
        self.step_hold_time = 10
        self.hold_counter = 0

    def interpolate(self, current, target, speed=0.15):
        result = []
        done = True
        for c, t in zip(current, target):
            diff = t - c
            if abs(diff) > speed:
                c += speed * (1 if diff > 0 else -1)
                done = False
            else:
                c = t
            result.append(round(c, 4))
        return result, done

    def run(self):
        step_name = self.sequence[self.current_step]
        target = self.positions[step_name]
        self.current_angles, done = self.interpolate(self.current_angles, target)
        if done:
            self.hold_counter += 1
            if self.hold_counter >= self.step_hold_time:
                self.hold_counter = 0
                self.current_step = (self.current_step + 1) % len(self.sequence)
                next_step = self.sequence[self.current_step]
                self.get_logger().info(f"Moving to: {next_step}")
        msg = JointState()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.name = ["shoulder_joint", "elbow_joint", "wrist_joint"]
        msg.position = self.current_angles
        self.publisher.publish(msg)

def main():
    rclpy.init()
    node = PickAndPlace()
    rclpy.spin(node)
    rclpy.shutdown()
