import streamlit as st
import pandas as pd
import os, sys

sys.path.append(os.path.join(os.path.dirname(__file__), "backend"))
from connectors import simulate_service_job, score_basin

st.set_page_config(page_title="GB Glacier DSS Demo", layout="wide")

@st.cache_data
def load_data():
    glaciers = pd.read_csv("data/glacier_points.csv")
    indicators = pd.read_csv("data/basin_indicators.csv")
    ts = pd.read_csv("data/hunza_demo_timeseries.csv")
    services = pd.read_csv("data/service_catalog.csv")
    return glaciers, indicators, ts, services

glaciers, indicators, ts, services = load_data()

if "job_log" not in st.session_state:
    st.session_state.job_log = []

st.title("Gilgit-Baltistan Glacier Monitoring DSS — Demo Dashboard")
st.caption("Demo purpose only: connects GEE, GIS, SAR, climate, discharge and community observations into one simple interface.")

with st.sidebar:
    st.header("Pilot control")
    basin = st.selectbox("Select basin", sorted(indicators["basin"].unique()), index=0)
    start_year, end_year = st.slider("Monitoring period", 1998, 2025, (2013, 2023))
    selected_module = st.radio("Monitoring mode", ["Overview", "Optical NDSI/NDWI", "SAR priority", "Climate/flow", "Community reports"])
    st.info("Use service buttons to open source platforms. Use demo backend actions to show how jobs would be prepared.")

row = indicators[indicators["basin"] == basin].sort_values("year").tail(1).iloc[0]
status = score_basin(row)

k1, k2, k3, k4, k5 = st.columns(5)
k1.metric("Basin status", status, f"Risk score {int(row['risk_score'])}")
k2.metric("Snow-cover status", row["snow_cover_status"], f"{row['snow_cover_area_km2']} km² demo")
k3.metric("Lake status", row["lake_status"], f"{row['lake_area_change_pct']}% change")
k4.metric("SAR status", row["sar_velocity_status"])
k5.metric("Community reports", int(row["community_reports"]))

tabs = st.tabs(["Dashboard", "One-click services", "Map & layers", "Workflow", "Backend log", "How to explain"])

with tabs[0]:
    st.subheader("Basin scorecard")
    st.write("This page shows how scattered data sources can be joined into a single decision-support view for GB glacier monitoring.")
    col1, col2 = st.columns([1.3, 1])
    with col1:
        st.line_chart(ts.set_index("year")[["Batura_SCA_km2", "Demo_lake_area_km2", "Demo_discharge_index"]])
    with col2:
        st.dataframe(indicators[indicators["basin"] == basin], use_container_width=True)
        st.warning("Demo interpretation: if snow-cover decreases, lake expands, SAR indicates unusual motion, and community reports increase, the basin moves to Watch/High Concern.")

with tabs[1]:
    st.subheader("One-click service launcher")
    st.write("These buttons open the relevant service or prepare a demo backend action. Live APIs can be added later.")
    for _, s in services.iterrows():
        with st.container(border=True):
            c1, c2, c3 = st.columns([1.6, 1, 1])
            c1.markdown(f"**{s['service_name']}**  \n{s['category']} → {s['expected_output']}")
            c2.markdown(f"Tool: `{s['tool']}`")
            c3.link_button("Open service", s["url"], use_container_width=True)
            if st.button(f"Prepare backend job: {s['service_key']}", key=f"job_{s['service_key']}"):
                st.session_state.job_log.append(simulate_service_job(s["service_key"], basin, start_year, end_year))
                st.success(f"Demo job prepared for {s['service_name']}")

with tabs[2]:
    st.subheader("Pilot map: glaciers and priority points")
    map_df = glaciers.rename(columns={"lat":"latitude","lon":"longitude"})[["latitude","longitude"]]
    st.map(map_df)
    st.dataframe(glaciers[["glacier_id","glacier","basin","module","priority","note"]], use_container_width=True)
    st.caption("For a real map, replace this with GeoJSON glacier polygons, village points, river network and road layers in Leaflet/Folium or GeoServer.")

with tabs[3]:
    st.subheader("Simple workflow")
    st.markdown("""
    1. Load **RGI/GLIMS glacier outlines**.  
    2. Run **GEE NDSI/NDWI** for snow cover and lake area.  
    3. Overlay outputs in **QGIS/PostGIS** with villages, roads, river network and infrastructure.  
    4. For selected priority glaciers, run **Sentinel-1 SAR/SNAP** velocity/deformation workflow.  
    5. Add **ERA5-Land/PMD** temperature and precipitation context.  
    6. Add **WAPDA/IRSA/PMD-FFD** discharge context.  
    7. Add **Kobo/ODK** community observations.  
    8. Compare dashboard status with **NDMA advisories/SITREPs/projection pages** for official Pakistan context.  
    9. Open global reference dashboards such as **NASA Worldview, GLIMS Viewer, WGMS Browser, Copernicus GloFAS and Google Flood Hub** for comparison.  
    10. Publish basin scorecard, maps, alerts and short policy report.
    """)
    st.code("Satellite + field + hydro + community data -> PostGIS -> Dashboard/DSS -> planning decision", language="text")

with tabs[4]:
    st.subheader("Backend demo log")
    if st.session_state.job_log:
        st.dataframe(pd.DataFrame(st.session_state.job_log), use_container_width=True)
    else:
        st.info("No demo backend jobs yet. Go to 'One-click services' and click a backend action.")

with tabs[5]:
    st.subheader("Presentation explanation")
    st.write("""
    My dashboard is a demo of the decision-support layer. It does not replace scientific processing.
    GEE is used for time-series satellite processing, QGIS/PostGIS for spatial connection, SAR tools
    for priority glacier motion, Python for automation and dashboard logic, field forms for local
    observations, and NDMA public advisories/SITREPs for official disaster-management context. Global dashboards such as NASA Worldview, GLIMS, WGMS, GloFAS and Google Flood Hub are added as reference services. The important point is that a policymaker should not receive separate maps, Excel files,
    and field notes. The dashboard joins them into one basin-wise status picture.
    """)
    st.success("Demo slogan: From glacier pixels to basin decisions.")
