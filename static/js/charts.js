/**
 * RoadScan AI - Analytics & Chart Visualizations
 */

function initDashboardCharts(inspectionsData, projectData) {
    initProgressChart(inspectionsData);
    initDefectsChart(inspectionsData);
}

function initProgressChart(inspections) {
    const ctx = document.getElementById('progress-chart');
    if (!ctx) return;

    // Sort chronologically
    const sorted = [...inspections].reverse();
    const labels = sorted.map(i => i.date ? i.date.slice(5, 10) : 'Date');
    const dataProgress = sorted.map(i => i.progress_pct);
    const targetProgress = sorted.map((_, idx) => Math.min(100, 60 + idx * 4));

    new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels.length ? labels : ['Survey 1', 'Survey 2', 'Survey 3'],
            datasets: [
                {
                    label: 'Actual Road Paving Progress (%)',
                    data: dataProgress.length ? dataProgress : [64, 68.5, 72],
                    borderColor: '#38bdf8',
                    backgroundColor: 'rgba(56, 189, 248, 0.15)',
                    borderWidth: 3,
                    fill: true,
                    tension: 0.35,
                    pointBackgroundColor: '#0284c7',
                    pointBorderColor: '#ffffff',
                    pointRadius: 5,
                    pointHoverRadius: 7
                },
                {
                    label: 'Contract Schedule Target (%)',
                    data: targetProgress.length ? targetProgress : [62, 66, 70],
                    borderColor: '#94a3b8',
                    borderWidth: 2,
                    borderDash: [5, 5],
                    fill: false,
                    tension: 0.2,
                    pointRadius: 0
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'top',
                    labels: { color: '#94a3b8', font: { family: 'Inter', size: 12 } }
                },
                tooltip: {
                    backgroundColor: '#0f172a',
                    titleColor: '#38bdf8',
                    bodyColor: '#f8fafc',
                    borderColor: '#334155',
                    borderWidth: 1,
                    padding: 12
                }
            },
            scales: {
                x: {
                    grid: { color: 'rgba(51, 65, 85, 0.3)' },
                    ticks: { color: '#94a3b8' }
                },
                y: {
                    min: 0,
                    max: 100,
                    grid: { color: 'rgba(51, 65, 85, 0.3)' },
                    ticks: {
                        color: '#94a3b8',
                        callback: function (value) { return value + '%'; }
                    }
                }
            }
        }
    });
}

function initDefectsChart(inspections) {
    const ctx = document.getElementById('defects-chart');
    if (!ctx) return;

    // Use latest inspection counts or fallback
    const latest = inspections && inspections.length ? inspections[0] : null;
    const counts = latest && latest.summary_counts ? latest.summary_counts : {
        potholes: 2,
        surface_defects: 3,
        incomplete_sections: 2
    };

    new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: ['Pothole Hazards', 'Surface Cracking & Raveling', 'Incomplete Pavement Layer'],
            datasets: [{
                data: [counts.potholes, counts.surface_defects, counts.incomplete_sections],
                backgroundColor: [
                    '#ef4444', // Red for Potholes
                    '#f59e0b', // Amber for Surface Distress
                    '#38bdf8'  // Cyan for Incomplete Section
                ],
                borderWidth: 2,
                borderColor: '#0f172a'
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'bottom',
                    labels: { color: '#94a3b8', font: { family: 'Inter', size: 11 }, padding: 14 }
                },
                tooltip: {
                    backgroundColor: '#0f172a',
                    titleColor: '#f8fafc',
                    borderColor: '#334155',
                    borderWidth: 1,
                    padding: 10
                }
            },
            cutout: '72%'
        }
    });
}
