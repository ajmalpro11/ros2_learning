import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32

class TemperatureReader(Node):

    def __init__(self):
        super().__init__('temperature_reader')
        self.subscription = self.create_subscription(
            Float32,
            '/temperature',
            self.temperature_callback,
            10)
        self.get_logger().info('Temperature reader started!')

    def temperature_callback(self, msg):
        temp = msg.data
        self.get_logger().info(f'Received temperature: {temp} °C')

        if temp > 30.0:
            self.get_logger().warn(f'WARNING: Temperature too high! {temp} °C')

def main():
    rclpy.init()
    node = TemperatureReader()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()
