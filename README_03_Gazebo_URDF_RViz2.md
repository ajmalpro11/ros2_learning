# 03 — Gazebo Simulation + URDF Robot Models + RViz2

**Date completed:** May 2026  
**Goal:** Visualize and control robot models using URDF, RViz2 and understand joint states  
**Project series:** Mechatronics & Robotics Learning Journey  
**GitHub:** [ajmalpro11](https://github.com/ajmalpro11)

---

## What was achieved

- Installed Gazebo Harmonic simulator
- Launched Turtlebot4 in a warehouse simulation
- Loaded URDF robot models in RViz2
- Controlled robot joints using the Joint State Publisher sliders
- Observed `/joint_states` topic updating in real time as joints move
- Understood the full control loop of a robotic arm in ROS 2

---

## Key concepts learned

| Concept | Simple explanation |
|---|---|
| URDF | XML file that describes a robot — its links, joints, and dimensions |
| Link | A rigid body part of a robot (like an arm segment or wheel) |
| Joint | A connection between two links that can move (rotate or slide) |
| RViz2 | A 3D visualization tool for ROS 2 — shows robot models and sensor data |
| Gazebo | A full physics simulator — robots move, fall, collide realistically |
| `/joint_states` | The most important topic in robotics — publishes every joint's current angle |
| Joint State Publisher | A tool that lets you manually control joint angles via sliders |

---

## The Pareto insight

The `/joint_states` topic is the foundation of all robot control:
- **Slider moves** → Joint State Publisher sends angles to `/joint_states`
- **RViz2 subscribes** to `/joint_states` → robot model moves on screen
- **Real robot arm** → motor controller reads `/joint_states` → physical motors move

A robotic arm is just this loop, with joints named `shoulder`, `elbow`, `wrist` instead of `wheel` and `gripper`.

---

## Tools installed

```bash
# Gazebo Harmonic (integrated with ROS 2 Jazzy)
sudo apt install -y ros-jazzy-ros-gz

# Turtlebot4 simulator
sudo apt install -y ros-jazzy-turtlebot4-simulator ros-jazzy-turtlebot4-description

# URDF tutorial package
sudo apt install -y ros-jazzy-urdf-tutorial

# Keyboard teleop
sudo apt install -y ros-jazzy-teleop-twist-keyboard
```

---

## How to launch Gazebo

```bash
source /opt/ros/jazzy/setup.bash

# Launch empty Gazebo world
gz sim

# Launch diff drive demo (two robots on flat surface)
ros2 launch ros_gz_sim gz_sim.launch.py gz_args:="-r diff_drive.sdf"

# Launch Turtlebot4 in warehouse
ros2 launch turtlebot4_gz_bringup turtlebot4_gz.launch.py
```

---

## How to launch RViz2 with URDF models

```bash
source /opt/ros/jazzy/setup.bash

# Single link robot (cylinder)
ros2 launch urdf_tutorial display.launch.py model:=urdf/01-myfirst.urdf

# Multi-link robot with legs and head
ros2 launch urdf_tutorial display.launch.py model:=urdf/06-flexible.urdf

# Full robot with moveable joints + slider panel
ros2 launch urdf_tutorial display.launch.py model:=urdf/08-macroed.urdf.xacro
```

---

## The joint states topic

```bash
# Watch joint angles update in real time
ros2 topic echo /joint_states
```

Example output:
```
name:
- right_front_wheel_joint
- left_gripper_joint
- right_gripper_joint
- head_swivel
position:
- 0.797
- 0.370
- 0.423
- 0.016
```

Each `position` value is the joint angle in **radians**. Moving a slider changes this value in real time.

---

## URDF structure (what you'll write for your robotic arm)

```xml
<?xml version="1.0"?>
<robot name="my_arm">

  <!-- Base link -->
  <link name="base_link">
    <visual>
      <geometry>
        <cylinder length="0.1" radius="0.05"/>
      </geometry>
    </visual>
  </link>

  <!-- First arm segment -->
  <link name="shoulder_link">
    <visual>
      <geometry>
        <cylinder length="0.2" radius="0.03"/>
      </geometry>
    </visual>
  </link>

  <!-- Joint connecting base to shoulder -->
  <joint name="shoulder_joint" type="revolute">
    <parent link="base_link"/>
    <child link="shoulder_link"/>
    <axis xyz="0 0 1"/>
    <limit lower="-1.57" upper="1.57" effort="10" velocity="1"/>
  </joint>

</robot>
```

This is the exact structure you'll use for the robotic arm project.

---

## RViz2 navigation

| Action | Control |
|---|---|
| Rotate view | Left click + drag |
| Zoom | Scroll wheel |
| Pan | Middle click + drag |

---

## How to open Ubuntu next time

```powershell
wsl -d Ubuntu-24.04 -u ajumal
```

Then source ROS 2:
```bash
source /opt/ros/jazzy/setup.bash
source ~/ros2_ws/install/setup.bash
```

---

## Next session — Session 4

- [ ] Write your first URDF file from scratch
- [ ] Build a simple 3-joint robotic arm in URDF
- [ ] Visualize it in RViz2 with moveable joints
- [ ] Understand coordinate frames and transforms (TF)

---

## Full learning roadmap

| Phase | Topic | Status |
|---|---|---|
| 1 | WSL2 + Ubuntu + ROS 2 setup | ✅ Done |
| 2 | ROS 2 nodes, topics, publisher, subscriber | ✅ Done |
| 3 | Gazebo simulation + URDF + RViz2 + joint states | ✅ Done |
| 4 | Write your own URDF — 3 joint robotic arm | 🔜 Next |
| 5 | Control the arm with ROS 2 nodes | ⏳ Upcoming |
| 6 | Robotic arm capstone project on GitHub | ⏳ Final goal |
