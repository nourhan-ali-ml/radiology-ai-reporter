from ultralytics import YOLO
import cv2
import numpy as np
from typing import List, Dict

class SimpleDetector:
    """Simple detector for testing - uses pretrained YOLO"""
    
    def __init__(self):
        print("Loading YOLOv8 model...")
        self.model = YOLO('yolov8n.pt')  # Nano model for testing
        print("✅ Model loaded!")
    
    def detect(self, image_path: str, conf_threshold: float = 0.3) -> List[Dict]:
        """Detect objects in image"""
        results = self.model.predict(
            image_path,
            conf=conf_threshold,
            verbose=False
        )
        
        detections = []
        for result in results:
            boxes = result.boxes
            for box in boxes:
                detection = {
                    'finding': 'abnormality',
                    'confidence': float(box.conf[0]),
                    'bbox': {
                        'x1': float(box.xyxy[0][0]),
                        'y1': float(box.xyxy[0][1]),
                        'x2': float(box.xyxy[0][2]),
                        'y2': float(box.xyxy[0][3])
                    },
                    'urgency': self.determine_urgency(float(box.conf[0]))
                }
                detections.append(detection)
        
        return detections
    
    def determine_urgency(self, confidence: float) -> str:
        """Determine urgency level"""
        if confidence > 0.7:
            return "high"
        elif confidence > 0.4:
            return "moderate"
        else:
            return "low"
    
    def visualize_detections(self, image_path: str, detections: List[Dict], output_path: str):
        """Visualize detections on image"""
        img = cv2.imread(image_path)
        
        for det in detections:
            bbox = det['bbox']
            confidence = det['confidence']
            
            color = {
                'high': (0, 0, 255),
                'moderate': (0, 165, 255),
                'low': (0, 255, 0)
            }[det['urgency']]
            
            cv2.rectangle(
                img,
                (int(bbox['x1']), int(bbox['y1'])),
                (int(bbox['x2']), int(bbox['y2'])),
                color,
                2
            )
            
            label = f"{det['finding']} {confidence:.2f}"
            cv2.putText(
                img,
                label,
                (int(bbox['x1']), int(bbox['y1']) - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                color,
                2
            )
        
        cv2.imwrite(output_path, img)
        print(f"✅ Visualization saved to {output_path}")

if __name__ == "__main__":
    detector = SimpleDetector()
    print("✅ Detector ready!")