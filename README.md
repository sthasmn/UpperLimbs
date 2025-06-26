# UpperLimbs - 3D Upper Body Movement Tracking

[![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A Python module for real-time 3D tracking of upper body and hand movements using a standard webcam, powered by Google's MediaPipe framework.

This tool captures pose and hand landmarks, transforms them into a unified coordinate system, and provides simple methods to access the raw 3D data or generate a live 3D visualization of the skeleton.

## Demo

![UpperLimbs Demo GIF](Demo/upperlimbs_demo.gif)
---

## Table of Contents
- [Features](#features)
- [How It Works](#how-it-works)
- [Installation](#installation)
- [Usage](#usage)
  - [Running the Demo](#running-the-demo)
  - [Programmatic Use](#programmatic-use)
- [API Reference](#api-reference)
- [Output Coordinate System](#output-coordinate-system)
- [Citation](#citation)
- [Dependencies](#dependencies)

---

## Features

- **Real-time Performance:** Tracks upper body and hand landmarks directly from a webcam or video file.
- **Unified 3D Coordinates:** Combines pose and hand landmarks into a single, easy-to-use data structure.
- **Shoulder-Centric Origin:** Transforms coordinates to a stable system with the origin at the center of the shoulders.
- **Live 3D Visualization:** Includes a built-in method to generate a dynamic 3D plot of the skeleton.
- **Simple API:** Designed to be easily integrated into other applications for data analysis, interactive art, or physical therapy research.

---

## How It Works

The module follows a straightforward processing pipeline to generate the final 3D coordinates:

1.  **Frame Capture:** An image is captured from a video source (like a webcam).
2.  **MediaPipe Processing:** The image is fed into MediaPipe's **Pose** and **Hands** models, which detect and return the 3D world landmarks for each part.
3.  **Coordinate Transformation:**
    - The origin of the coordinate system is moved from the hips (MediaPipe's default) to the center point between the left and right shoulders. This provides a more stable origin for upper-body movements.
    - The hand landmarks, which have their own local coordinate systems, are translated to align with the wrist landmarks from the pose model.
4.  **Data Combination:** The transformed pose and hand landmarks are combined into a single list of 48 points.
5.  **Output:** This final list of coordinates can be retrieved with `.get_coordinates()` or visualized with `.visualize()`.

---

## Installation

It is highly recommended to use a virtual environment to avoid conflicts with other projects.

1.  **Clone the Repository**
    ```bash
    git clone [https://github.com/your-username/UpperLimbs_Project.git](https://github.com/your-username/UpperLimbs_Project.git)
    cd UpperLimbs_Project
    ```

2.  **Create and Activate a Virtual Environment** (Optional, but recommended)
    ```bash
    # For Mac/Linux
    python3 -m venv venv
    source venv/bin/activate

    # For Windows
    python -m venv venv
    .\venv\Scripts\activate
    ```

3.  **Install the Package**
    This command will also install all required dependencies like `opencv`, `mediapipe`, and `matplotlib`.
    ```bash
    pip install .
    ```
    If you intend to modify the source code, install it in "editable" mode:
    ```bash
    pip install -e .
    ```

---

## Usage

### Running the Demo

The included `main.py` script provides a simple demonstration using a webcam.

```bash
python main.py
```
- A preview window will appear showing the webcam feed with 2D landmarks drawn on it.
- Press the **`v`** key to open or close the live 3D visualization window.
- Press the **`q`** key to quit the application.

### Programmatic Use

Integrating the `upperlimbs` module into your own project is simple.

```python
import cv2
import matplotlib.pyplot as plt
import upperlimbs

# 1. Initialize the UpperLimbs class
ul = upperlimbs.UpperLimbs()

# 2. Start video capture (0 for webcam)
cap = cv2.VideoCapture(0)

while cap.isOpened():
    success, image = cap.read()
    if not success:
        break

    # 3. Process the frame
    ul.process_frame(image)

    # 4. Get the coordinate data
    coordinates = ul.get_coordinates()
    if coordinates:
        # 'coordinates' is a list of 48 points. See the "Output Coordinate System" section.
        # Get the left and right wrist coordinates by their correct indices.
        left_wrist_coords = coordinates[4]
        right_wrist_coords = coordinates[5]
        print(f"Right Wrist [X, Y, Z]: {right_wrist_coords}")

    # 5. Optionally, show the live 3D plot
    ul.visualize()
    
    # 6. Optionally, show the 2D preview
    annotated_image = ul.draw_landmarks(image.copy())
    cv2.imshow("My Preview", annotated_image)

    # Exit on 'ESC' key
    if cv2.waitKey(5) & 0xFF == 27:
        break

# 7. Clean up resources
cap.release()
cv2.destroyAllWindows()
ul.close()
```

---

## API Reference

The primary interface is the `UpperLimbs` class.

`ul = upperlimbs.UpperLimbs(min_detection_confidence=0.5, min_tracking_confidence=0.5)`
:   Initializes the processor. You can optionally adjust the MediaPipe model confidence levels.

`coordinates = ul.process_frame(image)`
:   Processes a single image frame (a NumPy array in BGR format) and returns the list of 48 3D coordinates.

`coordinates = ul.get_coordinates()`
:   Returns the list of coordinates from the last successfully processed frame. Returns `None` if no landmarks were found.

`ul.visualize()`
:   Opens or updates a Matplotlib 3D plot window showing the skeleton based on the last processed coordinates.

`annotated_image = ul.draw_landmarks(image)`
:   Draws the 2D pose and hand landmarks detected by MediaPipe onto the provided image and returns the annotated image.

`ul.close()`
:   Releases the MediaPipe model resources. Should be called when you are finished.

---

## Output Coordinate System

The `.get_coordinates()` method returns a single list containing **48 points**. Each point is a sub-list of `[X, Y, Z]` coordinates.

The origin `(0, 0, 0)` is the center point between the shoulders. The units are roughly metric but are scaled based on the person's detected pose.
-   **+X** is to your right
-   **+Y** is up
-   **+Z** is towards you (out of the screen)

The 48 points are ordered as follows:

| Index Range | Part                  | Number of Points | Details                                                                                   |
| :---------- | :-------------------- | :--------------- | :---------------------------------------------------------------------------------------- |
| `0 - 5`     | **Pose (Torso/Arms)** | 6                | The main joints of the upper body. See detailed breakdown below.                           |
| `6 - 26`    | **Left Hand** | 21               | All landmarks for the left hand. Connects to the Left Wrist (Index 4).                    |
| `27 - 47`   | **Right Hand** | 21               | All landmarks for the right hand. Connects to the Right Wrist (Index 5).                  |

#### Detailed Breakdown of Pose Landmarks (Indices 0-5):

-   `Index 0`: Left Shoulder
-   `Index 1`: Right Shoulder
-   `Index 2`: Left Elbow
-   `Index 3`: Right Elbow
-   `Index 4`: Left Wrist
-   `Index 5`: Right Wrist

#### Detailed Breakdown of Hand Landmarks (Indices 6-26 and 27-47):

The 21 landmarks for each hand follow the standard MediaPipe Hand Landmark Model. For a visual diagram of these points, please refer to the official [MediaPipe Hands documentation](https://developers.google.com/mediapipe/solutions/vision/hand_landmarker#hand-landmarks).

---

## Citation

If you use this software in your research or a publication, we would appreciate it if you would cite the following paper:

**S. Shrestha, H. Takami, Y. Honda and M. Irie, "Research on Measurement System of Upper Limb by Using Single Monocular Web Camera and Inference AI," *2024 17th International Convention on Rehabilitation Engineering and Assistive Technology (i-CREATe)*, 2024, pp. 1-4, doi: 10.1109/i-CREATe62067.2024.10776555.**

For your convenience, you can use the following BibTeX entry:

```bibtex
@INPROCEEDINGS{10776555,
  author={Shrestha, Suman and Takami, Hibiki and Honda, Yuichiro and Irie, Mitsuru},
  booktitle={2024 17th International Convention on Rehabilitation Engineering and Assistive Technology (i-CREATe)}, 
  title={Research on Measurement System of Upper Limb by Using Single Monocular Web Camera and Inference AI}, 
  year={2024},
  volume={},
  number={},
  pages={1-4},
  keywords={Training;Visualization;Accuracy;Tracking;Low-pass filters;Cameras;Motion capture;Real-time systems;Artificial intelligence;Time-domain analysis},
  doi={10.1109/i-CREATe62067.2024.10776555}
}
```

---

## Dependencies
This project's dependencies will be installed automatically when you run `pip install .`.
- `opencv-python`
- `mediapipe`
- `numpy`
- `matplotlib`