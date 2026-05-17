# 05 — Arm Controller Node: Automated Joint Motion

**Date completed:** May 2026  
**Goal:** Write a ROS 2 Python node that moves the robotic arm automatically  
**Project series:** Mechatronics & Robotics Learning Journey  
**GitHub:** [ajmalpro11](https://github.com/ajmalpro11)

---

## What was achieved

- Wrote a Python node that publishes joint angles to `/joint_states`
- Arm moves automatically in a smooth sine wave motion
- All 3 joints (shoulder, elbow, wrist) move at different phases
- Recorded a GIF of the moving arm and added it to GitHub homepage
- Understood the full control loop: Python node → topic → RViz2 → motion

---

## The key insight

This is how every real robot arm works:

```
Python node calculates joint angles
        ↓
Publishes to /joint_states topic
        ↓
Robot (RViz2 or real hardware) subscribes
        ↓
Motors move to those angles
```

The only difference between this simulation and a real robot arm is the last step — instead of RViz2, a real motor driver reads `/joint_states` and moves physical motors.

---

## The arm controller node

**File:** `my_robot_arm/my_robot_arm/arm_controller.py`

```python
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState
import math

class ArmController(Node):

    def __init__(self):
        super().__init__('arm_controller')
        self.publisher = self.create_publisher(JointState, '/joint_states', 10)
        self.timer = self.create_timer(0.1, self.move_arm)
        self.t = 0.0
        self.get_logger().info('Arm controller started!')

    def move_arm(self):
        msg = JointState()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.name = ['shoulder_joint', 'elbow_joint', 'wrist_joint']

        # Smooth wave motion using sine wave
        shoulder = 1.0 * math.sin(self.t)
        elbow    = 0.8 * math.sin(self.t + 1.0)
        wrist    = 0.5 * math.sin(self.t + 2.0)

        msg.position = [shoulder, elbow, wrist]
        self.publisher.publish(msg)
        self.t += 0.05

def main():
    rclpy.init()
    node = ArmController()
    rclpy.spin(node)
    rclpy.shutdown()
```

---

## Key concepts explained

### JointState message
```python
from sensor_msgs.msg import JointState

msg = JointState()
msg.header.stamp = self.get_clock().now().to_msg()  # timestamp
msg.name = ['shoulder_joint', 'elbow_joint', 'wrist_joint']  # joint names
msg.position = [0.5, -0.3, 0.8]  # angles in radians
```

Joint names must match exactly what's in your URDF file.

### Sine wave motion
```python
import math
angle = amplitude * math.sin(time + phase_offset)
```

| Parameter | Effect |
|---|---|
| amplitude | How far the joint moves (1.0 = ~57 degrees) |
| time (t) | Increases every step — drives the wave |
| phase_offset | Shifts when each joint peaks — creates wave effect |

### Radians vs degrees
| Degrees | Radians |
|---|---|
| 0° | 0.0 |
| 45° | 0.785 |
| 90° | 1.57 |
| 180° | 3.14 |

---

## How to run

**Terminal 1 — visualize the arm:**
```bash
source /opt/ros/jazzy/setup.bash
source ~/ros2_ws/install/setup.bash
ros2 launch urdf_tutorial display.launch.py model:=$(ros2 pkg prefix my_robot_arm)/share/my_robot_arm/urdf/arm.urdf
```

**Terminal 2 — run the controller:**
```bash
source /opt/ros/jazzy/setup.bash
source ~/ros2_ws/install/setup.bash
ros2 run my_robot_arm arm_controller
```

Watch the arm move automatically in RViz2!

---

## Useful commands

```bash
# Watch joint angles updating in real time
ros2 topic echo /joint_states

# Check the node is running
ros2 node list

# Check what topics are active
ros2 topic list
```

---

## Why GIF over video for GitHub

| | GIF | MP4 Video |
|---|---|---|
| GitHub README | Plays automatically | Needs a click |
| File size | Larger | Smaller |
| Loop | Yes | No |
| Best for | GitHub, Slack, email | LinkedIn, YouTube |

Always use GIF in your GitHub README — recruiters see your robot moving instantly without clicking anything.

---

## Next session — Session 6 (Final Project)

- [ ] Add the arm to Gazebo with physics
- [ ] Add a target object to pick up
- [ ] Write a pick and place controller node
- [ ] Full demo recording for GitHub

---

## Full learning roadmap

| Phase | Topic | Status |
|---|---|---|
| 1 | WSL2 + Ubuntu + ROS 2 setup | ✅ Done |
| 2 | ROS 2 nodes, topics, publisher, subscriber | ✅ Done |
| 3 | Gazebo simulation + URDF + RViz2 + joint states | ✅ Done |
| 4 | Write your own URDF — 3 joint robotic arm | ✅ Done |
| 5 | Control the arm with ROS 2 Python nodes | ✅ Done |
| 6 | Pick and place capstone project on GitHub | 🔜 Next |
