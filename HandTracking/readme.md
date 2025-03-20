# Hand Tracking and Gesture-Based Volume Control

This project implements a **real-time hand tracking system** using **Python, OpenCV, and MediaPipe** to detect hand gestures and control system volume. It allows users to adjust their system volume by moving their fingers in front of the camera. This is a practical example of computer vision and human-computer interaction.

## Features

- **Hand Tracking**: Uses **MediaPipe** to detect hand landmarks in real-time.
- **Gesture-Based Volume Control**: Maps finger distance to system volume using **NumPy interpolation**.
- **AppleScript Integration**: Adjusts macOS system volume automatically.
- **Visual Feedback**: Displays detected hands, distance lines, and a dynamic volume bar using **OpenCV**.
- **Optimized Performance**: Runs efficiently with real-time processing.

## Installation

1. **Clone the Repository**:
    ```bash
    git clone https://github.com/ZaidIslam1/PortfolioProjects.git
    cd PortfolioProjects/HandTracking
    ```

3. **Run the Application**:
    ```bash
    python VolumeControl.py
    ```

## Usage

- **Move Index and Thumb**: Adjusts system volume based on their distance.
- **Hand Visualization**: The interface highlights finger positions and volume bar changes.
- **Press 'ctrl+c'**: Exits the application.

## Files Overview

- **HandTrackingModule.py**: Defines the `HandDetector` class for detecting and processing hand landmarks.
- **VolumeControl.py**: Main script that captures video, detects hands, and adjusts volume dynamically.

This project demonstrates the power of **computer vision** and **gesture recognition** for intuitive user interactions.

