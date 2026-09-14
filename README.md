<<<<<<< HEAD
# RoadScan AI – Automated Aerial Road Monitoring System

> **College Project Prototype / Technical Demonstration**  
> An autonomous aerial computer vision web application designed to monitor highway construction progress, evaluate pavement quality, detect surface distress (potholes, cracks, incomplete sections), and generate official compliance audit reports from drone orthomosaic imagery.

---

## 1. Quick Start Guide: How to Run the Application

The application is built on **Python 3.13 + Flask** paired with modern client-side libraries loaded via CDN (Tailwind CSS, Lucide Icons, Chart.js, Leaflet.js, and html2pdf.js). There is **no Node.js / npm build step required**.

### Prerequisites
- Python 3.10+ (Python 3.13 is already installed on your system)
- Flask (`pip install Flask` – already installed)

### Launch Command
Open PowerShell or Command Prompt in the project folder:
```powershell
cd C:\Users\basav\.gemini\antigravity\scratch\roadscan-ai
python app.py
```

### Accessing the Web Application
Open your web browser and navigate to:
```
http://127.0.0.1:5000
```

---

## 2. Project Architecture & File Organization

```
roadscan-ai/
├── app.py                      # Core Flask backend server & REST API controller
├── README.md                   # Complete documentation & architecture guide
├── data/
│   └── store.json              # Persistent project, inspection & report database
├── services/
│   ├── __init__.py
│   ├── ai_engine.py            # AI Engine architecture & simulated/future CV detectors
│   └── project_manager.py      # Project, survey telemetry & report management service
├── static/
│   ├── css/
│   │   └── style.css           # Custom dark HUD theme, bounding-box overlays & print styling
│   ├── images/
│   │   ├── logo.svg            # RoadScan AI vector emblem
│   │   ├── drone_road_aerial_1.svg  # High-res aerial survey for NH-169 (Pothole & Paving)
│   │   ├── drone_road_aerial_2.svg  # Curved corridor survey (Cracking & Distress)
│   │   └── drone_road_aerial_3.svg  # Sub-base grading & roller survey
│   ├── js/
│   │   ├── app.js              # Application logic, AI simulation runner, canvas bounding-box logic
│   │   ├── charts.js           # Chart.js progress velocity & defect distribution charts
│   │   └── map.js              # Leaflet.js GIS highway corridor & waypoint mapping
│   └── uploads/                # Directory for user-uploaded aerial JPG/PNG/MP4 files
└── templates/
    ├── base.html               # Main responsive layout, navigation sidebar & telemetry HUD
    ├── index.html              # Executive Dashboard (KPIs, Charts, GIS map, Recent surveys)
    ├── projects.html           # Project Directory (Corridor cards & Add New Project modal)
    ├── upload.html             # Upload Drone Data & Staged AI inference terminal simulation
    ├── inspection_detail.html  # Interactive AI Inspection Studio (Bounding box canvas & Filters)
    └── reports.html            # Quality Audit Reports Archive & Printable PDF generator
```

---

## 3. Frontend vs. Backend Architecture

### Backend (`app.py`, `services/`)
- **Web Controller (`app.py`)**: Defines route handlers for all pages (`/`, `/projects`, `/upload`, `/inspections/<id>`, `/reports`) and REST APIs (`/api/stats`, `/api/projects`, `/api/analyze`, `/api/reports/generate`).
- **Data Persistence (`services/project_manager.py`)**: Stores projects (e.g. NH-169 Karnataka, 12 km), inspections, and reports with automatic state persistence in `data/store.json`.
- **Media Upload Manager**: Validates and stores incoming UAV orthomosaics and MP4 survey videos up to 64MB.

