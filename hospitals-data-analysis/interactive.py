import sqlite3
from urllib.request import urlopen
import json
import pandas as pd
import plotly.express as px

connection = sqlite3.connect('../hospital_data.db')

#  Query counts clinical trials per region by joining the `hospitals` and `trial_data` tables on their
#  respective ID fields. It then groups the results by the `region` field from the `hospitals` table to provide the
#  total number of trials for each `region`.
query = """
SELECT h.region, COUNT(td.trial_code) AS trial_count
FROM hospitals AS h
JOIN trial_data AS td ON h.hospital_card_id = td.hospital_id
GROUP BY h.region;
"""

# Run query thru Pandas and converting result into dataframe type
df_trials = pd.read_sql_query(query, connection)
connection.close()

# Spain Regions Geojson data (well-known as CCAA)
with urlopen('https://github.com/R-CoderDotCom/data/blob/main/shapefile_spain/spain.geojson?raw=true') as response:
    ccaa = json.load(response)

# Create a dictionary for mapping regions to ccaa_id
df_regions = pd.DataFrame({
    "ccaa_id": ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12", "13", "14", "15", "16", "17", "18"],
    "name": ["Andalucía", "Aragón", "Principado de Asturias", "Islas Baleares", "Islas Canarias",
             "Cantabria", "Castilla y León", "Castilla-La Mancha", "Cataluña", "Comunidad Valenciana",
             "Extremadura", "Galicia", "Comunidad de Madrid", "Región de Murcia", "Comunidad Foral de Navarra",
             "País Vasco", "La Rioja", "Ceuta y Melilla"]
})

region_to_id = df_regions.set_index('name')['ccaa_id'].to_dict()

# Handle special cases in region names
region_to_id["Asturias"] = region_to_id["Principado de Asturias"]
region_to_id["Baleares"] = region_to_id["Islas Baleares"]
region_to_id["Canarias"] = region_to_id["Islas Canarias"]
region_to_id["Castilla - La Mancha"] = region_to_id["Castilla-La Mancha"]
region_to_id["Comunitat Valenciana"] = region_to_id["Comunidad Valenciana"]
region_to_id["Comunidad de Madrid"] = region_to_id["Comunidad de Madrid"]
region_to_id["Murcia"] = region_to_id["Región de Murcia"]
region_to_id["Navarra"] = region_to_id["Comunidad Foral de Navarra"]
region_to_id["Ceuta"] = region_to_id["Ceuta y Melilla"]  # Assuming Ceuta and Melilla have the same id for simplification
region_to_id["Melilla"] = region_to_id["Ceuta y Melilla"]

# Map the regions to their corresponding ccaa_id
df_trials['ccaa_id'] = df_trials['region'].map(region_to_id)

fig = px.choropleth_mapbox(
    data_frame=df_trials,
    geojson=ccaa,
    featureidkey='properties.ccaa_id',
    locations='ccaa_id',
    color='trial_count',
    color_continuous_scale='viridis',
    opacity=0.5,
    hover_name='region',
    mapbox_style='open-street-map',
    center=dict(lat=40.0, lon=-3.72),
    zoom=4)

fig.show()
