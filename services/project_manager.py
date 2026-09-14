"""
RoadScan AI - Automated Aerial Road Monitoring System
Module: services/project_manager.py

Handles project state, inspection histories, persistent storage,
and reporting metadata.
"""

import os
import json
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional


class ProjectManager:
    """Manages road projects, drone survey records, and generated inspection reports."""

    def __init__(self, data_file: str = "data/store.json"):
        self.data_file = data_file
        self.data: Dict[str, Any] = {
            "active_project_id": "proj-nh169",
            "projects": [],
            "inspections": [],
            "reports": []
        }
        self._load_or_seed_data()

    def _load_or_seed_data(self):
        os.makedirs(os.path.dirname(self.data_file), exist_ok=True)
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    self.data = json.load(f)
                return
            except Exception as e:
                print(f"[ProjectManager] Failed to load {self.data_file}, reseeding: {e}")

        self._seed_default_data()
        self.save()

    def _seed_default_data(self):
        """Seed realistic sample data required by the specification."""
        now = datetime.now()
        d1 = (now - timedelta(days=2)).strftime("%Y-%m-%d %H:%M")
        d2 = (now - timedelta(days=9)).strftime("%Y-%m-%d %H:%M")
        d3 = (now - timedelta(days=18)).strftime("%Y-%m-%d %H:%M")
        d4 = (now - timedelta(days=28)).strftime("%Y-%m-%d %H:%M")

        self.data["projects"] = [
            {
                "id": "proj-nh169",
                "name": "NH-169 Road Development",
                "corridor_code": "NH-169-KA-SEC4",
                "location": "Karnataka, India (Shivamogga - Mangaluru Section)",
                "coordinates": {"lat": 13.0827, "lng": 75.0135},
                "total_length_km": 12.0,
                "progress_pct": 72.0,
                "completed_km": 8.64,
                "remaining_km": 3.36,
                "status": "Active Construction",
                "contractor": "Karnataka State Highway Authority & L&T Infra",
                "last_inspection_date": d1,
                "total_inspections": 6,
                "open_issues": 7,
                "overall_condition": "Fair",
                "description": "Widening of 2-lane to 4-lane paved corridor with asphalt concrete wearing course and grade separators."
            },
            {
                "id": "proj-sh48",
                "name": "SH-48 Coastal Highway Corridor",
                "corridor_code": "SH-48-KA-CST",
                "location": "Udupi - Kundapura, Karnataka, India",
                "coordinates": {"lat": 13.3409, "lng": 74.7421},
                "total_length_km": 24.5,
                "progress_pct": 45.0,
                "completed_km": 11.02,
                "remaining_km": 13.48,
                "status": "Active Construction",
                "contractor": "Coastal Infra Developers Ltd.",
                "last_inspection_date": d3,
                "total_inspections": 4,
                "open_issues": 12,
                "overall_condition": "Fair",
                "description": "Marine environment high-durability bituminous highway reinforcement with reinforced shoulder slopes."
            },
            {
                "id": "proj-or4",
                "name": "Bengaluru Outer Ring Expressway Link",
                "corridor_code": "BLR-ORR-PH3",
                "location": "Bengaluru Rural, Karnataka, India",
                "coordinates": {"lat": 13.0358, "lng": 77.5970},
                "total_length_km": 18.0,
                "progress_pct": 89.0,
                "completed_km": 16.02,
                "remaining_km": 1.98,
                "status": "Final Surfacing",
                "contractor": "Karnataka Road Development Corp (KRDCL)",
                "last_inspection_date": d2,
                "total_inspections": 8,
                "open_issues": 3,
                "overall_condition": "Good",
                "description": "6-lane controlled access asphalt corridor connecting industrial zones with smart electronic tolling gantries."
            }
        ]

        # Seed realistic inspections for NH-169
        self.data["inspections"] = [
            {
                "id": "insp-nh169-001",
                "project_id": "proj-nh169",
                "project_name": "NH-169 Road Development",
                "date": d1,
                "media_type": "image",
                "media_url": "/static/images/drone_road_aerial_1.svg",
                "thumbnail_url": "/static/images/drone_road_aerial_1.svg",
                "flight_duration_min": 24,
                "uav_pilot": "Capt. R. Sharma (DGCA Certified)",
                "progress_pct": 72.0,
                "completed_km": 8.64,
                "remaining_km": 3.36,
                "overall_condition": "Fair",
                "health_score": 78,
                "summary_counts": {
                    "total_issues": 7,
                    "potholes": 2,
                    "surface_defects": 3,
                    "incomplete_sections": 2,
                    "high_severity": 2,
                    "medium_severity": 3,
                    "low_severity": 2
                },
                "detected_issues": [
                    {
                        "id": "DEF-001",
                        "type": "pothole",
                        "label": "Pothole Hazard",
                        "severity": "HIGH",
                        "confidence": 0.94,
                        "chainage": "KM 8.420",
                        "bbox": {"x": 34, "y": 42, "width": 14, "height": 12},
                        "area_sq_m": 0.85,
                        "depth_cm": 6.2,
                        "description": "Deep asphalt depression with loose aggregate, poses severe risk to high-speed traffic."
                    },
                    {
                        "id": "DEF-002",
                        "type": "pothole",
                        "label": "Sub-Base Cavity",
                        "severity": "HIGH",
                        "confidence": 0.89,
                        "chainage": "KM 8.510",
                        "bbox": {"x": 68, "y": 55, "width": 12, "height": 10},
                        "area_sq_m": 0.62,
                        "depth_cm": 4.8,
                        "description": "Localized water-ingress cavity causing base course degradation."
                    },
                    {
                        "id": "DEF-003",
                        "type": "surface_defect",
                        "label": "Longitudinal Cracking",
                        "severity": "MEDIUM",
                        "confidence": 0.87,
                        "chainage": "KM 8.350",
                        "bbox": {"x": 20, "y": 25, "width": 26, "height": 15},
                        "area_sq_m": 3.40,
                        "depth_cm": 1.5,
                        "description": "Linear thermal fatigue cracking along outer wheel path."
                    },
                    {
                        "id": "DEF-004",
                        "type": "surface_defect",
                        "label": "Surface Raveling & Weathering",
                        "severity": "LOW",
                        "confidence": 0.82,
                        "chainage": "KM 8.210",
                        "bbox": {"x": 52, "y": 28, "width": 20, "height": 18},
                        "area_sq_m": 5.10,
                        "depth_cm": 0.5,
                        "description": "Loss of binder matrix resulting in dislodged coarse stone aggregate."
                    },
                    {
                        "id": "DEF-005",
                        "type": "surface_defect",
                        "label": "Edge Break Distress",
                        "severity": "MEDIUM",
                        "confidence": 0.85,
                        "chainage": "KM 8.610",
                        "bbox": {"x": 78, "y": 36, "width": 16, "height": 14},
                        "area_sq_m": 2.15,
                        "depth_cm": 2.2,
                        "description": "Irregular edge breaking along unpaved earthen shoulder."
                    },
                    {
                        "id": "DEF-006",
                        "type": "incomplete_section",
                        "label": "Missing Bituminous Wearing Course",
                        "severity": "MEDIUM",
                        "confidence": 0.96,
                        "chainage": "KM 8.680 - 8.850",
                        "bbox": {"x": 45, "y": 68, "width": 35, "height": 22},
                        "area_sq_m": 120.0,
                        "depth_cm": 0.0,
                        "description": "Prime coat and tack coat exposed; final 40mm Stone Matrix Asphalt (SMA) pending."
                    },
                    {
                        "id": "DEF-007",
                        "type": "incomplete_section",
                        "label": "Uncompacted Shoulder Layer",
                        "severity": "LOW",
                        "confidence": 0.91,
                        "chainage": "KM 8.100 - 8.250",
                        "bbox": {"x": 10, "y": 60, "width": 25, "height": 16},
                        "area_sq_m": 45.0,
                        "depth_cm": 0.0,
                        "description": "Graded granular sub-base requires final roller vibratory compaction pass."
                    }
                ],
                "telemetry": {
                    "uav_platform": "DJI Matrice 300 RTK - Zenmuse P1 45MP",
                    "flight_altitude_m": 48.5,
                    "ground_sampling_distance_cm_px": 1.15,
                    "flight_speed_m_s": 4.2,
                    "coordinates": {"latitude": 13.0827, "longitude": 75.0135},
                    "sensor_shutter": "1/1000s, ISO 100, f/4.0",
                    "survey_grid": "Double-Grid Cross Hatch (75% Forward, 70% Side Overlap)"
                },
                "recommendations": [
                    "Execute cold-mix or mastic asphalt patching immediately on KM 8.420 and KM 8.510 potholes to prevent moisture seepage into WMM sub-base.",
                    "Apply elastomeric crack sealant on longitudinal cracks (KM 8.350) prior to monsoon precipitation.",
                    "Schedule Bituminous Concrete (BC) paver convoy for unpaved corridor stretch KM 8.680 - 8.850.",
                    "Mobilize pneumatic tire roller for shoulder stabilization on KM 8.100."
                ]
            },
            {
                "id": "insp-nh169-002",
                "project_id": "proj-nh169",
                "project_name": "NH-169 Road Development",
                "date": d2,
                "media_type": "image",
                "media_url": "/static/images/drone_road_aerial_2.svg",
                "thumbnail_url": "/static/images/drone_road_aerial_2.svg",
                "flight_duration_min": 28,
                "uav_pilot": "Capt. R. Sharma (DGCA Certified)",
                "progress_pct": 68.5,
                "completed_km": 8.22,
                "remaining_km": 3.78,
                "overall_condition": "Fair",
                "health_score": 74,
                "summary_counts": {
                    "total_issues": 9,
                    "potholes": 4,
                    "surface_defects": 3,
                    "incomplete_sections": 2,
                    "high_severity": 3,
                    "medium_severity": 4,
                    "low_severity": 2
                },
                "detected_issues": [
                    {
                        "id": "DEF-101",
                        "type": "pothole",
                        "label": "Transverse Pothole Cluster",
                        "severity": "HIGH",
                        "confidence": 0.92,
                        "chainage": "KM 7.820",
                        "bbox": {"x": 42, "y": 38, "width": 16, "height": 14},
                        "area_sq_m": 1.2,
                        "depth_cm": 7.0,
                        "description": "Significant pavement dislodgement following heavy rain runoff."
                    },
                    {
                        "id": "DEF-102",
                        "type": "surface_defect",
                        "label": "Alligator Cracking Pattern",
                        "severity": "HIGH",
                        "confidence": 0.88,
                        "chainage": "KM 7.950",
                        "bbox": {"x": 62, "y": 48, "width": 22, "height": 18},
                        "area_sq_m": 4.8,
                        "depth_cm": 2.1,
                        "description": "Interconnected load fatigue distress indicating structural base deflection."
                    }
                ],
                "telemetry": {
                    "uav_platform": "DJI Phantom 4 RTK",
                    "flight_altitude_m": 50.0,
                    "ground_sampling_distance_cm_px": 1.35,
                    "flight_speed_m_s": 5.0,
                    "coordinates": {"latitude": 13.0810, "longitude": 75.0110}
                },
                "recommendations": [
                    "Full depth patch replacement required at KM 7.820 cluster.",
                    "Core sample extraction recommended to verify sub-base compaction."
                ]
            },
            {
                "id": "insp-nh169-003",
                "project_id": "proj-nh169",
                "project_name": "NH-169 Road Development",
                "date": d3,
                "media_type": "image",
                "media_url": "/static/images/drone_road_aerial_3.svg",
                "thumbnail_url": "/static/images/drone_road_aerial_3.svg",
                "flight_duration_min": 32,
                "uav_pilot": "A. K. Verma (Lead Drone Specialist)",
                "progress_pct": 64.0,
                "completed_km": 7.68,
                "remaining_km": 4.32,
                "overall_condition": "Good",
                "health_score": 82,
                "summary_counts": {
                    "total_issues": 5,
                    "potholes": 1,
                    "surface_defects": 2,
                    "incomplete_sections": 2,
                    "high_severity": 1,
                    "medium_severity": 2,
                    "low_severity": 2
                },
                "detected_issues": [],
                "telemetry": {
                    "uav_platform": "DJI Matrice 300 RTK",
                    "flight_altitude_m": 45.0,
                    "ground_sampling_distance_cm_px": 1.10,
                    "flight_speed_m_s": 4.0,
                    "coordinates": {"latitude": 13.0780, "longitude": 75.0080}
                },
                "recommendations": [
                    "Continue grading and tack coat application along KM 7.600 corridor."
                ]
            }
        ]

        # Seed realistic reports
        self.data["reports"] = [
            {
                "id": "rep-nh169-001",
                "inspection_id": "insp-nh169-001",
                "project_id": "proj-nh169",
                "project_name": "NH-169 Road Development",
                "report_title": "Bi-Weekly Aerial Infrastructure Quality Audit",
                "generated_at": d1,
                "inspector_name": "Er. S. Nair, M.Tech (Highway Structures)",
                "authority": "Public Works Dept. & National Highways Authority",
                "status": "Certified",
                "progress_pct": 72.0,
                "overall_condition": "Fair",
                "total_issues": 7,
                "critical_actions": 2
            },
            {
                "id": "rep-nh169-002",
                "inspection_id": "insp-nh169-002",
                "project_id": "proj-nh169",
                "project_name": "NH-169 Road Development",
                "report_title": "Mid-Month Road Surface Defect Analysis",
                "generated_at": d2,
                "inspector_name": "Er. P. Hegde (Quality Assurance Directorate)",
                "authority": "National Highways Quality Wing",
                "status": "Archived",
                "progress_pct": 68.5,
                "overall_condition": "Fair",
                "total_issues": 9,
                "critical_actions": 3
            }
        ]

    def save(self):
        try:
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(self.data, f, indent=2)
        except Exception as e:
            print(f"[ProjectManager] Failed to save {self.data_file}: {e}")

    # --- Projects API ---
    def get_projects(self) -> List[Dict[str, Any]]:
        return self.data.get("projects", [])

    def get_project(self, project_id: str) -> Optional[Dict[str, Any]]:
        for p in self.data.get("projects", []):
            if p["id"] == project_id:
                return p
        return None

    def get_active_project(self) -> Dict[str, Any]:
        active_id = self.data.get("active_project_id", "proj-nh169")
        p = self.get_project(active_id)
        if not p and self.data["projects"]:
            p = self.data["projects"][0]
            self.data["active_project_id"] = p["id"]
        return p

    def set_active_project(self, project_id: str) -> bool:
        if self.get_project(project_id):
            self.data["active_project_id"] = project_id
            self.save()
            return True
        return False

    def add_project(self, project_data: Dict[str, Any]) -> Dict[str, Any]:
        new_id = f"proj-{int(datetime.now().timestamp())}"
        project = {
            "id": new_id,
            "name": project_data.get("name", "New Road Project"),
            "corridor_code": project_data.get("corridor_code", f"CORR-{datetime.now().year}"),
            "location": project_data.get("location", "Karnataka, India"),
            "coordinates": {
                "lat": float(project_data.get("lat", 13.0827)),
                "lng": float(project_data.get("lng", 75.0135))
            },
            "total_length_km": float(project_data.get("total_length_km", 10.0)),
            "progress_pct": float(project_data.get("progress_pct", 0.0)),
            "completed_km": round((float(project_data.get("progress_pct", 0.0)) / 100.0) * float(project_data.get("total_length_km", 10.0)), 2),
            "remaining_km": round(float(project_data.get("total_length_km", 10.0)) * (1.0 - float(project_data.get("progress_pct", 0.0)) / 100.0), 2),
            "status": project_data.get("status", "Active Construction"),
            "contractor": project_data.get("contractor", "State Highway Infrastructure Corp"),
            "last_inspection_date": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "total_inspections": 0,
            "open_issues": 0,
            "overall_condition": "Good",
            "description": project_data.get("description", "Highway corridor under automated UAV aerial surveillance.")
        }
        self.data["projects"].insert(0, project)
        self.data["active_project_id"] = new_id
        self.save()
        return project

    # --- Inspections API ---
    def get_inspections(self, project_id: Optional[str] = None) -> List[Dict[str, Any]]:
        inspections = self.data.get("inspections", [])
        if project_id:
            return [i for i in inspections if i.get("project_id") == project_id]
        return inspections

    def get_inspection(self, inspection_id: str) -> Optional[Dict[str, Any]]:
        for i in self.data.get("inspections", []):
            if i["id"] == inspection_id:
                return i
        return None

    def add_inspection(self, inspection_data: Dict[str, Any]) -> Dict[str, Any]:
        self.data["inspections"].insert(0, inspection_data)
        
        # Update associated project stats
        project = self.get_project(inspection_data["project_id"])
        if project:
            project["progress_pct"] = inspection_data.get("progress_pct", project["progress_pct"])
            project["completed_km"] = inspection_data.get("completed_km", project["completed_km"])
            project["remaining_km"] = inspection_data.get("remaining_km", project["remaining_km"])
            project["last_inspection_date"] = inspection_data.get("date", datetime.now().strftime("%Y-%m-%d %H:%M"))
            project["total_inspections"] = project.get("total_inspections", 0) + 1
            project["open_issues"] = inspection_data.get("summary_counts", {}).get("total_issues", project.get("open_issues", 0))
            project["overall_condition"] = inspection_data.get("overall_condition", project.get("overall_condition", "Good"))
        
        self.save()
        return inspection_data

    # --- Reports API ---
    def get_reports(self, project_id: Optional[str] = None) -> List[Dict[str, Any]]:
        reports = self.data.get("reports", [])
        if project_id:
            return [r for r in reports if r.get("project_id") == project_id]
        return reports

    def get_report(self, report_id: str) -> Optional[Dict[str, Any]]:
        for r in self.data.get("reports", []):
            if r["id"] == report_id:
                return r
        return None

    def create_report_from_inspection(self, inspection_id: str, title: Optional[str] = None) -> Optional[Dict[str, Any]]:
        inspection = self.get_inspection(inspection_id)
        if not inspection:
            return None

        report_id = f"rep-{int(datetime.now().timestamp())}"
        report = {
            "id": report_id,
            "inspection_id": inspection["id"],
            "project_id": inspection["project_id"],
            "project_name": inspection["project_name"],
            "report_title": title or f"Aerial Inspection Report - {inspection['date'][:10]}",
            "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "inspector_name": "Er. S. Nair, M.Tech (Highway Structures)",
            "authority": "National Highways Authority & PWD Monitoring Cell",
            "status": "Certified",
            "progress_pct": inspection.get("progress_pct", 72.0),
            "completed_km": inspection.get("completed_km", 8.64),
            "remaining_km": inspection.get("remaining_km", 3.36),
            "overall_condition": inspection.get("overall_condition", "Good"),
            "total_issues": inspection.get("summary_counts", {}).get("total_issues", 0),
            "critical_actions": inspection.get("summary_counts", {}).get("high_severity", 0),
            "inspection_data": inspection
        }
        self.data["reports"].insert(0, report)
        self.save()
        return report
