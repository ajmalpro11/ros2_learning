# 04 — Building a 3-Joint Robotic Arm in URDF

**Date completed:** May 2026  
**Goal:** Write a URDF file from scratch and visualize a 3-joint robotic arm in RViz2  
**Project series:** Mechatronics & Robotics Learning Journey  
**GitHub:** [ajmalpro11](https://github.com/ajmalpro11)

---

## What was achieved

- Created a new ROS 2 package `my_robot_arm` from scratch
- Wrote a complete URDF file describing a 3-joint robotic arm
- Visualized the arm in RViz2 with moveable joints
- Controlled shoulder, elbow and wrist joints using sliders
- Added robot arm screenshot to GitHub repo homepage

---

## The robotic arm structure

```
base_link
    └── shoulder_joint (revolute - rotates around Z axis)
            └── upper_arm_link
                    └── elbow_joint (revolute - rotates around Y axis)
                            └── forearm_link
                                    └── wrist_joint (revolute - rotates around Y axis)
                                            └── gripper_link
```

| Link | Shape | Color | Description |
|---|---|---|---|
| base_link | Cylinder | Blue | Fixed base, mounted to ground |
| upper_arm_link | Cylinder | Red | First arm segment |
| forearm_link | Cylinder | Green | Second arm segment |
| gripper_link | Box | Yellow | End effector |

| Joint | Type | Axis | Range |
|---|---|---|---|
| shoulder_joint | revolute | Z | -90° to +90° |
| elbow_joint | revolute | Y | -90° to +90° |
| wrist_joint | revolute | Y | -90° to +90° |

---

## The complete URDF file

**File:** `my_robot_arm/urdf/arm.urdf`

```xml
<?xml version="1.0"?>
<robot name="my_robot_arm">

  <!-- BASE LINK - fixed to ground -->
  <link name="base_link">
    <visual>
      <geometry>
        <cylinder length="0.1" radius="0.07"/>
      </geometry>
      <material name="blue">
        <color rgba="0 0 0.8 1"/>
      </material>
    </visual>
  </link>

  <!-- UPPER ARM LINK -->
  <link name="upper_arm_link">
    <visual>
      <origin xyz="0 0 0.15" rpy="0 0 0"/>
      <geometry>
        <cylinder length="0.3" radius="0.03"/>
      </geometry>
      <material name="red">
        <color rgba="0.8 0 0 1"/>
      </material>
    </visual>
  </link>

  <!-- SHOULDER JOINT - connects base to upper arm -->
  <joint name="shoulder_joint" type="revolute">
    <parent link="base_link"/>
    <child link="upper_arm_link"/>
    <origin xyz="0 0 0.05" rpy="0 0 0"/>
    <axis xyz="0 0 1"/>
    <limit lower="-1.57" upper="1.57" effort="10" velocity="1"/>
  </joint>

  <!-- FOREARM LINK -->
  <link name="forearm_link">
    <visual>
      <origin xyz="0 0 0.125" rpy="0 0 0"/>
      <geometry>
        <cylinder length="0.25" radius="0.025"/>
      </geometry>
      <material name="green">
        <color rgba="0 0.8 0 1"/>
      </material>
    </visual>
  </link>

  <!-- ELBOW JOINT - connects upper arm to forearm -->
  <joint name="elbow_joint" type="revolute">
    <parent link="upper_arm_link"/>
    <child link="forearm_link"/>
    <origin xyz="0 0 0.3" rpy="0 0 0"/>
    <axis xyz="0 1 0"/>
    <limit lower="-1.57" upper="1.57" effort="10" velocity="1"/>
  </joint>

  <!-- GRIPPER LINK -->
  <link name="gripper_link">
    <visual>
      <geometry>
        <box size="0.08 0.08 0.04"/>
      </geometry>
      <material name="yellow">
        <color rgba="0.8 0.8 0 1"/>
      </material>
    </visual>
  </link>

  <!-- WRIST JOINT - connects forearm to gripper -->
  <joint name="wrist_joint" type="revolute">
    <parent link="forearm_link"/>
    <child link="gripper_link"/>
    <origin xyz="0 0 0.25" rpy="0 0 0"/>
    <axis xyz="0 1 0"/>
    <limit lower="-1.57" upper="1.57" effort="10" velocity="1"/>
  </joint>

</robot>
```

---

## Key URDF concepts

### Link structure
```xml
<link name="link_name">
  <visual>
    <origin xyz="x y z" rpy="roll pitch yaw"/>  <!-- position offset -->
    <geometry>
      <cylinder length="0.3" radius="0.03"/>     <!-- shape -->
    </geometry>
    <material name="red">
      <color rgba="0.8 0 0 1"/>                  <!-- color (r g b alpha) -->
    </material>
  </visual>
</link>
```

### Joint structure
```xml
<joint name="joint_name" type="revolute">
  <parent link="parent_link_name"/>   <!-- where joint starts -->
  <child link="child_link_name"/>     <!-- what it moves -->
  <origin xyz="0 0 0.3" rpy="0 0 0"/> <!-- position relative to parent -->
  <axis xyz="0 1 0"/>                 <!-- rotation axis (Y axis here) -->
  <limit lower="-1.57" upper="1.57"  <!-- joint limits in radians -->
         effort="10" velocity="1"/>
</joint>
```

### Joint types
| Type | Behaviour | Example |
|---|---|---|
| revolute | Rotates with limits | Elbow, shoulder |
| continuous | Rotates without limits | Wheel |
| prismatic | Slides linearly | Linear actuator |
| fixed | No movement | Camera mount |

### Rotation axes
| Axis | Direction | Typical use |
|---|---|---|
| xyz="1 0 0" | X axis | Roll |
| xyz="0 1 0" | Y axis | Pitch (elbow bend) |
| xyz="0 0 1" | Z axis | Yaw (shoulder rotate) |

---

## How to visualize your arm

```bash
source /opt/ros/jazzy/setup.bash
source ~/ros2_ws/install/setup.bash
ros2 launch urdf_tutorial display.launch.py model:=$(ros2 pkg prefix my_robot_arm)/share/my_robot_arm/urdf/arm.urdf
```

---

## How to build the package

```bash
cd ~/ros2_ws
colcon build --packages-select my_robot_arm
source ~/ros2_ws/install/setup.bash
```

---

## What the joint sliders do

Moving the sliders publishes to `/joint_states` topic:
```bash
# Watch joint angles in real time
ros2 topic echo /joint_states
```

This is the same topic a real robot motor controller reads to know where to move each joint.

---

## Next session — Session 5

- [ ] Control the arm joints using a ROS 2 Python node
- [ ] Write a node that moves the arm to specific positions automatically
- [ ] Understand inverse kinematics basics
- [ ] Prepare for pick and place simulation

---

## Full learning roadmap

| Phase | Topic | Status |
|---|---|---|
| 1 | WSL2 + Ubuntu + ROS 2 setup | ✅ Done |
| 2 | ROS 2 nodes, topics, publisher, subscriber | ✅ Done |
| 3 | Gazebo simulation + URDF + RViz2 + joint states | ✅ Done |
| 4 | Write your own URDF — 3 joint robotic arm | ✅ Done |
| 5 | Control the arm with ROS 2 Python nodes | 🔜 Next |
| 6 | Pick and place capstone project on GitHub | ⏳ Final goal |
