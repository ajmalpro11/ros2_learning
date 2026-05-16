# 01 — WSL2 + ROS 2 Jazzy Setup on Windows

**Date completed:** May 2026  
**Goal:** Install Ubuntu 24.04 and ROS 2 Jazzy on a Windows PC without dual booting  
**Project series:** Mechatronics & Robotics Learning Journey  
**GitHub:** [ajmalpro11](https://github.com/ajmalpro11)

---

## What was achieved

- Installed Ubuntu 24.04 LTS inside Windows using WSL2
- Moved Ubuntu installation to D: drive (HDD) to preserve C: SSD space
- Created a personal Linux user account (`ajumal`)
- Installed ROS 2 Jazzy Desktop (full installation)
- Verified ROS 2 with a working publisher/subscriber demo

---

## System info

| Item | Details |
|---|---|
| Windows version | 10.0.19045.6466 |
| WSL version | 2.4.10.0 |
| WSLg version | 1.0.65 (enables Gazebo GUI) |
| Ubuntu version | 24.04.4 LTS (Noble) |
| ROS 2 version | Jazzy Jalopy |
| Ubuntu location | D:\WSL\Ubuntu-24.04 (HDD, not SSD) |
| Linux username | ajumal |

---

## What is WSL2?

WSL2 (Windows Subsystem for Linux 2) is a feature built into Windows that lets you run a full Ubuntu Linux environment inside a terminal window — without rebooting or dual booting. Windows and Ubuntu run at the same time.

WSLg is an extension that allows Linux GUI applications (like Gazebo 3D simulator) to open as normal Windows on your desktop.

---

## Step-by-step: what was done

### 1. Verify WSL2 is available

```powershell
wsl --version
```

Expected output includes `WSL version: 2.x.x` and `WSLg version: 1.x.x`.

---

### 2. Create folder on D: drive

```powershell
mkdir D:\WSL\Ubuntu-24.04
```

---

### 3. Install Ubuntu 24.04

```powershell
wsl --install -d Ubuntu-24.04
```

---

### 4. Export Ubuntu to D: drive

```powershell
wsl --export Ubuntu-24.04 D:\ubuntu-backup.tar
```

---

### 5. Remove from C: drive

```powershell
wsl --unregister Ubuntu-24.04
```

---

### 6. Import into D: drive

```powershell
wsl --import Ubuntu-24.04 D:\WSL\Ubuntu-24.04 D:\ubuntu-backup.tar
```

---

### 7. Delete backup file

```powershell
Remove-Item D:\ubuntu-backup.tar
```

---

### 8. Launch Ubuntu and create user

```powershell
wsl -d Ubuntu-24.04
```

Inside Ubuntu:

```bash
useradd -m -s /bin/bash ajumal
passwd ajumal
usermod -aG sudo ajumal
exit
```

---

### 9. Launch as your user

```powershell
wsl -d Ubuntu-24.04 -u ajumal
```

---

### 10. Set default user in wsl.conf

```bash
sudo sh -c "echo '[user]\ndefault=ajumal' >> /etc/wsl.conf"
```

---

### 11. Update Ubuntu

```bash
sudo apt update && sudo apt upgrade -y
```

---

### 12. Install ROS 2 Jazzy

```bash
# Add curl and software tools
sudo apt install -y software-properties-common curl

# Add ROS 2 GPG key
sudo curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.key \
  -o /usr/share/keyrings/ros-archive-keyring.gpg

# Add ROS 2 repository
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] \
  http://packages.ros.org/ros2/ubuntu \
  $(. /etc/os-release && echo $UBUNTU_CODENAME) main" | \
  sudo tee /etc/apt/sources.list.d/ros2.list > /dev/null

# Update and install
sudo apt update
sudo apt install -y ros-jazzy-desktop
```

---

### 13. Configure ROS 2 environment

```bash
echo "source /opt/ros/jazzy/setup.bash" >> ~/.bashrc
source ~/.bashrc
```

---

### 14. Verify with demo nodes

Open two Ubuntu terminals:

**Terminal 1 — publisher (talker):**
```bash
ros2 run demo_nodes_cpp talker
```

**Terminal 2 — subscriber (listener):**
```bash
ros2 run demo_nodes_cpp listener
```

Expected: Terminal 1 prints `Publishing: Hello World: 1, 2, 3...`  
Terminal 2 prints `I heard: Hello World: 1, 2, 3...`

This confirms ROS 2 nodes can communicate over topics — the foundation of all ROS 2 robotics systems.

---

## How to reopen Ubuntu next time

Open PowerShell and run:

```powershell
wsl -d Ubuntu-24.04 -u ajumal
```

---

## Key concepts learned

| Concept | What it means |
|---|---|
| Node | A single program in ROS 2 (e.g. a sensor reader, a motor controller) |
| Topic | A named channel nodes use to send/receive messages |
| Publisher | A node that sends messages to a topic |
| Subscriber | A node that receives messages from a topic |
| `ros2 topic list` | Lists all active topics in the ROS 2 network |

---

## Next session — Phase 2

- [ ] Create your first custom ROS 2 Python node
- [ ] Understand ROS 2 workspaces and packages (`colcon build`)
- [ ] Install Gazebo Harmonic simulator
- [ ] Drive a simulated robot in a virtual environment

---

## Full learning roadmap

| Phase | Topic | Status |
|---|---|---|
| 1 | WSL2 + Ubuntu + ROS 2 setup | ✅ Done |
| 2 | ROS 2 nodes, topics, workspaces | 🔜 Next |
| 3 | Gazebo simulation + URDF robot model | ⏳ Upcoming |
| 4 | SLAM mapping + Nav2 navigation | ⏳ Upcoming |
| 5 | Robotic arm / capstone project | ⏳ Final goal |
