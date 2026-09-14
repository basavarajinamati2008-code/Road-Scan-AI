/**
 * RoadScan AI - Front-End Application Logic
 * Automated Aerial Road Monitoring System
 */

document.addEventListener('DOMContentLoaded', () => {
    lucide.createIcons();
    initProjectSelector();
    initUploadPage();
    initInspectionCanvas();
    initReportGenerator();
});

// =============================================================================
// Project Switcher & Modal
// =============================================================================
function initProjectSelector() {
    const projectSelect = document.getElementById('project-quick-select');
    if (projectSelect) {
        projectSelect.addEventListener('change', async (e) => {
            const projectId = e.target.value;
            try {
                const res = await fetch('/api/projects/set-active', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ project_id: projectId })
                });
                if (res.ok) {
                    window.location.reload();
                }
            } catch (err) {
                console.error('Failed to change active project:', err);
            }
        });
    }

    // New Project Modal
    const createProjectForm = document.getElementById('create-project-form');
    if (createProjectForm) {
        createProjectForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const formData = new FormData(createProjectForm);
            const payload = {
                name: formData.get('name'),
                location: formData.get('location'),
                total_length_km: parseFloat(formData.get('total_length_km')),
                progress_pct: parseFloat(formData.get('progress_pct') || 0),
                contractor: formData.get('contractor'),
                description: formData.get('description')
            };

            try {
                const res = await fetch('/api/projects', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(payload)
                });
                const data = await res.json();
                if (data.status === 'success') {
                    window.location.href = '/projects';
                } else {
                    alert(data.message || 'Failed to create project');
                }
            } catch (err) {
                console.error('Error creating project:', err);
            }
        });
    }
}

// =============================================================================
// Upload & Staged AI Analysis Simulation
// =============================================================================
function initUploadPage() {
    const uploadDropzone = document.getElementById('upload-dropzone');
    const fileInput = document.getElementById('file-input');
    const previewContainer = document.getElementById('media-preview-container');
    const previewImage = document.getElementById('preview-image');
    const previewVideo = document.getElementById('preview-video');
    const previewFilename = document.getElementById('preview-filename');
    const previewFilesize = document.getElementById('preview-filesize');
    const analyzeBtn = document.getElementById('analyze-btn');
    const sampleCards = document.querySelectorAll('.sample-dataset-card');

    let selectedFile = null;
    let selectedSampleUrl = null;

    if (!uploadDropzone) return;

    // Preset Sample Selectors
    sampleCards.forEach(card => {
        card.addEventListener('click', () => {
            sampleCards.forEach(c => c.classList.remove('ring-2', 'ring-sky-400', 'bg-slate-800/80'));
            card.classList.add('ring-2', 'ring-sky-400', 'bg-slate-800/80');

            selectedSampleUrl = card.dataset.url;
            selectedFile = null;

            // Show Preview
            if (previewVideo) previewVideo.classList.add('hidden');
            if (previewImage) {
                previewImage.src = selectedSampleUrl;
                previewImage.classList.remove('hidden');
            }
            if (previewContainer) previewContainer.classList.remove('hidden');
            if (previewFilename) previewFilename.textContent = card.dataset.name;
            if (previewFilesize) previewFilesize.textContent = "Preset Aerial Survey Sample";
            if (analyzeBtn) analyzeBtn.removeAttribute('disabled');

            previewContainer.scrollIntoView({ behavior: 'smooth', block: 'center' });
        });
    });

    // File Input / Drag & Drop
    uploadDropzone.addEventListener('click', () => fileInput && fileInput.click());

    ['dragenter', 'dragover'].forEach(eventName => {
        uploadDropzone.addEventListener(eventName, (e) => {
            e.preventDefault();
            uploadDropzone.classList.add('border-sky-400', 'bg-slate-800/60');
        }, false);
    });

    ['dragleave', 'drop'].forEach(eventName => {
        uploadDropzone.addEventListener(eventName, (e) => {
            e.preventDefault();
            uploadDropzone.classList.remove('border-sky-400', 'bg-slate-800/60');
        }, false);
    });

    uploadDropzone.addEventListener('drop', (e) => {
        const dt = e.dataTransfer;
        const files = dt.files;
        if (files && files.length) {
            handleFileSelect(files[0]);
        }
    });

    if (fileInput) {
        fileInput.addEventListener('change', (e) => {
            if (e.target.files && e.target.files.length) {
                handleFileSelect(e.target.files[0]);
            }
        });
    }

    function handleFileSelect(file) {
        selectedFile = file;
        selectedSampleUrl = null;
        sampleCards.forEach(c => c.classList.remove('ring-2', 'ring-sky-400', 'bg-slate-800/80'));

        const isVideo = file.type.includes('video') || file.name.endsWith('.mp4');
        const fileUrl = URL.createObjectURL(file);

        if (isVideo) {
            if (previewImage) previewImage.classList.add('hidden');
            if (previewVideo) {
                previewVideo.src = fileUrl;
                previewVideo.classList.remove('hidden');
            }
        } else {
            if (previewVideo) previewVideo.classList.add('hidden');
            if (previewImage) {
                previewImage.src = fileUrl;
                previewImage.classList.remove('hidden');
            }
        }

        if (previewContainer) previewContainer.classList.remove('hidden');
        if (previewFilename) previewFilename.textContent = file.name;
        if (previewFilesize) previewFilesize.textContent = (file.size / (1024 * 1024)).toFixed(2) + ' MB';
        if (analyzeBtn) analyzeBtn.removeAttribute('disabled');

        previewContainer.scrollIntoView({ behavior: 'smooth', block: 'center' });
    }

    // AI Analysis Trigger & Realistic Loading Animation
    if (analyzeBtn) {
        analyzeBtn.addEventListener('click', async () => {
            if (!selectedFile && !selectedSampleUrl) {
                alert('Please upload an aerial image/video or select a sample dataset.');
                return;
            }

            openAnalysisModal();
            runSimulatedInferencePipeline(selectedFile, selectedSampleUrl);
        });
    }
}

