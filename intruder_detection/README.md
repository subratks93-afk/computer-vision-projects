# 🔍 AI-Based Smart Intruder Detection & Alert System

---

## 📌 Overview

A real-time AI surveillance system built using Python and OpenCV that detects human faces through a webcam and identifies whether the person is authorized or an intruder using face recognition.

> ⚡ Designed with real-world constraints like false detection handling and alert optimization.

If an intruder is detected, the system:

* Captures the image
  
* Triggers an alert
  
* Sends a Telegram notification
  
* Logs the event

---

## ⭐ Key Highlights

* Real-time face detection and recognition
  
* Intelligent intruder alert system
  
* Telegram integration with image alerts

* Stable predictions using confidence averaging
  
* Cooldown mechanism to prevent alert spam
  
* Designed for real-world surveillance applications

---

## 🚀 Features

* Detects faces in real-time using webcam
  
* Recognizes authorized users using LBPH model
  
* Identifies unknown persons as intruders
  
* Captures and stores intruder images
  
* Sends Telegram alerts with captured image
  
* Triggers beep sound for local alert
  
* Maintains CSV log of all events
  
* Confidence averaging for stable detection
  
* Cooldown system to avoid repeated alerts

---

## 🧠 Technologies Used

* Python
  
* OpenCV (`opencv-contrib-python`)
  
* NumPy
  
* LBPH Face Recognition
  
* Haar Cascade (Face Detection)
  
* Telegram Bot API
  
* CSV (Logging system)

---

## 🧩 System Architecture

```
Webcam Input

      ↓

Face Detection (Haar Cascade)

      ↓

Face Recognition (LBPH)

      ↓

Decision Making


Authorized → No Action
 
Intruder → Alert + Capture + Notify + Log
```

---

## 🔄 How It Works

1. Webcam captures live video
   
2. Faces are detected using Haar Cascade
   
3. Face is compared with trained dataset
   
4. System checks confidence score
   
5. If intruder detected:

   * Beep alert is triggered
     
   * Image is saved
     
   * Telegram alert is sent
     
   * Event is logged in CSV

---

## 📷 Output

### ✅ Authorized User Detection

System correctly identifies an authorized user.

![Authorized](authorized_image.png)

---

### 🚨 Intruder Detection

Unknown person detected and classified as intruder.

![Intruder](intruder.png)

---

### 📊 CSV Log Output

All detection events are recorded with timestamp and status.

![CSV Log](CSV_log.png)

---

### 📩 Telegram Alert Output

The system sends a real-time alert via Telegram with image and timestamp.

![Intruder Alert](intruder_alert.jpeg)

---

## 📂 Data Storage

* Intruder images → `intruder_images/`
  
* Logs → `access_log.csv`

---

## 📁 Project Structure

```
intruder_detection/

│

├── intr.py

├── trainer.yml

├── labels.pkl

├── access_log.csv

│

├── intruder_images/

│

└── dataset/

    └── SUBRAT/
```

---

## 📦 Requirements

* Python 3.10
  
* Webcam
  
* Internet connection (for Telegram alerts)

---

## 🛠️ Installation

```
pip install opencv-contrib-python numpy requests
```

---

## ▶️ Run

```
python intr.py
```

Press **'s'** to stop the system.

---

## ⚠️ Important Note

Update your Telegram credentials before running:

```
bot_token = "YOUR_BOT_TOKEN"

chat_id = "YOUR_CHAT_ID"
```

---

## ⚠️ Challenges Faced

* Reducing false detections
  
* Stabilizing predictions using confidence averaging
  
* Avoiding alert spam using cooldown mechanism

---

## 🔮 Future Improvements

* Multi-user face recognition
  
* Raspberry Pi deployment
  
* GUI dashboard
  
* Deep learning-based upgrade (YOLO / CNN)

---

## 👨‍💻 Author

Subrat

---

## ⭐ About

A real-time AI surveillance system for detecting and alerting intruders using computer vision.
