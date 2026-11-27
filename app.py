
import tkinter as tk
from tkinter import ttk, messagebox
import cv2
from PIL import Image, ImageTk
from ultralytics import YOLO


# ---------------------------------------
# CONFIGURATION
# ---------------------------------------

CAMERA_INDEX = 1

MODEL_N_PATH = "models/yolov11n/best.pt"
MODEL_M_PATH = "models/yolov11m/best.pt"

MOTHER_CONFIDENCE = 0.25
WEEVIL_CONFIDENCE = 0.30

# CPU inference
DEVICE = "cpu"


# ---------------------------------------
# LOAD YOLO MODELS
# ---------------------------------------

print("Loading MusaSense models...")

try:
    model_n = YOLO(MODEL_N_PATH)
    print("YOLO11n loaded successfully.")

    model_m = YOLO(MODEL_M_PATH)
    print("YOLO11m loaded successfully.")

except Exception as e:
    print("Model loading error:", e)
    raise


# ---------------------------------------
# MAIN APPLICATION
# ---------------------------------------

class MusaSenseApp:

    def __init__(self, root):

        self.root = root
        self.root.title(
            "MusaSense - Banana Plant Monitoring System"
        )
        self.root.geometry("1100x750")
        self.root.configure(bg="#f2f5f2")

        self.running = True
        self.current_mode = "mother"
        self.camera = None
        self.camera_index = CAMERA_INDEX

        self.weevil_threshold = WEEVIL_CONFIDENCE
        self.last_frame = None

        self.create_interface()
        self.open_camera()

        if self.camera is not None:
            self.update_camera()

        self.root.protocol("WM_DELETE_WINDOW", self.close_app)

    # -----------------------------------
    # INTERFACE
    # -----------------------------------

    def create_interface(self):

        title = tk.Label(
            self.root,
            text="MUSASENSE",
            font=("Arial", 24, "bold"),
            bg="#f2f5f2",
            fg="#176b3a"
        )
        title.pack(pady=(15, 3))

        subtitle = tk.Label(
            self.root,
            text="Autonomous Banana Pup Removal "
                 "and Stem Disease Monitoring",
            font=("Arial", 11),
            bg="#f2f5f2",
            fg="#444444"
        )
        subtitle.pack(pady=(0, 15))

        # Tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(
            fill="x",
            padx=25,
            pady=5
        )

        self.mother_tab = tk.Frame(
            self.notebook,
            bg="#ffffff"
        )

        self.weevil_tab = tk.Frame(
            self.notebook,
            bg="#ffffff"
        )

        self.notebook.add(
            self.mother_tab,
            text="Mother Plant & Sucker Identification"
        )

        self.notebook.add(
            self.weevil_tab,
            text="Pseudostem-Weevil Detection"
        )

        self.notebook.bind(
            "<<NotebookTabChanged>>",
            self.change_mode
        )

        # Camera display
        self.video_label = tk.Label(
            self.root,
            bg="#202020",
            text="Waiting for camera...",
            fg="white",
            font=("Arial", 14)
        )

        self.video_label.pack(
            padx=25,
            pady=15,
            fill="both",
            expand=True
        )

        # Status
        self.status_label = tk.Label(
            self.root,
            text="Camera initializing...",
            font=("Arial", 13, "bold"),
            bg="#f2f5f2",
            fg="#176b3a"
        )

        self.status_label.pack(pady=8)

        # Mother tab information
        tk.Label(
            self.mother_tab,
            text="YOLO11n - Mother Plant and Sucker Detection",
            font=("Arial", 11, "bold"),
            bg="white",
            fg="#176b3a"
        ).pack(pady=10)

        tk.Label(
            self.mother_tab,
            text="Green box: Mother Plant    |    "
                 "Red box: Sucker Plant",
            font=("Arial", 10),
            bg="white"
        ).pack(pady=5)

        # Weevil tab information
        tk.Label(
            self.weevil_tab,
            text="YOLO11m - Pseudostem-Weevil Detection",
            font=("Arial", 11, "bold"),
            bg="white",
            fg="#176b3a"
        ).pack(pady=8)

        tk.Label(
            self.weevil_tab,
            text="Adjust the confidence threshold:",
            font=("Arial", 10),
            bg="white"
        ).pack()

        self.threshold_value = tk.DoubleVar(
            value=WEEVIL_CONFIDENCE
        )

        self.threshold_slider = tk.Scale(
            self.weevil_tab,
            from_=0.10,
            to=0.90,
            resolution=0.05,
            orient="horizontal",
            variable=self.threshold_value,
            length=350,
            bg="white",
            highlightthickness=0,
            command=self.update_threshold
        )

        self.threshold_slider.pack(pady=5)

        self.threshold_label = tk.Label(
            self.weevil_tab,
            text="Confidence Threshold: 0.30",
            font=("Arial", 10, "bold"),
            bg="white",
            fg="#176b3a"
        )

        self.threshold_label.pack(pady=(0, 10))

        # Footer
        self.camera_label = tk.Label(
            self.root,
            text="Selected Camera: External USB Webcam (Index 1)",
            font=("Arial", 9),
            bg="#f2f5f2",
            fg="#555555"
        )

        self.camera_label.pack(pady=(0, 10))

    # -----------------------------------
    # OPEN USB CAMERA
    # -----------------------------------

    def open_camera(self):

        self.camera = cv2.VideoCapture(
            self.camera_index,
            cv2.CAP_DSHOW
        )

        if not self.camera.isOpened():

            self.camera.release()

            messagebox.showerror(
                "Camera Error",
                "Unable to open the USB webcam.\n\n"
                "Check the USB connection and close other "
                "applications using the camera."
            )

            self.camera = None
            return

        self.camera.set(
            cv2.CAP_PROP_FRAME_WIDTH, 640
        )

        self.camera.set(
            cv2.CAP_PROP_FRAME_HEIGHT, 480
        )

        print("External USB webcam connected.")

    # -----------------------------------
    # CHANGE DETECTION MODE
    # -----------------------------------

    def change_mode(self, event=None):

        selected_tab = self.notebook.index(
            self.notebook.select()
        )

        if selected_tab == 0:

            self.current_mode = "mother"

            self.status_label.config(
                text="Mother Plant & Sucker Identification Mode",
                fg="#176b3a"
            )

        else:

            self.current_mode = "weevil"

            self.status_label.config(
                text="Pseudostem-Weevil Detection Mode",
                fg="#176b3a"
            )

        print("Selected mode:", self.current_mode)

    # -----------------------------------
    # UPDATE CONFIDENCE THRESHOLD
    # -----------------------------------

    def update_threshold(self, value):

        self.weevil_threshold = float(value)

        self.threshold_label.config(
            text=f"Confidence Threshold: "
                 f"{self.weevil_threshold:.2f}"
        )

    # -----------------------------------
    # MOTHER PLANT AND SUCKER DETECTION
    # -----------------------------------

    def detect_mother_and_sucker(self, frame):

        results = model_n.predict(
            source=frame,
            conf=MOTHER_CONFIDENCE,
            imgsz=416,
            device=DEVICE,
            verbose=False
        )

        result = results[0]

        annotated_frame = result.plot()

        detections = []

        if result.boxes is not None:

            for box in result.boxes:

                class_id = int(box.cls[0])
                confidence = float(box.conf[0])

                class_name = str(
                    model_n.names[class_id]
                )

                detections.append(
                    f"{class_name}: {confidence:.2f}"
                )

        if detections:

            status = " | ".join(detections)

            self.status_label.config(
                text=status,
                fg="#176b3a"
            )

        else:

            self.status_label.config(
                text="No Mother Plant or Sucker Detected",
                fg="#555555"
            )

        return annotated_frame

    # -----------------------------------
    # PSEUDOSTEM-WEEVIL DETECTION
    # -----------------------------------

    def detect_weevil(self, frame):

        results = model_m.predict(
            source=frame,
            conf=self.weevil_threshold,
            imgsz=640,
            device=DEVICE,
            verbose=False
        )

        result = results[0]

        annotated_frame = result.plot()

        detected = False
        highest_confidence = 0.0

        if result.boxes is not None:

            for box in result.boxes:

                confidence = float(box.conf[0])

                class_id = int(box.cls[0])

                class_name = str(
                    model_m.names[class_id]
                )

                if "weevil" in class_name.lower():

                    detected = True

                    highest_confidence = max(
                        highest_confidence,
                        confidence
                    )

        if detected:

            self.status_label.config(
                text=(
                    "POTENTIAL PSEUDOSTEM-WEEVIL DETECTED! "
                    f"Confidence: {highest_confidence:.2f}"
                ),
                fg="#c62828"
            )

        else:

            self.status_label.config(
                text="No Weevil Detected Above Threshold",
                fg="#176b3a"
            )

        return annotated_frame

    # -----------------------------------
    # LIVE CAMERA AND MODEL PROCESSING
    # -----------------------------------

    def update_camera(self):

        if not self.running:
            return

        if self.camera is None:
            return

        ret, frame = self.camera.read()

        if not ret:

            self.status_label.config(
                text="Unable to read camera frame",
                fg="#c62828"
            )

            self.root.after(100, self.update_camera)
            return

        # Run only the selected model

        if self.current_mode == "mother":

            output_frame = self.detect_mother_and_sucker(
                frame
            )

        else:

            output_frame = self.detect_weevil(
                frame
            )

        # Convert frame for Tkinter

        output_frame = cv2.cvtColor(
            output_frame,
            cv2.COLOR_BGR2RGB
        )

        image = Image.fromarray(output_frame)

        image.thumbnail((950, 520))

        photo = ImageTk.PhotoImage(image=image)

        self.video_label.configure(
            image=photo,
            text=""
        )

        self.video_label.image = photo

        # Schedule next frame

        self.root.after(
            10,
            self.update_camera
        )

    # -----------------------------------
    # CLOSE APPLICATION
    # -----------------------------------

    def close_app(self):

        self.running = False

        if self.camera is not None:
            self.camera.release()

        self.root.destroy()


# ---------------------------------------
# START APPLICATION
# ---------------------------------------

if __name__ == "__main__":

    root = tk.Tk()

    app = MusaSenseApp(root)

    root.mainloop()