/**
 * Realistic Staged Progress Simulation with Live Status Log
 */
async function runSimulatedInferencePipeline(file, sampleUrl) {
    const statusText = document.getElementById('analysis-status-text');
    const progressBar = document.getElementById('analysis-progress-bar');
    const progressPercent = document.getElementById('analysis-percent-text');
    const consoleLogs = document.getElementById('analysis-console-logs');

    function logStep(message, pct) {
        if (statusText) statusText.textContent = message;
        if (progressBar) progressBar.style.width = `${pct}%`;
        if (progressPercent) progressPercent.textContent = `${pct}%`;
        if (consoleLogs) {
            const line = document.createElement('div');
            line.className = 'text-xs font-mono text-slate-300 flex items-center gap-2 py-0.5';
            line.innerHTML = `<span class="text-sky-400 font-bold">●</span> <span>[${new Date().toLocaleTimeString()}]</span> <span>${message}</span>`;
            consoleLogs.appendChild(line);
            consoleLogs.scrollTop = consoleLogs.scrollHeight;
        }
    }

    try {
        logStep("Initializing RoadScan AI neural pipeline & GPU context...", 10);
        await sleep(700);

        logStep("Ingesting aerial telemetry & orthorectifying coordinate space...", 28);
        await sleep(800);

        logStep("Segmenting asphalt carriageway vs. earthen shoulder corridor...", 48);
        await sleep(900);

        logStep("Executing YOLOv8 pavement distress detector (Potholes, Cracking, Raveling)...", 72);
        await sleep(950);

        logStep("Computing chainage progress metrics & IRC severity classification...", 88);
        await sleep(800);

        logStep("Finalizing inspection metadata and generating audit report...", 96);

        // Send request to Flask API
        const formData = new FormData();
        if (file) {
            formData.append('file', file);
        } else if (sampleUrl) {
            formData.append('sample_url', sampleUrl);
        }

        const response = await fetch('/api/analyze', {
            method: 'POST',
            body: formData
        });

        const result = await response.json();
        if (result.status === 'success') {
            logStep("Inspection completed successfully! Redirecting to Inspection Studio...", 100);
            await sleep(600);
            window.location.href = result.redirect_url;
        } else {
            alert(result.message || 'Analysis encountered an error');
            closeAnalysisModal();
        }
    } catch (err) {
        console.error('Inference error:', err);
        alert('Analysis request failed. Please check server logs.');
        closeAnalysisModal();
    }
}

function openAnalysisModal() {
    const modal = document.getElementById('analysis-modal');
    if (modal) {
        modal.classList.remove('hidden');
        modal.classList.add('flex');
    }
}

function closeAnalysisModal() {
    const modal = document.getElementById('analysis-modal');
    if (modal) {
        modal.classList.add('hidden');
        modal.classList.remove('flex');
    }
}

function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