### Frontend (`templates/`, `static/`)
- **Responsive Layout (`templates/base.html`)**: Features an enterprise-grade dark telemetry interface with active corridor switching and quick navigation.
- **Interactive Inspection Canvas (`static/js/app.js`, `templates/inspection_detail.html`)**: Renders dynamic bounding boxes over the aerial image with color-coded severity badges (**HIGH** in Red, **MEDIUM** in Amber, **LOW** in Cyan). Hovering over any defect pulses the corresponding region on the aerial canvas.
- **GIS Corridor Mapping (`static/js/map.js`)**: Visualizes the highway alignment in Karnataka, India with paved vs. unpaved segments, UAV station markers, and defect hotspots using Leaflet.js.
- **Audit Report Generator (`templates/reports.html`, `static/js/app.js`)**: Generates and downloads official compliance PDF reports with project metadata, aerial imagery, defect tables, and engineering recommendations using `html2pdf.js`.

---

## 4. Where the Mock / Simulated AI Analysis is Implemented

The simulated analysis engine is located in:
👉 [`services/ai_engine.py`](file:///C:/Users/basav/.gemini/antigravity/scratch/roadscan-ai/services/ai_engine.py) in the **`SimulatedRoadAnalyzer`** class.

### Key Capabilities of the Simulator:
1. **Pavement Progress Estimation**: Computes actual paved kilometers vs. planned corridor length based on simulated chainage markers (e.g. 72% / 8.64 km for NH-169).
2. **Defect Bounding-Box Generation**: Outputs normalized coordinates (`x`, `y`, `width`, `height` in %) compatible with standard YOLO and COCO annotation formats.
3. **Defect Severity & Metrics**: Quantifies distress types (Potholes, Longitudinal Cracks, Raveling, Incomplete SMA course), confidence ratings (82%–96%), depth in cm, and surface area in $m^2$.
4. **Engineering Directives**: Generates remediation actions aligned with Indian Roads Congress (IRC) highway maintenance standards.

---

## 5. How a Real Computer Vision Model Could Later Be Connected

The application was designed from the ground up using the **Strategy Pattern** with an abstract base class `BaseRoadAnalyzer`.

### Future Intended Pipeline
$$\text{Drone Footage (JPG/MP4)} \longrightarrow \text{Orthorectification} \longrightarrow \text{YOLOv8 / SegNet} \longrightarrow \text{Distress & Progress} \longrightarrow \text{Database} \longrightarrow \text{Dashboard}$$

### Step-by-Step Production Integration:
1. **Install Computer Vision Libraries**:
   ```bash
   pip install ultralytics opencv-python torch torchvision
   ```

2. **Activate the Placeholder Class**:
   In [`services/ai_engine.py`](file:///C:/Users/basav/.gemini/antigravity/scratch/roadscan-ai/services/ai_engine.py), implement the `YOLOv8RoadAnalyzer` class:
   ```python
   from ultralytics import YOLO
   import cv2

   class YOLOv8RoadAnalyzer(BaseRoadAnalyzer):
       def __init__(self, model_weights_path="models/roadscan_yolov8x.pt"):
           self.model = YOLO(model_weights_path)

       def analyze_media(self, media_path, media_type, project_metadata):
           # 1. Read aerial image
           image = cv2.imread(media_path)
           
           # 2. Run inference
           results = self.model.predict(source=image, conf=0.45)
           
           # 3. Extract bounding boxes, labels, and mask areas
           detected_issues = []
           for box in results[0].boxes:
               # Map detected classes (0: Pothole, 1: Crack, etc.)
               ...
           
           # 4. Calculate progress ratio from asphalt segmentation mask
           progress_pct = calculate_paved_ratio(results[0].masks)
           
           return {
               "progress_pct": progress_pct,
               "detected_issues": detected_issues,
               ...
           }
   ```

3. **Switch Engine Mode**:
   In `app.py`, change:
   ```python
   analyzer = get_analyzer(mode="production_cv")
   ```
   The entire frontend, dashboard, interactive bounding box canvas, and PDF generator will immediately use the real model outputs with **zero UI code changes required**.
=======
# Road-Scan-AI 
>>>>>>> 589c418a4a3bacdef89ad7ec118a21da5e3c7387
