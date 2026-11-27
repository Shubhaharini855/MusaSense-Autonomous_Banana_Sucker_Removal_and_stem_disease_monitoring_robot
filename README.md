# MusaSense – Autonomous Banana Sucker Removal and Pseudostem Weevil Monitoring Robot

## 📌 Project Overview

MusaSense is an AI-powered agricultural robotics project designed to assist banana farmers in identifying unwanted banana suckers while monitoring pseudostem weevil-related features.

The system uses custom-trained YOLO11 deep learning models for plant identification and pest-related object detection. It combines computer vision with a four-wheel robotic chassis and a robotic arm equipped with a cutter mechanism to support targeted sucker removal.

## 🎯 Objectives

- Identify banana mother plants and unwanted suckers using deep learning.
- Detect pseudostem weevil-related visual features for plant monitoring.
- Develop a robotic platform to support targeted sucker removal.
- Reduce manual effort and improve precision in banana farm operations.

## 🧠 Deep Learning Models

### 1. Mother Plant and Sucker Detection – YOLO11n

- Dataset: 312 self-collected banana plant images.
- Annotation: Manually annotated using Roboflow.
- Classes: `mother_plant`, `sucker_plant`.
- Model: Ultralytics YOLO11n (Nano).
- Training: Local CPU-based training.
- Evaluation: 80.8% mAP@50 on the validation dataset.

### 2. Pseudostem Weevil Detection – YOLO11m

- Dataset: Approximately 2,736 images.
- Annotation: Manually annotated using Roboflow.
- Class: `Pseudostem-weevil`.
- Model: Ultralytics YOLO11m (Medium).
- Training: Google Colab, 100 epochs.
- Evaluation: 37.29% mAP@50 on the test dataset.

## ⚙️ Hardware Components

| Component | Purpose |
|---|---|
| ESP32 | Mobile chassis control |
| Arduino Uno | Robotic arm control |
| NEMA17 Stepper Motors (3) | Robotic arm movement |
| DRV8825 Drivers | Stepper motor control |
| CNC Shield V3 | Motor driver interface |
| Tower Pro Micro Servo | Cutter mechanism operation |
| L298N Motor Driver (1) | DC motor control |
| 37GM385 DC Gear Motors (4) | Robot movement |
| 18650 Batteries (3) | Mobile power supply |
| LM2596 Buck Converter | Voltage regulation |
| 12V 5A SMPS | Robotic arm power supply |
| USB Webcam | Planned live image acquisition |

## 💻 Software and Technologies

- Python
- YOLO11n and YOLO11m
- PyTorch
- Ultralytics
- Roboflow
- OpenCV
- Google Colab
- Visual Studio Code
- Arduino IDE
- ESP32 and Arduino programming

## 🔄 System Architecture

The proposed system workflow is:

1. Image acquisition from a camera.
2. YOLO11n identifies the banana mother plant and sucker.
3. YOLO11m detects pseudostem weevil-related features when selected.
4. Detection results support target identification and monitoring.
5. The robotic platform and arm are intended to perform targeted sucker removal.

## 📊 Model Performance

| Evaluation Metric | YOLO11n | YOLO11m |
|---|---:|---:|
| Precision | 80.0% | 54.05% |
| Recall | 74.4% | 51.45% |
| mAP@50 | 80.8% | 37.29% |
| mAP@50–95 | 43.7% | 22.66% |
| Evaluation Dataset | Validation | Test |

*Note: The models were evaluated on different dataset splits. Their scores should not be considered a direct comparison.*

## 🚧 Current Development Status

**Completed:**
- Custom banana mother plant and sucker image collection.
- Dataset annotation and preparation using Roboflow.
- YOLO11n and YOLO11m model training and evaluation.
- Initial image-based model inference.
- Robotic arm movement programming.
- Preliminary mobile chassis development.

**Future Enhancements:**
- Live USB webcam integration.
- ROS 2-based coordination.
- AI-to-robot controller integration.
- Camera calibration and target localization.
- Autonomous navigation and targeted sucker removal.
- Field testing and performance improvements.

## 🌱 Expected Impact

MusaSense aims to support smart banana farming through deep learning-based plant identification, pest-related visual monitoring, and robotic assistance. The project explores how AI and robotics can reduce manual agricultural effort and support more efficient farm management.

## 👩‍💻 Project Focus

**Domain:** Deep Learning | Computer Vision | Agricultural Robotics | Object Detection

**Project Name:** MusaSense

**Model Architecture:** YOLO11n and YOLO11m

*Developed as an academic agricultural robotics project.*
