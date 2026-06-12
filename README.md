# Gilgit-Baltistan Glacier Monitoring DSS — Demo Dashboard

This is a simple demo dashboard for the Environmental Informatics case study: **Glacier Monitoring System for Gilgit-Baltistan**.

It is designed for class demonstration. It does **not** claim a fully operational system.
It connects the idea of different services in one simple GUI:

- RGI/GLIMS glacier outlines
- Google Earth Engine for Landsat/Sentinel NDSI/NDWI
- Copernicus Browser for Sentinel-1/2 scene search
- ESA SNAP for Sentinel-1 SAR workflow
- ERA5-Land for climate variables
- WAPDA/PMD river-flow context
- NDMA official website/advisories/SITREPs/projection links
- KoboToolbox/ODK for community reporting
- QGIS/PostGIS for GIS storage and spatial queries
- Streamlit/Leaflet/Power BI style dashboard layer

## Folder contents

- `app.py` — Streamlit demo dashboard
- `data/` — small demo CSV files
- `backend/connectors.py` — simulated backend service connector logic
- `gee_scripts/hunza_batura_ndsi_demo.js` — GEE JavaScript demo for NDSI
- `demo_dashboard.html` — static dashboard mockup, opens directly in browser
- `requirements.txt` — Python packages

## How to run the Streamlit dashboard

1. Open terminal in this folder.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Run:

```bash
streamlit run app.py
```

4. Browser will open the dashboard.

## How to use for presentation

Use this explanation:

> This dashboard is the decision-support layer. It does not replace scientific processing. GEE prepares NDSI/NDWI maps, QGIS/PostGIS connects those maps with settlements and infrastructure, SAR tools support velocity/deformation checks for priority glaciers, climate and discharge records add water-resource context, and community forms add ground observations. The dashboard joins everything into one basin scorecard.

## What is real and what is demo?

Real concept:
- The dashboard architecture, service mapping, tool roles and decision outputs.

Demo data:
- The CSV values are simplified/sample values for presentation.
- The service buttons open sources or simulate backend jobs.
- Live API integration is not enabled to keep the project simple.

## How to extend later

- Replace demo glacier points with RGI/GLIMS glacier polygons.
- Replace CSV indicators with outputs exported from GEE.
- Add PostGIS connection.
- Add Streamlit-Folium or GeoServer map services.
- Add Earth Engine Python API.
- Add Kobo/ODK form exports.
- Add PMD/WAPDA/IRSA data ingestion.


## NDMA links added in this updated version

The dashboard now includes public NDMA links:

- NDMA official website: https://www.ndma.gov.pk/
- NDMA advisories: https://www.ndma.gov.pk/advisories
- NDMA situation reports: https://www.ndma.gov.pk/sitreps
- NDMA latest projections and impacts: https://www.ndma.gov.pk/projection-impact
- NDMA admin dashboard login: https://www.ndma.gov.pk/login

Note: the admin dashboard is shown only as an official login point. This demo does not access private NDMA data, does not use credentials, and does not scrape restricted pages. For class purposes, use the public advisories, SITREPs and projection pages.


## Latest update
Removed the private/broken NDMA login link. Added global reference dashboards: NASA Worldview, GLIMS Glacier Viewer, WGMS Glacier Browser, Copernicus Glacier Mass Change, Copernicus GloFAS, Copernicus EMS Mapping, and Google Flood Hub. These are reference dashboards, not live backend integrations in this demo.
