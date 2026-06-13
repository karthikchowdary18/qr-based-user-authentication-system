# QR-Based User Authentication System Using Camera Input

ROS 2 node for camera-based user authentication using QR decoding and topic-driven system-state communication.

**Author:** Karthik Chowdary Nunna  
**Timeline:** Dec 2025 - Jan 2026  
**Package:** `user_authorization`

## Project Summary

This project implements a ROS 2 authentication node for an autonomous shuttle access workflow. The node receives an approved login ID from a backend service, reads Intel RealSense RGB camera frames, decodes QR payloads, and publishes an authentication decision that downstream systems can use for actions such as door unlocking.

## Highlights

- Designed and implemented a ROS 2 node for camera-based user authentication.
- Integrated backend state, camera input, and downstream control through ROS 2 topics.
- Processed Intel RealSense RGB streams with `cv_bridge` and decoded QR codes with `pyzbar`.
- Published authentication results as a boolean ROS 2 topic for system-level coordination.
- Added robustness features including invalid QR filtering and repeated-state suppression.
- Included unit tests for authentication success, failure, duplicate-state handling, and node startup.

## System Workflow

1. Backend publishes the approved user ID on `/auth/login_id`.
2. The node receives RGB frames from `/robot1/D455_1/color/image_raw`.
3. QR payloads are decoded and validated against the format `ELDRIVE:<USER_ID>`.
4. Manual fallback input can be received from `/auth/user_input`.
5. The received ID is compared against the approved backend ID.
6. The result is published on `/user_auth_done` for downstream behavior such as door unlocking.

## ROS 2 Interfaces

### Subscribers

- `/auth/login_id` with `std_msgs/String`
- `/auth/user_input` with `std_msgs/String`
- `/robot1/D455_1/color/image_raw` with `sensor_msgs/Image`

### Publisher

- `/user_auth_done` with `std_msgs/Bool`

## Technical Stack

- ROS 2
- Python
- OpenCV
- `cv_bridge`
- `pyzbar`
- Intel RealSense RGB camera
- Linux

## Repository Structure

```text
user_authorization/
|- user_authorization/
|  |- user_authorization.py
|- test/
|  |- conftest.py
|  |- test_flake8.py
|  |- test_pep257.py
|  |- test_user_authorization.py
|- package.xml
|- setup.py
|- README.md
```

## Running the Node

### Prerequisites

- ROS 2 workspace configured on Linux
- Python dependencies required by the node
- Intel RealSense RGB stream available on the configured topic

### Build and Run

```bash
colcon build
source install/setup.bash
ros2 run user_authorization user_authorization
```

## What This Project Demonstrates

- Robotics software integration with ROS 2 publishers and subscribers
- Computer-vision-based authentication using live camera input
- Defensive validation of external inputs
- State-aware event publishing for reliable downstream behavior
