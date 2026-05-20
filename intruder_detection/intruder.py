import cv2
import numpy as np
import datetime
import os
import winsound
import requests
import pickle
import time
import csv
from ultralytics import YOLO

# ================= CONFIG =================
CONFIDENCE_THRESHOLD = 65
ALERT_COOLDOWN = 15
CONF_HISTORY_SIZE = 15

BOT_TOKEN = "YOUR_BOT_TOKEN"
CHAT_ID = "YOUR_CHAT_ID"

IMAGE_DIR = "intruder_images"
LOG_FILE = "access_log.csv"

# ================= LOAD MODELS =================
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read("trainer.yml")

with open("labels.pkl", "rb") as f:
    label_map = pickle.load(f)

face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)

yolo_model = YOLO("yolov8n.pt")

# ================= SETUP =================
os.makedirs(IMAGE_DIR, exist_ok=True)

if not os.path.exists(LOG_FILE):
    with open(LOG_FILE, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Timestamp", "Name", "Confidence", "Status", "Intruder_Count"])

# ================= FUNCTIONS =================
def send_sos(image_path, timestamp, count):
    message = f"🚨 Intruder Alert 🚨\n{count} Intruder(s) Detected\nTime: {timestamp}"

    try:
        requests.get(
            f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
            params={"chat_id": CHAT_ID, "text": message},
            timeout=5
        )

        with open(image_path, "rb") as photo:
            requests.post(
                f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto",
                data={"chat_id": CHAT_ID},
                files={"photo": photo},
                timeout=5
            )

    except Exception as e:
        print("Telegram Error:", e)


def log_event(name, confidence, status, intruder_count=0):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open(LOG_FILE, 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([timestamp, name, round(confidence, 2), status, intruder_count])


# ================= CAMERA =================
cap = cv2.VideoCapture(0)

for _ in range(10):
    cap.read()

cv2.namedWindow("Smart Intruder Detection System", cv2.WINDOW_NORMAL)

confidence_history = {}
intruder_counter = 0
last_alert_time = 0

# ================= MAIN LOOP =================
while cap.isOpened():

    ret, frame = cap.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # ================= YOLO HUMAN DETECTION =================
    results = yolo_model(frame)[0]
    human_boxes = []

    for box in results.boxes:
        cls = int(box.cls[0])

        if cls == 0:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            human_boxes.append((x1, y1, x2, y2))

    # ================= FACE DETECTION =================
    faces = []

    for (x1, y1, x2, y2) in human_boxes:
        roi_gray = gray[y1:y2, x1:x2]

        detected_faces = face_cascade.detectMultiScale(roi_gray, 1.2, 5)

        for (fx, fy, fw, fh) in detected_faces:
            faces.append((x1 + fx, y1 + fy, fw, fh))

    # ================= HUMAN COUNT =================
    human_count = max(len(human_boxes), len(faces))

    cv2.putText(frame, f"HUMANS: {human_count}", (20, 50),
                cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)

    intruders_in_frame = 0
    max_intruder_conf = 0

    for (x, y, w, h) in faces:

        if w < 80 or h < 80:
            continue

        face = cv2.resize(gray[y:y+h, x:x+w], (200, 200))
        label, confidence = recognizer.predict(face)
        name = label_map.get(label, "Unknown")

        # ================= CONFIDENCE HISTORY =================
        if label not in confidence_history:
            confidence_history[label] = []

        confidence_history[label].append(confidence)

        if len(confidence_history[label]) > CONF_HISTORY_SIZE:
            confidence_history[label].pop(0)

        avg_conf = sum(confidence_history[label]) / len(confidence_history[label])

        if name == "Unknown":
            avg_conf = 999

        # ================= DECISION =================
        if avg_conf < 65:
            status = f"AUTHORIZED - {name} ({int(avg_conf)})"
            color = (0, 255, 0)
            
        elif avg_conf < 70:
            status = f"UNSURE - {name} ({int(avg_conf)})"
            color = (0, 255, 255)

        else:
            status = f"INTRUDER - UNKNOWN ({int(avg_conf)})"
            color = (0, 0, 255)
            intruders_in_frame += 1
            max_intruder_conf = max(max_intruder_conf, avg_conf)

        cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)
        y_text = y - 10 if y - 10 > 30 else y + 25

        cv2.putText(frame, status, (x, y_text),
            cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)

    # ================= ALERT =================
    if intruders_in_frame > 0 and intruder_counter > 10 and time.time() - last_alert_time > ALERT_COOLDOWN:

        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        image_path = os.path.join(IMAGE_DIR, f"intruder_{timestamp}.jpg")

        cv2.imwrite(image_path, frame)
        winsound.Beep(2000, 400)

        send_sos(image_path, timestamp, intruders_in_frame)
        log_event("UNKNOWN", max_intruder_conf, "INTRUDER", intruders_in_frame)

        last_alert_time = time.time()
        intruder_counter = 0

    if intruders_in_frame > 0:
        intruder_counter += 1
    else:
        intruder_counter = 0

    cv2.imshow("Smart Intruder Detection System", frame)

    if cv2.waitKey(1) & 0xFF == ord('s'):
        break

cap.release()
cv2.destroyAllWindows()