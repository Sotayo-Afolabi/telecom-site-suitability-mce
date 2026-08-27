<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/bb055be0-37f4-46f3-8716-2235664b1c85" /># Telecom Tower Site Suitability Analysis (Spatial MCE & AHP)

![License](https://img.shields.io/badge/License-MIT-blue.svg)
![GIS Platform](https://img.shields.io/badge/GIS-QGIS%203.28+-green.svg)
![Status](https://img.shields.io/badge/Status-Phase%201%20Complete-brightgreen.svg)

A spatial Multi-Criteria Decision Analysis (MCDA) framework designed to identify optimal candidate sites for 4G/5G telecommunications infrastructure across **Ogun State, Nigeria**. 

This project balances network growth goals against terrain topography and site access by combining vector spatial analysis, Analytic Hierarchy Process (AHP) weighting, and weighted raster overlays.

---

## 📌 Executive Summary

Expanding telecommunications infrastructure requires significant capital expenditure (CapEx). Placing towers in low-demand areas or challenging terrain leads to inflated operational costs and low coverage yield. 

This model synthesizes **5 key spatial variables** into a standardized suitability index. Using Saaty’s Analytic Hierarchy Process (AHP), criteria weights were evaluated to prioritize coverage gaps while maintaining engineering accessibility. The decision model achieved a **Consistency Ratio (CR) of 1.3%**, confirming logical mathematical consistency.

---

## 🗺️ Project Architecture & Workflow

```text
┌─────────────────────────┐
│   Raw Spatial Layers    │ (DEM, Roads, Land Use, Cell Towers, Water)
└────────────┬────────────┘
             │
             ▼
┌─────────────────────────┐
│ Vector & Spatial Analysis│ 3 km Tower Buffer → Land Use Erase (Dead Zone Extraction)
└────────────┬────────────┘
             │
             ▼
┌─────────────────────────┐
│ Raster Standardization  │ 30m Resampling & 1–5 Scale Reclassification
└────────────┬────────────┘
             │
             ▼
┌─────────────────────────┐
│   AHP Matrix Weighting  │ Pairwise Evaluation & Consistency Validation (CR = 1.3%)
└────────────┬────────────┘
             │
             ▼
┌─────────────────────────┐
│ Weighted Overlay & Map  │ QGIS WLC Raster Math & Cartographic Layout Export
└─────────────────────────┘
```
## 📊 Criteria Selection & Reclassification Scheme

All datasets were processed at a **30-meter spatial resolution** and reclassified onto a uniform **1 to 5 suitability scale** (1 = Least Suitable, 5 = Most Suitable):

| Criterion | Source Layer | GIS Derivation Logic | Reclassification (1–5 Scale) |
| :--- | :--- | :--- | :--- |
| **Telecom Dead Zones** | Tower Points & Settlement Polygons | 3 km buffer erased from inhabited land use areas to extract unserved populations | Unserved areas assigned Highest Priority (5) |
| **Road Network** | OpenStreetMap Vector | Euclidean Distance calculation (Proximity analysis) | Near roads = 5 (Low CapEx); Remote = 1 |
| **Elevation** | SRTM Digital Elevation Model (DEM) | Altitude above sea level (Meters) | Moderate-high elevations favored (Coverage range) |
| **Slope** | Derived DEM Terrain | Slope calculation in degrees | Flat/gentle terrain = 5; Steep slopes (>15°) = 1 |
| **Water Bodies** | Hydrographic Layer | Proximity buffering around rivers/drainage | Buffer zones outside flood zones = 5; Water = 1 |





## 🧮 Mathematical Framework (AHP & Consistency Check)

Criteria priority weights were calculated using Saaty’s pairwise evaluation scale:

### 1. Pairwise Comparison Matrix

| Spatial Criterion | Telecom Dead Zones | Road Access | Elevation | Slope | Water Distance |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Telecom Dead Zones** | 1.00 | 3.00 | 3.00 | 5.00 | 5.00 |
| **Road Access** | 0.33 | 1.00 | 2.00 | 3.00 | 3.00 |
| **Elevation** | 0.33 | 0.50 | 1.00 | 2.00 | 3.00 |
| **Slope** | 0.20 | 0.33 | 0.50 | 1.00 | 1.00 |
| **Water Distance** | 0.20 | 0.33 | 0.33 | 1.00 | 1.00 |

### 2. Derived Criteria Weights
* **Telecom Dead Zones:** `42.0%` (`0.42`)
* **Road Proximity:** `26.0%` (`0.26`)
* **Elevation:** `16.0%` (`0.16`)
* **Slope:** `8.0%` (`0.08`)
* **Water Distance:** `8.0%` (`0.08`)

### 3. Model Consistency Validation
* **Principal Eigenvalue ($\lambda_{\max}$):** `5.060`
* **Consistency Index (CI):** `0.015`
* **Consistency Ratio (CR):** **`1.3%`** *(Passed: $\text{CR} \le 10\%$ confirms model validity)*



## 🖼️ Deliverables & Visual Results

### Reclassified Input Criteria
*(Standardized 1–5 suitability maps for all five spatial variables)*

* **Telecom Dead Zones:** `maps/OGUN STATE TELECOME DEADZONES.png`
* **Road Proximity:** `maps/Ogun state Road network reclassified.png`
* **Elevation:** `maps/Ogun state ELEVATION RECLASSIFIED.png`
* **Slope:** `maps/Ogun state slope reclassification.png`
* **Water Distance:** `maps/Ogun state RIVER DISTANCE CLASSIFICATION.png`
* **Dead Zone Land Use:** `maps/Ogun state land use telecom deadzone calssification.png`

*(Composite thumbnail grid `input_rasters_grid.png` coming soon)*

### Final Composite Suitability Model
The weighted linear combination was executed via QGIS Raster Calculator:

$$\text{Suitability} = (R_{\text{deadzone}} \times 0.42) + (R_{\text{road}} \times 0.26) + (R_{\text{elevation}} \times 0.16) + (R_{\text{slope}} \times 0.08) + (R_{\text{water}} \times 0.08)$$

![Ogun State Final Suitability Map](<maps/Ogun state Telecom Suitability Map.png>)


---


```text
## 📁 Repository Structure

```text
telecom-site-suitability-mce/
├── README.md                                       <-- Main Project Overview & Report
├── docs/
│   └── Telecom_Suitability_CaseStudy_Sotayo.pdf        <-- Downloadable Executive PDF
├── maps/
│   ├── Ogun state Telecom Suitability Map.png       <-- Final composite suitability map
│   ├── OGUN STATE TELECOME DEADZONES.png            <-- Reclassified deadzone layer
│   ├── Ogun state Road network reclassified.png     <-- Reclassified road proximity
│   ├── Ogun state ELEVATION RECLASSIFIED.png        <-- Reclassified elevation layer
│   ├── Ogun state slope reclassification.png        <-- Reclassified slope layer
│   ├── Ogun state RIVER DISTANCE CLASSIFICATION.png <-- Reclassified river buffer
│   └── Ogun state land use telecom deadzone...png   <-- Land use overlay classification
└── data/
    └── README.md                                   <-- Metadata specs, CRS info, sources

```

## 🚀 Project Roadmap & Automation Plan

- [x] **Phase 1 (GIS GUI):** Vector gap extraction, AHP matrix derivation ($\text{CR} = 1.3\%$), QGIS WLC overlay calculation, and executive PDF case study layout.
- [ ] **Phase 2 (Python Automation):** Refactoring the manual overlay into an automated Python pipeline using `Rasterio`, `GeoPandas`, and `NumPy` for batch execution.

---

## 📄 License & Contact

Distributed under the MIT License. See `LICENSE` for details.

**Author:** Sodiq Afolabi Sotayo  
**Role:** GIS Analyst & Spatial Data Engineer  
**GitHub:** [github.com/Sotayo-Afolabi](https://github.com/Sotayo-Afolabi)
