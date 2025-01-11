# detect.py
from ultralytics import YOLO
import cv2
import os

# Load pretrained YOLOv8 model
model = YOLO('yolov8n.pt')

def detect_objects(image_path):
    """
    Phát hiện đối tượng trong hình ảnh và vẽ các khung bao quanh đối tượng.

    Args:
        image_path (str): Đường dẫn đến hình ảnh cần phát hiện đối tượng.

    Returns:
        tuple: Một tuple chứa:
            - detections (list): Danh sách các đối tượng được phát hiện, mỗi đối tượng là một dictionary với các khóa:
                - 'label' (str): Nhãn của đối tượng.
                - 'confidence' (float): Độ tin cậy của phát hiện.
            - output_path (str): Đường dẫn đến hình ảnh đã được vẽ khung bao quanh đối tượng.
    """
    # Perform object detection
    results = model(image_path)
    output_path = image_path.replace('uploads', 'static/results')
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    # Draw bounding boxes on the image
    detections = []
    for result in results:
        img = result.orig_img
        for box in result.boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            label = result.names[int(box.cls)]
            confidence = float(box.conf[0])
            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(img, f'{label} {confidence:.2f}', (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
            detections.append({'label': label, 'confidence': confidence})
        # Save the image with bounding boxes
        cv2.imwrite(output_path, img)
    return detections, output_path