# Deepfake Detector

Deepfake Detector is a Python library designed for detecting deepfake content in images and videos. Leveraging advanced machine learning techniques, it provides an easy-to-use interface for real-time and batch processing of media files.

## Features

- Real-time Deepfake Detection: Analyze live video feeds to detect deepfake content.
- Batch Processing: Process multiple images and videos to classify them as real or fake.
- Customizable Thresholds: Adjust detection sensitivity to suit your specific needs.

## Installation

You can install the `deepfake_detector` package using pip:

```bash
pip install deepfake_detector
```

## Usage

### For Video Detection

Detect deepfake content in a video file. You can provide a video file path or use a webcam.

```python
from deepfake_detector import live_video_prediction, image_prediction

# Set a custom threshold
live_video_prediction(source='name.mp4',threshold=0.5)
```

### For Image Detection

Detect deepfake content in a single image.

```python
from deepfake_detector import live_video_prediction, image_prediction

# Image prediction example
image_prediction('name.png', threshold=0.6)
```

### Customizing Detection Threshold

You can set the threshold to control the sensitivity of the detection.

```python
# Example with a higher sensitivity threshold
live_video_prediction(source='name.mp4',threshold=0.5)
image_prediction('name.png', threshold=0.6)
```

## Paper Reference

For more detailed information about the techniques used in this library, please refer to the following research paper:

- **Title**: [Deepfake Detection Using the Rate of Change between Frames Based on Computer Vision](https://www.mdpi.com/1424-8220/21/21/7367)
- **Journal**: MDPI Sensors
- **Abstract**: This paper explores advanced methods for detecting deepfake media using convolutional neural networks (CNNs). The study provides a comprehensive analysis of various techniques and their effectiveness in identifying manipulated content.

## Contributing

If you would like to contribute to the development of this library, please contact me.

## Contact

For any questions or feedback, please contact:

- **Author**: Adupa Nithin Sai
- **Email**: [adupanithinsai@gmail.com](mailto:adupanithinsai@gmail.com)
- **GitHub**: [https://github.com/saiadupa/Deepfake-detector](https://github.com/saiadupa/Deepfake-detector)

---

Thank you for using Deepfake Detector. We hope you find it useful for your deepfake detection needs!
```
