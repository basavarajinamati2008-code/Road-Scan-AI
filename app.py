"""
RoadScan AI - Automated Aerial Road Monitoring System
Main Flask Application Server
"""

import os
import uuid
from datetime import datetime
from flask import Flask, render_template, request, jsonify, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename

from services.project_manager import ProjectManager
from services.ai_engine import get_analyzer

app = Flask(__name__)
app.config['SECRET_KEY'] = 'roadscan-ai-secure-secret-2026'
app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(__file__), 'static', 'uploads')
app.config['MAX_CONTENT_LENGTH'] = 64 * 1024 * 1024  # 64MB max upload
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'mp4', 'svg'}

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Initialize project manager and AI engine
pm = ProjectManager(data_file=os.path.join(os.path.dirname(__file__), 'data', 'store.json'))
analyzer = get_analyzer(mode="simulated")


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# --------------------------------------------------------------------------
# Web Page Routes
# --------------------------------------------------------------------------

@app.route('/')
def dashboard():
    active_project = pm.get_active_project()
    projects = pm.get_projects()
    inspections = pm.get_inspections(active_project['id'] if active_project else None)
    reports = pm.get_reports(active_project['id'] if active_project else None)

    # Calculate aggregate summary stats
    latest_inspection = inspections[0] if inspections else None
    
    return render_template(
        'index.html',
        active_project=active_project,
        projects=projects,
        inspections=inspections[:6],  # Most recent
        latest_inspection=latest_inspection,
        reports_count=len(reports)
    )


@app.route('/projects')
def projects_page():
    active_project = pm.get_active_project()
    projects = pm.get_projects()
    return render_template(
        'projects.html',
        active_project=active_project,
        projects=projects
    )


@app.route('/upload')
def upload_page():
    active_project = pm.get_active_project()
    projects = pm.get_projects()
    sample_images = [
        {
            "id": "sample-1",
            "name": "NH-169 Active Paving Chainage (KM 8.420)",
            "url": "/static/images/drone_road_aerial_1.svg",
            "type": "image",
            "desc": "Fresh asphalt carriageway transitioning to granular sub-base, with visible surface distress & machine activity."
        },
        {
            "id": "sample-2",
            "name": "NH-169 Sector 7 Curve & Fatigue Cracking",
            "url": "/static/images/drone_road_aerial_2.svg",
            "type": "image",
            "desc": "Curved highway section with transverse pothole cluster and longitudinal wheel path fatigue cracking."
        },
        {
            "id": "sample-3",
            "name": "Granular Sub-Base & Roller Compaction Pass",
            "url": "/static/images/drone_road_aerial_3.svg",
            "type": "image",
            "desc": "Unpaved sub-base corridor under mechanical grading and vibratory roller pass prior to prime coat."
        }
    ]
    return render_template(
        'upload.html',
        active_project=active_project,
        projects=projects,
        sample_images=sample_images
    )


@app.route('/inspections/<inspection_id>')
def inspection_detail(inspection_id):
    active_project = pm.get_active_project()
    inspection = pm.get_inspection(inspection_id)
    if not inspection:
        return redirect(url_for('dashboard'))
    return render_template(
        'inspection_detail.html',
        active_project=active_project,
        inspection=inspection
    )


@app.route('/reports')
def reports_page():
    active_project = pm.get_active_project()
    reports = pm.get_reports()
    inspections = pm.get_inspections()
    return render_template(
        'reports.html',
        active_project=active_project,
        reports=reports,
        inspections=inspections
    )


# --------------------------------------------------------------------------
# REST API Endpoints
# --------------------------------------------------------------------------

@app.route('/api/stats')
def api_stats():
    active_project = pm.get_active_project()
    inspections = pm.get_inspections(active_project['id'] if active_project else None)
    return jsonify({
        "project": active_project,
        "inspections": inspections
    })


@app.route('/api/projects/set-active', methods=['POST'])
def api_set_active_project():
    data = request.get_json() or {}
    project_id = data.get('project_id')
    if pm.set_active_project(project_id):
        return jsonify({"status": "success", "active_project": pm.get_active_project()})
    return jsonify({"status": "error", "message": "Project not found"}), 404


@app.route('/api/projects', methods=['POST'])
def api_create_project():
    data = request.get_json() or {}
    name = data.get('name', '').strip()
    if not name:
        return jsonify({"status": "error", "message": "Project name is required"}), 400
    
    new_project = pm.add_project(data)
    return jsonify({"status": "success", "project": new_project})


@app.route('/api/analyze', methods=['POST'])
def api_analyze():
    """
    Simulated AI Analysis Pipeline endpoint.
    Accepts an uploaded file OR a preset sample image URL.
    """
    active_project = pm.get_active_project()
    if not active_project:
        return jsonify({"status": "error", "message": "No active project selected"}), 400

    media_url = None
    media_type = "image"
    original_filename = "aerial_survey.jpg"

    # Check if a file was uploaded
    if 'file' in request.files and request.files['file'].filename != '':
        file = request.files['file']
        if allowed_file(file.filename):
            ext = file.filename.rsplit('.', 1)[1].lower()
            original_filename = secure_filename(file.filename)
            unique_filename = f"drone_{uuid.uuid4().hex[:10]}.{ext}"
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
            file.save(file_path)
            media_url = f"/static/uploads/{unique_filename}"
            if ext == 'mp4':
                media_type = "video"
    else:
        # Check if sample image was provided in form data or json
        sample_url = request.form.get('sample_url') or (request.get_json() or {}).get('sample_url')
        if sample_url:
            media_url = sample_url
            original_filename = sample_url.split('/')[-1]

    # Default fallback to sample 1 if none provided
    if not media_url:
        media_url = "/static/images/drone_road_aerial_1.svg"
        original_filename = "drone_road_aerial_1.svg"

    # Run AI Analysis via Engine
    analysis_results = analyzer.analyze_media(
        media_path=media_url,
        media_type=media_type,
        project_metadata=active_project
    )

    # Persist as a new official Inspection Record
    inspection_id = f"insp-{uuid.uuid4().hex[:8]}"
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M")
    
    inspection_record = {
        "id": inspection_id,
        "project_id": active_project["id"],
        "project_name": active_project["name"],
        "date": now_str,
        "media_type": media_type,
        "media_url": media_url,
        "thumbnail_url": media_url,
        "original_filename": original_filename,
        "flight_duration_min": 22,
        "uav_pilot": "Capt. R. Sharma (DGCA Certified)",
        **analysis_results
    }

    pm.add_inspection(inspection_record)

    # Automatically generate an associated inspection report
    report = pm.create_report_from_inspection(
        inspection_id=inspection_id,
        title=f"Aerial Road Inspection Audit - {now_str[:10]}"
    )

    return jsonify({
        "status": "success",
        "inspection": inspection_record,
        "report_id": report["id"] if report else None,
        "redirect_url": f"/inspections/{inspection_id}"
    })


@app.route('/api/reports/generate', methods=['POST'])
def api_generate_report():
    data = request.get_json() or {}
    inspection_id = data.get('inspection_id')
    title = data.get('title')
    report = pm.create_report_from_inspection(inspection_id, title)
    if report:
        return jsonify({"status": "success", "report": report})
    return jsonify({"status": "error", "message": "Inspection not found"}), 404


@app.route('/api/reports/<report_id>')
def api_get_report(report_id):
    report = pm.get_report(report_id)
    if report:
        return jsonify({"status": "success", "report": report})
    return jsonify({"status": "error", "message": "Report not found"}), 404


if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
