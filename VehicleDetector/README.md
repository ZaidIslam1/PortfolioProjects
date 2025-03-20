# Vehicle Detection and Counting

This project implements a **real-time vehicle detection and counting system** using **OpenCV** and **Background Subtraction**. It processes video footage to detect and count vehicles crossing a predefined line, making it useful for **traffic analysis, congestion monitoring, and automated vehicle tracking**.

## Features
- **Vehicle Detection**: Uses OpenCV's **background subtraction** and **contour detection** to identify vehicles.
- **Vehicle Counting**: Tracks vehicles crossing a defined counting line.
- **Adaptive Background Subtraction**: Uses **MOG (Mixture of Gaussians)** for dynamic background changes.
- **Configurable Line Positioning**: Customizable counting line for different video sources.
- **Efficient Processing**: Morphological operations to refine detected vehicle contours.

## Installation

1. **Clone the Repository**:
    ```bash
    git clone https://github.com/ZaidIslam1/PortfolioProjects.git
    cd PortfolioProjects/VehicleDetection
    ```

2. **Install Dependencies**:
    ```bash
    pip install opencv-python numpy
    ```

3. **Run the Application**:
    ```bash
    python vehicle_counter.py
    ```

## Usage
- Place the video file in the same directory as the script.
- **Modify `VIDEO_PATH`** in `vehicle_counter.py` to match your input video.
- Run the script to process the video and count the vehicles.
- Press **any key** to exit the application.

## Files Overview
- **vehicle_counter.py**: Main script for detecting and counting vehicles.
- **video.mp4**: Sample video file for testing (provide your own for real-world scenarios).

This project demonstrates the use of **computer vision** for traffic monitoring and vehicle analytics.