// =============================================================================
// Interactive AI Inspection Canvas with Bounding Boxes
// =============================================================================
function initInspectionCanvas() {
    const canvasContainer = document.getElementById('inspection-canvas-overlay');
    const defectListItems = document.querySelectorAll('.defect-list-item');
    const filterButtons = document.querySelectorAll('.defect-filter-btn');
    const toggleBoxesCheckbox = document.getElementById('toggle-bounding-boxes');
    const toggleScanlineCheckbox = document.getElementById('toggle-scanline');
    const scanlineElem = document.querySelector('.scanline');

    if (!canvasContainer || !window.INSPECTION_ISSUES) return;

    const issues = window.INSPECTION_ISSUES;

    // Render Bounding Boxes dynamically
    function renderBoxes(filteredIssues) {
        canvasContainer.innerHTML = '';

        filteredIssues.forEach(issue => {
            const bbox = issue.bbox;
            if (!bbox) return;

            const box = document.createElement('div');
            box.className = `ai-overlay-box severity-${issue.severity}`;
            box.id = `box-${issue.id}`;
            box.style.left = `${bbox.x}%`;
            box.style.top = `${bbox.y}%`;
            box.style.width = `${bbox.width}%`;
            box.style.height = `${bbox.height}%`;

            const label = document.createElement('div');
            label.className = 'ai-box-label';
            label.textContent = `${issue.label} (${(issue.confidence * 100).toFixed(0)}%)`;
            box.appendChild(label);

            // Click box -> highlight item in defect list
            box.addEventListener('click', (e) => {
                e.stopPropagation();
                highlightDefect(issue.id);
            });

            canvasContainer.appendChild(box);
        });
    }

    renderBoxes(issues);

    // Filter Buttons (All, High, Medium, Low)
    filterButtons.forEach(btn => {
        btn.addEventListener('click', () => {
            filterButtons.forEach(b => b.classList.remove('bg-sky-500', 'text-white', 'border-sky-400'));
            filterButtons.forEach(b => b.classList.add('bg-slate-800', 'text-slate-300'));

            btn.classList.add('bg-sky-500', 'text-white', 'border-sky-400');
            btn.classList.remove('bg-slate-800', 'text-slate-300');

            const filter = btn.dataset.filter;
            const filtered = filter === 'ALL' ? issues : issues.filter(i => i.severity === filter);
            renderBoxes(filtered);

            // Filter the sidebar list as well
            defectListItems.forEach(item => {
                if (filter === 'ALL' || item.dataset.severity === filter) {
                    item.classList.remove('hidden');
                } else {
                    item.classList.add('hidden');
                }
            });
        });
    });

    // Hover defect list item -> pulse corresponding bounding box
    defectListItems.forEach(item => {
        item.addEventListener('mouseenter', () => {
            const issueId = item.dataset.id;
            const box = document.getElementById(`box-${issueId}`);
            if (box) box.classList.add('active');
        });
        item.addEventListener('mouseleave', () => {
            const issueId = item.dataset.id;
            const box = document.getElementById(`box-${issueId}`);
            if (box) box.classList.remove('active');
        });
        item.addEventListener('click', () => {
            highlightDefect(item.dataset.id);
        });
    });

    function highlightDefect(id) {
        document.querySelectorAll('.ai-overlay-box').forEach(b => b.classList.remove('active'));
        document.querySelectorAll('.defect-list-item').forEach(i => i.classList.remove('ring-2', 'ring-sky-400', 'bg-slate-800'));

        const targetBox = document.getElementById(`box-${id}`);
        const targetItem = document.querySelector(`.defect-list-item[data-id="${id}"]`);

        if (targetBox) targetBox.classList.add('active');
        if (targetItem) {
            targetItem.classList.add('ring-2', 'ring-sky-400', 'bg-slate-800');
            targetItem.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
        }
    }

    // Toggle Toggles
    if (toggleBoxesCheckbox) {
        toggleBoxesCheckbox.addEventListener('change', (e) => {
            canvasContainer.style.display = e.target.checked ? 'block' : 'none';
        });
    }

    if (toggleScanlineCheckbox && scanlineElem) {
        toggleScanlineCheckbox.addEventListener('change', (e) => {
            scanlineElem.style.display = e.target.checked ? 'block' : 'none';
        });
    }
}

// =============================================================================
// PDF Report Generator & Download
// =============================================================================
function initReportGenerator() {
    const downloadPdfBtn = document.getElementById('download-pdf-btn');
    const printReportBtn = document.getElementById('print-report-btn');
    const reportContent = document.getElementById('printable-report-card');

    if (printReportBtn) {
        printReportBtn.addEventListener('click', () => {
            window.print();
        });
    }

    if (downloadPdfBtn && reportContent) {
        downloadPdfBtn.addEventListener('click', () => {
            downloadPdfBtn.disabled = true;
            downloadPdfBtn.innerHTML = `<i data-lucide="loader-2" class="w-4 h-4 animate-spin"></i> Compiling PDF...`;
            lucide.createIcons();

            const opt = {
                margin: [10, 10, 10, 10],
                filename: `RoadScan_AI_Inspection_${new Date().toISOString().slice(0, 10)}.pdf`,
                image: { type: 'jpeg', quality: 0.98 },
                html2canvas: { scale: 2, useCORS: true, logging: false },
                jsPDF: { unit: 'mm', format: 'a4', orientation: 'portrait' }
            };

            if (window.html2pdf) {
                html2pdf().set(opt).from(reportContent).save().then(() => {
                    downloadPdfBtn.disabled = false;
                    downloadPdfBtn.innerHTML = `<i data-lucide="download" class="w-4 h-4"></i> Download PDF Report`;
                    lucide.createIcons();
                }).catch(err => {
                    console.error('PDF generation error:', err);
                    window.print();
                    downloadPdfBtn.disabled = false;
                    downloadPdfBtn.innerHTML = `<i data-lucide="download" class="w-4 h-4"></i> Download PDF Report`;
                    lucide.createIcons();
                });
            } else {
                window.print();
                downloadPdfBtn.disabled = false;
                downloadPdfBtn.innerHTML = `<i data-lucide="download" class="w-4 h-4"></i> Download PDF Report`;
                lucide.createIcons();
            }
        });
    }
}
