import pandas as pd
import plotly.express as px
import json

with open(f'city_subreddits.json', 'r') as f:
    cities_json = json.load(f)

# for i in cities_json["City List"]:
#     print(cities_json["City List"][i]['lat'])

df = pd.DataFrame.from_dict(cities_json['City List'],orient='index').reset_index()

df.rename({'index': 'city'}, axis=1, inplace=True)
#print(df)
fig = px.scatter_mapbox(df, lat="lat", lon="lon", hover_name="city", #hover_data=["State", "Population"],
                        color_discrete_sequence=["fuchsia"], zoom=3, height=300)
fig.update_layout(mapbox_style="open-street-map")
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
fig.show()

