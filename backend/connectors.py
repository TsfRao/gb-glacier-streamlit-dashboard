"""
Demo backend connectors for the GB Glacier DSS.
This is intentionally light. It does not call paid/live APIs. It shows how each service
would be connected in a real deployment.
"""

from datetime import datetime
import pandas as pd


def load_service_catalog(path="data/service_catalog.csv"):
    return pd.read_csv(path)


def simulate_service_job(service_key: str, basin: str, start_year: int, end_year: int) -> dict:
    """
    Demo job runner. In real deployment, this function can be replaced with:
    - Earth Engine Python API jobs
    - CDS API request
    - WAPDA/PMD data ingestion scripts
    - PostGIS stored procedures
    - SNAP graph processing jobs
    """
    messages = {
        "rgi_glims": "Loaded glacier outlines into the inventory layer.",
        "gee": "Prepared NDSI/NDWI time-series task for GEE.",
        "usgs": "Prepared Landsat scene search query.",
        "copernicus": "Prepared Sentinel-1/2 scene search query.",
        "snap": "Prepared Sentinel-1 SAR processing workflow note.",
        "era5": "Prepared temperature and precipitation request.",
        "pmd_ffd": "Prepared current river-state record entry.",
        "wapda": "Prepared discharge observation entry.",
        "kobo": "Prepared community observation survey link.",
        "ndma_site": "Opened NDMA official reference link for national disaster-management context.",
        "ndma_advisories": "Prepared NDMA advisory/GLOF alert check for the preparedness panel.",
        "ndma_sitreps": "Prepared NDMA SITREP reference entry for official situation reporting.",
        "ndma_projection": "Prepared NDMA latest projections/impact reference entry.",
        "nasa_worldview": "Opened NASA Worldview for global satellite imagery comparison.",
        "glims_viewer": "Opened GLIMS Glacier Viewer for glacier outline verification.",
        "wgms_browser": "Opened WGMS glacier-change browser for global glacier statistics.",
        "cds_glacier_mass": "Opened Copernicus global glacier mass-change dataset.",
        "glofas": "Opened Copernicus GloFAS for flood forecast and monitoring context.",
        "copernicus_mapping": "Opened Copernicus EMS On-Demand Mapping for disaster maps.",
        "google_floodhub": "Opened Google Flood Hub for AI-based river flood forecast context.",
    }
    return {
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "service_key": service_key,
        "basin": basin,
        "period": f"{start_year}-{end_year}",
        "status": "DEMO_READY",
        "message": messages.get(service_key, "Demo service action prepared."),
    }


def score_basin(row) -> str:
    risk = int(row.get("risk_score", 0))
    if risk >= 70:
        return "High concern"
    if risk >= 50:
        return "Watch"
    return "Normal"
