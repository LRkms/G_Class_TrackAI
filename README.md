# Smart Stereo Vision-Based Autonomous RC Car

This project is a stereo vision-based smart autonomous 4WD RC car built using Jetson Nano and STM32F411RE.

Unlike traditional systems that rely on ultrasonic sensors or LiDAR, this car uses two fixed USB cameras for stereo vision to estimate object distance, enabling real-time obstacle avoidance and line tracking with AI support.

---

## 🔧 System Overview

### 🧠 Main Controller
- **Jetson Nano B01**
  - Runs object detection models (e.g., YOLO)
  - Calculates depth from stereo images
  - Sends driving commands to STM32 via UART

### ⚙️ Hardware Control Unit
- **STM32F411RE**
  - Controls 4WD motors and servo (MG996)
  - Executes commands received from Jetson Nano

### 🛠️ Hardware Components
| Component | Description |
|----------|-------------|
| **Motors (4WD)** | For vehicle movement, driven via ESC |
| **MG996 Servo (x1)** | Controls gear shifting or front-wheel steering |
| **USB Cameras (x2)** | OV9732 720P modules for stereo vision (fixed mount, no gimbal) |
| **3D Printed Frame** | Based on G-Wagon body style |
| **Battery (2S LiPo)** | Powers motors and electronics separately |

---

## 🎯 Key Features
- Stereo vision-based depth estimation (no ultrasonic or LiDAR)
- Real-time obstacle detection and avoidance
- AI-based object recognition (face, color, palm, gesture)
- Line tracking using OpenCV
- UART communication between Jetson Nano and STM32

---

## ✅ Project Goal
To create a low-cost, vision-based autonomous RC car by integrating AI perception with embedded hardware control, enabling it to make reactive decisions similar to real-world autonomous vehicles.

