# Data Sources & Metadata Specifications

This directory contains metadata, spatial reference specifications, and processing parameters for the spatial datasets used in the **Telecom Site Suitability Analysis across Ogun State, Nigeria**.

To maintain repository optimization and prevent storage clutter, heavy raw spatial datasets (`.tif`, `.shp`) are not hosted directly in this repository. All source data used in this study are publicly accessible or derived using the methodologies detailed below.

---

## 🌐 Spatial Reference System (CRS)

All spatial datasets were projected and aligned to the local projected coordinate system prior to raster overlay modeling:

* **Geographic Coordinate System (GCS):** `GCS_WGS_1984` (EPSG:4326)
* **Projected Coordinate System (PCS):** `Minna / UTM Zone 31N` (EPSG:26331)
* **Processing Resolution:** **30m x 30m** cell size (Resampled via Nearest Neighbor for discrete layers, Bilinear Interpolation for continuous rasters).
* **Study Area Bounding Box:** Ogun State, Nigeria administrative boundary.

---

## 📊 Dataset Inventory & Sources

| Dataset Layer | Data Type | Primary Source | Spatial Resolution / Scale | Description & Derived Processing |
| :--- | :---: | :--- | :--- | :--- |
| **Existing Cell Towers** | Vector Point | OpenCelliD / Industry Point Data | Point geometry | Used to calculate a **3 km buffer coverage radius** identifying served operational zones. |
| **Land Use / Settlements** | Vector Polygon | Geofabrik OpenStreetMap Extracts | 1:50,000 | Settled and inhabited land use zones extracted and erased against existing tower coverage to derive **Unserved Telecom Dead Zones**. |
| **Road Network** | Vector Line | Geofabrik OpenStreetMap Extracts | Line geometry | Primary and secondary road vectors used for **Euclidean Distance proximity modeling** to minimize network extension CapEx. |
| **Digital Elevation Model (DEM)** | Raster Grid | USGS EarthExplorer (SRTM DEM) | 30-meter pixel | Elevation surface utilized directly to model signal propagation terrain advantages. |
| **Terrain Slope** | Raster Grid | Derived from SRTM DEM | 30-meter pixel | Calculated surface incline (in degrees) using QGIS Slope Tool to evaluate construction viability and landslide risks. |
| **Hydrographic Network** | Vector Line / Polygon | Geofabrik OpenStreetMap Extracts / HydroSHEDS | 1:100,000 | Rivers, lakes, and major drainage channels buffered to create exclusion/flood-risk safety zones. |

---

## 🛠️ Data Preprocessing & Reclassification Pipeline

1. **Reprojection:** All raw vector and raster layers were transformed into `EPSG:26331 (Minna / UTM Zone 31N)` to ensure accurate metric spatial distance calculations.
2. **Clipping:** Layers were clipped to the official Ogun State administrative boundary mask.
3. **Rasterization & Resampling:** Vector distance surfaces were rasterized and matched to the 30m grid alignment of the SRTM DEM.
4. **Scale Standardization:** All layers were reclassified using QGIS Reclassify by Table into a standardized ordinal scale of **1 to 5** (where 1 = Least Suitable, 5 = Most Suitable).

---

## 📖 External Data Access Links

If you wish to replicate this analysis, the raw datasets can be downloaded directly from the following providers:

* **Land Use, Roads & Hydrography Vectors:** [Geofabrik OpenStreetMap Extracts (Nigeria)](https://download.geofabrik.de/africa/nigeria.html)
* **SRTM Digital Elevation Data:** [USGS EarthExplorer](https://earthexplorer.usgs.gov/)
* **Global Open Cell Towers:** [OpenCelliD Database](https://opencellid.org/)
