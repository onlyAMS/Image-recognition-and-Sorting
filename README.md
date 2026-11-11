# Color-Based Object Recognition and Robotic Sorting

An implementation of the research paper **"Development of a Color-Based Image Recognition System for Robotic Sorting and Picking" (2024)**.

This project explores the integration of computer vision, microcontrollers, and robotic automation to develop an automated object-sorting system based on colour recognition.

## 1. Research Paper

**Title:** Development of a Color-Based Image Recognition System for Robotic Sorting and Picking

**Authors:**
- Sitti Wetenriajeng Sidehabi
- Muhammad Fadli Azis
- Muhammad Asbar

**Publication:** INTEK Jurnal Penelitian, Vol. 11, No. 2, October 2024.

**DOI:** https://doi.org/10.31963/intek.v11i2.5009

## 2. Project Overview

Note: This implementation does not make use of a robotic arm as stated in the original paper
The project implements an automated sorting system capable of identifying objects based on their colour and directing a robotic arm to place them in designated locations.

The system uses computer vision to identify object colours and communicates the classification results to an Arduino microcontroller, which coordinates the conveyor and robotic arm.

The primary objective is to reduce manual intervention in sorting processes while improving efficiency and consistency.

## 3. Technologies Used

| Technology           | Purpose |
|----------------------|---|
| Python               | Main application programming language |
| OpenCV               | Image processing and colour detection |
| HSV Colour Space     | Colour segmentation and classification |
| Arduino UNO          | Hardware control |
| Serial Communication | Python-Arduino communication |

## 4. System Architecture

The system consists of three main stages:

### A. Object Detection and Colour Recognition

A camera captures images of objects moving along the conveyor belt.

OpenCV processes the captured images using HSV colour segmentation to identify the object's colour.

The paper considers several colour ranges, including red, green, blue, brown, yellow, orange, cyan and black.

### B. Hardware Control


A Webcam detects the object.

When an object is detected:
1. The camera captures for colour identification.
2. The appropriate path for the colour is opened.


### C. Robotic Sorting

Gates open to allow colours to fall into their respective bins

| Colour | Sorting Bin |
|---|---|
| Red | Bin 1 |
| Yellow | Bin 2 |
| Blue | Bin 3 |

## 5. Colour Detection

The implementation uses the HSV (Hue, Saturation, Value) colour model.

HSV makes colour segmentation more intuitive by separating colour information (Hue) from saturation and brightness.

The original research specifies the following HSV ranges:

| Colour | Lower HSV | Upper HSV |
|---|---|---|
| Red | (136, 87, 111) | (180, 255, 255) |
| Green | (25, 52, 72) | (102, 255, 255) |
| Blue | (94, 80, 2) | (120, 255, 255) |
| Yellow | (25, 70, 120) | (30, 255, 255) |

*Note: These are the ranges from the paper's general HSV reference table. The experimental colour-identification section specifies separate ranges for red, yellow and blue.*

## 6. Installation

Clone the repository:

```bash
git clone <repository-url>
cd <repository-name>
```

Install the required dependencies:

```bash
pip install opencv-python numpy pyserial
```

Additional dependencies may be required depending on the implementation.

## 7. Running the Project

1. Connect the camera to the computer.
2. Connect the Arduino UNO.
3. Upload the Arduino control program.
4. Run the Python application.
5. Allow the application to access the camera.
6. Start the conveyor and introduce an object.
7. Observe the colour classification and sorting process.

## 8. Experimental Results

The original research evaluated the system through several tests:

- Colour identification testing.
- Gate logic control
- Overall system integration testing.

The robotic arm achieved 100% coordinate accuracy across five tested positions.

The complete sorting system successfully sorted three different coloured cubes across ten trials, achieving 100% sorting accuracy.

## 9. Implementation and Reproduction

This repository contains an implementation of the methodology proposed in the referenced research paper.

Differences between the original research and this implementation will be documented here, including:

- Hardware configuration differences.
- Modifications to the image-processing algorithm.
- Changes to HSV thresholds.
- Communication protocol modifications.
- Experimental results.

## 10. References

Sidehabi, S. W., Azis, M. F., & Asbar, M. (2024). Development of a Color-Based Image Recognition System for Robotic Sorting and Picking. *INTEK Jurnal Penelitian*, 11(2), 77–82.

https://doi.org/10.31963/intek.v11i2.5009