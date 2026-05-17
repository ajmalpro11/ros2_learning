# 06 — Pick and Place Capstone Project

**Date completed:** May 2026  
**Goal:** Build a complete pick and place robotic arm simulation using ROS 2  
**Project series:** Mechatronics & Robotics Learning Journey  
**GitHub:** [ajmalpro11](https://github.com/ajmalpro11)

---

## What was achieved

- Built a complete pick and place motion sequence
- Arm moves smoothly through: home → reach → pick → reach → place → home
- Implemented smooth interpolation between joint positions
- Recorded and published demo GIF on GitHub homepage
- Completed the digital twin of a pick and place robotic arm

---

## The pick and place sequence

```
home  → all joints at zero, arm straight up
reach → shoulder rotates out, elbow bends toward target
pick  → elbow and wrist lower to grab object
reach → lift back up with object
place → shoulder swings to opposite side to drop
home  → return to start position
repeat
```

---

## Joint positions for each step

| Step | shoulder | elbow | wrist | Description |
|---|---|---|---|---|
| home | 0.0 | 0.0 | 0.0 | Rest position |
| reach | 0.8 | 0.5 | 0.0 | Extend toward object |
| pick | 0.8 | 1.0 | 0.5 | Lower to grab |
| place | -0.8 | 0.5 | 0.0 | Swing to drop position |

All values in radians.

---

## The complete pick and place node

**File:** `my_robot_arm/my_robot_arm/pick_and_place.py`

```python
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState

class PickAndPlace(Node):

    def __init__(self):
        super().__init__('pick_and_place')
        self.publisher = self.create_publisher(JointState, '/joint_states', 10)
        self.timer = self.create_timer(0.05, self.run)
        self.positions = {
            'home':  [0.0,  0.0,  0.0],
            'reach': [0.8,  0.5,  0.0],
            'pick':  [0.8,  1.0,  0.5],
            'place': [-0.8, 0.5,  0.0],
        }
        self.sequence = ['home', 'reach', 'pick', 'reach', 'place', 'home']
        self.current_step = 0
        self.current_angles = [0.0, 0.0, 0.0]
        self.step_hold_time = 10
        self.hold_counter = 0
        self.get_logger().info('Pick and Place started!')

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
                self.get_logger().info(f'Moving to: {next_step}')
        msg = JointState()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.name = ['shoulder_joint', 'elbow_joint', 'wrist_joint']
        msg.position = self.current_angles
        self.publisher.publish(msg)

def main():
    rclpy.init()
    node = PickAndPlace()
    rclpy.spin(node)
    rclpy.shutdown()
```

---

## Key concept: Interpolation

Interpolation is what makes the motion smooth instead of jumping instantly between positions:

```python
def interpolate(self, current, target, speed=0.15):
    # Instead of jumping: current = target
    # Move a small step toward target each tick
    diff = target - current
    if abs(diff) > speed:
        current += speed * direction  # small step
    else:
        current = target  # close enough, snap to target
```

This is the same principle used in real robot motion planning.

---

## How to run the full demo

**Terminal 1 — launch RViz2:**
```bash
source /opt/ros/jazzy/setup.bash
source ~/ros2_ws/install/setup.bash
ros2 launch urdf_tutorial display.launch.py model:=$(ros2 pkg prefix my_robot_arm)/share/my_robot_arm/urdf/arm.urdf jsp_gui:=false
```

**Terminal 2 — run pick and place:**
```bash
source /opt/ros/jazzy/setup.bash
source ~/ros2_ws/install/setup.bash
ros2 run my_robot_arm pick_and_place
```

Close the Joint State Publisher slider panel if it appears — it conflicts with the node.

---

## Speed tuning

| Parameter | Effect |
|---|---|
| `timer interval` | Lower = faster updates (0.05 = 20 times/sec) |
| `speed` in interpolate | Higher = faster joint movement |
| `step_hold_time` | Lower = shorter pause at each position |

---

## What's next — Real hardware vision based arm

The digital twin is complete. Next steps toward a real robot:

### Hardware needed
- Raspberry Pi 5 (already have)
- Pi Camera Module 3 (already have)
- 3x Servo motors (MG996R recommended)
- 3D printed arm links (design in Fusion 360)
- PCA9685 servo driver board
- Arduino (already have)

### Software stack for real robot
```
Pi Camera → OpenCV (object detection)
     ↓
ROS 2 node calculates target position
     ↓
Joint angles published to /joint_states
     ↓
Arduino reads angles via rosserial
     ↓
Servo motors move to position
```

### Vision based pick and place flow
1. Camera detects object color/shape using OpenCV
2. Calculates object position in 3D space
3. Inverse kinematics converts position to joint angles
4. Arm moves to pick position
5. Gripper closes
6. Arm moves to place position
7. Gripper opens

---

## Complete learning journey summary

| Session | Topic | Key skill gained |
|---|---|---|
| 01 | WSL2 + Ubuntu + ROS 2 | Linux environment setup |
| 02 | Publisher + Subscriber | ROS 2 communication |
| 03 | Gazebo + URDF + RViz2 | Robot visualization |
| 04 | 3-joint arm URDF | Robot description |
| 05 | Arm controller node | Automated joint control |
| 06 | Pick and place | Complete motion sequence |

---

## Skills demonstrated in this project

- ROS 2 Jazzy — nodes, topics, publishers, subscribers
- URDF — robot description with links and joints
- RViz2 — 3D robot visualization
- Python — robot control nodes
- Joint interpolation — smooth motion planning
- GitHub — documented portfolio with GIF demos
- Gazebo — physics simulation environment
