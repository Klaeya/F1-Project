import folium
import geopandas as gpd
import numpy as np
import branca
import pandas as pd
import datetime
from shapely.geometry import Point

# creating data + geometry
circuits_df = pd.read_csv("circuits.csv")
race_df = pd.read_csv("races.csv")
race_df["date"] = pd.to_datetime(race_df["date"])
race_df["year"] = race_df["date"].dt.year


race_group = race_df.groupby("circuitId")["year"].agg(["count", "min"]).reset_index()


circuits_df = pd.merge(circuits_df, race_group, on="circuitId")
circuits_df["races"] = circuits_df["count"]
circuits_df["year"] = circuits_df["min"]

geometry = gpd.points_from_xy(circuits_df["lng"], circuits_df["lat"])
circuits_gdf = gpd.GeoDataFrame(circuits_df, geometry=geometry, crs="EPSG:4326")


# Calculate map center
center = circuits_gdf.geometry.centroid
avg_lat = center.y.mean()
avg_lon = center.x.mean()

# Create folium map
m = folium.Map(location=[avg_lat, avg_lon], zoom_start=3, tiles = None)

circuits_json = circuits_gdf.to_json()

# citation: https://stackoverflow.com/questions/73412210/how-to-make-folium-features-geojson-plot-circles-instead-of-icons
folium.GeoJson(
                marker=folium.Circle(
                    radius=10000,
                   fill_color="#FF1E00",
                   fill_opacity=0.8,
                   color="black",
                   weight=1.2),
    data=circuits_json,
    name="F1 Circuits",
    tooltip=folium.GeoJsonTooltip(fields=["name", "location", "country", "races", "year"], 
                                  aliases=["Name", "Location", "Country", "Total Races Held", "First Year"])
).add_to(m)


folium.TileLayer("CartoDB positron", show=True).add_to(m) 


folium.LayerControl().add_to(m)

m.save("circuit_map.html")
