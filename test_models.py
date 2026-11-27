
from ultralytics import YOLO

print("=" * 50)
print("       MUSASENSE - MODEL VERIFICATION")
print("=" * 50)

# Load YOLO11n
print("\nLoading YOLO11n model...")

model_n = YOLO("models/yolov11n/best.pt")

print("YOLO11n loaded successfully!")
print("YOLO11n Classes:", model_n.names)

# Load YOLO11m
print("\nLoading YOLO11m model...")

model_m = YOLO("models/yolov11m/best.pt")

print("YOLO11m loaded successfully!")
print("YOLO11m Classes:", model_m.names)

print("\n" + "=" * 50)
print("SUCCESS: BOTH MODELS LOADED!")
print("=" * 50)
