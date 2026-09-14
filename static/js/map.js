/**
 * RoadScan AI - Leaflet GIS Road Corridor Map
 */

function initCorridorMap(projectData, inspectionsData) {
    const mapElement = document.getElementById('corridor-map');
    if (!mapElement || typeof L === 'undefined') return;

    const lat = (projectData && projectData.coordinates && projectData.coordinates.lat) || 13.0827;
    const lng = (projectData && projectData.coordinates && projectData.coordinates.lng) || 75.0135;

    const map = L.map('corridor-map', {
        center: [lat, lng],
        zoom: 13,
        zoomControl: true,
        attributionControl: false
    });

    // Dark high-contrast basemap (CartoDB Dark Matter)
    L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', {
        maxZoom: 19,
        subdomains: 'abcd',
        attribution: '&copy; OpenStreetMap contributors &copy; CARTO'
    }).addTo(map);

    // Highway Alignment Polyline (Simulated NH-169 Segment)
    const roadPoints = [
        [lat - 0.025, lng - 0.035],
        [lat - 0.015, lng - 0.020],
        [lat - 0.005, lng - 0.008],
        [lat, lng],
        [lat + 0.008, lng + 0.012],
        [lat + 0.018, lng + 0.025],
        [lat + 0.030, lng + 0.040]
    ];

    // Paved Section (Cyan Glowing Corridor)
    const pavedSegment = roadPoints.slice(0, 5);
    L.polyline(pavedSegment, {
        color: '#0284c7',
        weight: 7,
        opacity: 0.9,
        lineCap: 'round',
        lineJoin: 'round'
    }).addTo(map).bindPopup(`<b>Paved Bituminous Corridor</b><br>NH-169 KM 0.000 to 8.640<br><span style="color:#38bdf8">Completed: 72%</span>`);

    // Incomplete Section (Amber Dashed Corridor)
    const unpavedSegment = roadPoints.slice(4);
    L.polyline(unpavedSegment, {
        color: '#f59e0b',
        weight: 6,
        dashArray: '8, 8',
        opacity: 0.9
    }).addTo(map).bindPopup(`<b>Unpaved / Under Construction</b><br>Sub-base grading ongoing (3.36 km remaining)`);

    // Custom High-Tech UAV Waypoint Icon
    const droneIcon = L.divIcon({
        className: 'custom-drone-pin',
        html: `<div style="background:#0284c7; width:28px; height:28px; border-radius:50%; border:2px solid #ffffff; display:flex; align-items:center; justify-content:center; box-shadow:0 0 12px #38bdf8;">
                <span style="font-size:14px;">🛸</span>
               </div>`,
        iconSize: [28, 28],
        iconAnchor: [14, 14]
    });

    // Drone Survey Hotspot Marker
    L.marker([lat, lng], { icon: droneIcon }).addTo(map)
        .bindPopup(`<b>Latest Aerial Survey Station</b><br>Altitude: 48.5m AGL<br>Platform: DJI Matrice 300 RTK<br>Detected Issues: 7`)
        .openPopup();

    // Defect Alert Hotspots
    const defectHotspots = [
        { lat: lat - 0.004, lng: lng - 0.006, title: "Pothole Cluster (HIGH)", desc: "KM 8.420 - Deep asphalt depression" },
        { lat: lat + 0.003, lng: lng + 0.005, title: "Longitudinal Cracks (MEDIUM)", desc: "KM 8.350 - Sealant required" }
    ];

    defectHotspots.forEach(defect => {
        L.circleMarker([defect.lat, defect.lng], {
            radius: 8,
            fillColor: '#ef4444',
            color: '#ffffff',
            weight: 2,
            opacity: 1,
            fillOpacity: 0.85
        }).addTo(map).bindPopup(`<b>${defect.title}</b><br>${defect.desc}`);
    });
}
