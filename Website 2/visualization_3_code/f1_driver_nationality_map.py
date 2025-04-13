import pandas as pd
import plotly.graph_objects as go
import geopandas as gpd

# loading data
# F1 data:
df_drivers = pd.read_csv("drivers.csv")
df_results = pd.read_csv("results.csv")
df_race = pd.read_csv("races.csv")

# nationality data
# source: https://github.com/knowitall/chunkedextractor/blob/master/src/main/resources/edu/knowitall/chunkedextractor/demonyms.csv
df_nat = pd.read_csv("demonyms.csv")
df_nat.columns = ["nationality", "country"]

# world data
world = gpd.read_file("ne_110m_admin_0_countries.shp").to_crs(4326)
world["country"] = world["SOVEREIGNT"]
world = world[world["country"] != "Greenland"]

# merging F1 data
df = pd.merge(df_drivers, df_results, how="inner", on="driverId")
df = pd.merge(df, df_race, how="left", on="raceId")
df["date"] = pd.to_datetime(df["date"], format="%Y-%m-%d")
df["year"] = df["date"].dt.year
df = df[["driverId", "nationality", "year"]]
df = df.drop_duplicates()
df = pd.merge(df, df_nat, how="left", on="nationality")
df.dropna(inplace=True)

# getting amount of drivers in each country by year
df_group = df.groupby(["country", "year"], as_index=False).agg("count")


def create_f1_map(year):
    """
    creates an F1 map for a given year
    params:
        year: int: the chosen year
    returns:
        merged_df: DataFrame: the world map merged with data from that year
    """
    # filtering the data for the year
    year_df = df_group[df_group["year"] == year]

    # merging data with geospatial data
    merged_df = pd.merge(world, year_df, how="left", on="country")
    merged_df["driverId"] = merged_df["driverId"].fillna(0)  # Fill NaN with 0 drivers

    return merged_df

# create an animation of maps, where each frame is each year of F1
# citation: https://plotly.com/python/animations/
frames = []
# iterating through all available years
years = sorted(df["year"].unique())
for year in years:
    merged_df = create_f1_map(year)
    
    # create the map for the given year
    frame = go.Choropleth(
        locations=merged_df["country"],
        locationmode="country names",
        z=merged_df["driverId"],
        hoverinfo="location+z",
        colorscale="Reds",
        colorbar_title="",
        #colorbar_x =-1,
        
        colorbar = dict(
            len=1,
            y=0.5,
            x=.1),
        zmin = 0,
        zmax = 25
    )
    
    frames.append(go.Frame(
        data=[frame],
        name=str(year)
    ))

# creating initial map
initial_map = create_f1_map(years[0])
initial_map_fig = go.Figure(
    data=[go.Choropleth(
        locations=initial_map["country"],
        locationmode="country names",
        z=initial_map["driverId"],
        hoverinfo="location+z",
        colorscale="Reds",
        colorbar_title="",
        colorbar = dict(
            len=1,
            y=0.5,
            x=0.1),
        zmin = 0,
        zmax = 25
    )],
    layout=go.Layout(
        geo=dict(
            showcoastlines=True,
            projection_type="equirectangular",
        ),
        autosize=True,
        height=700,
        margin=dict(l=0, r=0, t=0, b=0),
        sliders=[{
            "active": 0,
            "currentvalue": {
                "font": {"size": 20},
                "visible": True,
                "prefix": "Year: ",
                "offset": 50
                
            },
            "tickcolor": "white",
            "steps": [
                {
                    "args": [
                        [str(year)],
                        {"frame": {"duration": 300, "redraw": True}, 
                         "mode": "immediate", 
                         "transition": {"duration": 300},
                         "visible":False},
                    ],
                    "label": str(year),
                    "method": "animate",
                }
                for year in years
            ],
            
        }],
    ),
    frames=frames,
)

# adding a plotly slider to filter by year
# citation: https://plotly.com/python/sliders/
initial_map_fig.update_layout(
    geo=dict(
        showcoastlines=True,
        projection_type="equirectangular",
    ),
    dragmode=False,
    autosize=True,
    height=700,
    margin=dict(l=0, r=0, t=0, b=0),
    sliders=[{
        "currentvalue": {
            "font": {"size": 20},
            "visible": True,
            "prefix": "Year: ",
        },
        "steps": [
            {
                "args": [
                    [str(year)],
                    {"frame": {"duration": 300, "redraw": True}, "mode": "immediate", "transition": {"duration": 300}},
                ],
                "method": "animate",
            }
            for year in years
        ],
    }]
)



# writing html file
initial_map_fig.write_html("f1_driver_nationality_map.html", auto_play=False)