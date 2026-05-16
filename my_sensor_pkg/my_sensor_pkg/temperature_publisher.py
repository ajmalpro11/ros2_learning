import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32
import random

class TemperatureSensor(Node):

    def __init__(self):
        super().__init__('temperature_sensor')
        self.publisher = self.create_publisher(Float32, '/temperature', 10)
        self.timer = self.create_timer(1.0, self.publish_temperature)
        self.get_logger().info('Temperature sensor started!')

    def publish_temperature(self):
        msg = Float32()
        msg.data = round(random.uniform(20.0, 35.0), 2)
        self.publisher.publish(msg)
        self.get_logger().info(f'Publishing temperature: {msg.data} °C')

def main():
    rclpy.init()
    node = TemperatureSensor()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()
