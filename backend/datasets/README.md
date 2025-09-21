# Datasets Included in this Project

Sources and the datasets from them:
- **Western Pennsylvania Regional Data Center**
    - `Pittsburgh_City_Facilities.csv` (https://data.wprdc.org/dataset/city-of-pittsburgh-facilities/resource/fbb50b02-2879-47cd-abea-ae697ec05170)
    - `Pittsburgh_Neighborhoods.csv` (https://data.wprdc.org/dataset/neighborhoods2/resource/668d7238-cfd2-492e-b397-51a6e74182ff)
    - `wprdc_arrestdata_pittsburgh_apr2025.csv` sourced from [Western Pennsylvania Regional Data Center](https://data.wprdc.org/dataset/arrest-data/resource/e03a89dd-134a-4ee8-a2bd-62c40aeebc6f)
- **Western Pennsylvania Regional Data Center Parcels N'at** (https://parcelsnat.org/bulk)
    - `property-assessments-1.csv`
    - `property-assessments-2.csv`
    - `property-assessments-3.csv`
    - `property-assessments-4.csv`

Zip Code Centroid coordinates for proximity calculations: https://hudgis-hud.opendata.arcgis.com/datasets/zip-code-population-weighted-centroids-1/

Output Data:
- `output_categorized_data.pkl` - Clustered / Categorized main data
- `property-assessments-combined.csv` - Combined data for ALL parcel data in Pittsburgh