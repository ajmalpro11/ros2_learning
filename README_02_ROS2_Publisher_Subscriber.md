# 02 — First ROS 2 Nodes: Publisher & Subscriber

**Date completed:** May 2026  
**Goal:** Build a temperature sensor system using ROS 2 publisher and subscriber nodes  
**Project series:** Mechatronics & Robotics Learning Journey  
**GitHub:** [ajmalpro11](https://github.com/ajmalpro11)

---

## What was achieved

- Created a ROS 2 workspace and Python package from scratch
- Built a temperature publisher node that sends fake sensor data every second
- Built a temperature subscriber node that receives data and warns if too high
- Verified two nodes communicating live through a ROS 2 topic

---

## Core concepts learned

| Concept | Simple explanation |
|---|---|
| Node | A single Python program that does one job |
| Topic | A named channel nodes use to talk — like a WhatsApp group |
| Publisher | A node that sends messages to a topic |
| Subscriber | A node that receives messages from a topic |
| Message type | The format of data sent — e.g. `Float32` for a number |
| `colcon build` | Compiles your package so ROS 2 can find and run it |
| `source setup.bash` | Activates ROS 2 and your workspace in the terminal |

---

## The Pareto insight

These 4 things — **node, topic, publisher, subscriber** — cover 80% of all ROS 2 systems.  
A real robot is just many nodes publishing and subscribing to many topics.  
A LiDAR publishes to `/scan`. A camera publishes to `/image`. A motor listens to `/cmd_vel`.  
The structure is always the same.

---

## Project structure

```
ros2_learning/
└── my_sensor_pkg/
    ├── my_sensor_pkg/
    │   ├── __init__.py
    │   ├── temperature_publisher.py    ← publisher node
    │   └── temperature_subscriber.py  ← subscriber node
    ├── package.xml
    ├── setup.cfg
    └── setup.py
```

---

## The publisher node

**File:** `my_sensor_pkg/temperature_publisher.py`

```python
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
```

**What each part does:**
- `create_publisher(Float32, '/temperature', 10)` — creates a publisher on the `/temperature` topic using Float32 message type. `10` is the queue size.
- `create_timer(1.0, self.publish_temperature)` — calls `publish_temperature` every 1 second
- `rclpy.spin(node)` — keeps the node alive and running

---

## The subscriber node

**File:** `my_sensor_pkg/temperature_subscriber.py`

```python
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
```

**What each part does:**
- `create_subscription(Float32, '/temperature', self.temperature_callback, 10)` — listens to `/temperature` topic and calls `temperature_callback` whenever a message arrives
- `temperature_callback(self, msg)` — runs automatically every time a message is received
- `msg.data` — the actual float number inside the message

---

## How to build and run

### Build the package
```bash
cd ~/ros2_ws
colcon build --packages-select my_sensor_pkg
```

### Activate the workspace (run in every new terminal)
```bash
source /opt/ros/jazzy/setup.bash
source ~/ros2_ws/install/setup.bash
```

### Run the publisher (Terminal 1)
```bash
ros2 run my_sensor_pkg temperature_publisher
```

### Run the subscriber (Terminal 2)
```bash
ros2 run my_sensor_pkg temperature_subscriber
```

### Inspect the topic directly (any terminal)
```bash
ros2 topic echo /temperature
```

---

## Useful ROS 2 commands learned

```bash
ros2 topic list              # list all active topics
ros2 topic echo /topic_name  # print messages on a topic live
ros2 node list               # list all running nodes
ros2 pkg create              # create a new package
colcon build                 # build all packages in workspace
```

---

## How to open Ubuntu next time

```powershell
wsl -d Ubuntu-24.04 -u ajumal
```

---

## Next session — Phase 3

- [ ] Install Gazebo Harmonic simulator
- [ ] Load a pre-built robot model in Gazebo
- [ ] Drive the robot using ROS 2 topics from the terminal
- [ ] Understand URDF — how robots are described in code

---

## Full learning roadmap

| Phase | Topic | Status |
|---|---|---|
| 1 | WSL2 + Ubuntu + ROS 2 setup | ✅ Done |
| 2 | ROS 2 nodes, topics, publisher, subscriber | ✅ Done |
| 3 | Gazebo simulation + drive a robot | 🔜 Next |
| 4 | URDF — build your own robot model | ⏳ Upcoming |
| 5 | SLAM mapping + Nav2 navigation | ⏳ Upcoming |
| 6 | Robotic arm capstone project | ⏳ Final goal |
