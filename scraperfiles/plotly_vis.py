import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import pickle
import json

with open(f'city_subreddits.json', 'r') as f:
    cities_json = json.load(f)

# for i in cities_json["City List"]:
#     print(cities_json["City List"][i]['lat'])

# df = pd.DataFrame.from_dict(cities_json['City List'],orient='index').reset_index()
#
# df.rename({'index': 'city'}, axis=1, inplace=True)
# #print(df)
# fig = px.scatter_mapbox(df, lat="lat", lon="lon", hover_name="city", #hover_data=["State", "Population"],
#                         color_discrete_sequence=["fuchsia"], zoom=3, height=300)
# fig.update_layout(mapbox_style="open-street-map")
# fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
# fig.show()

with open('test1_data.pickle', 'rb') as f:
    x = pickle.load(f)

limits = [(0,2),(3,10),(11,20),(21,50),(50,3000)]
colors = ["royalblue","crimson","lightseagreen","orange","lightgrey"]
cities = []
scale = 5000

fig = go.Figure()

for i in range(len(limits)):
    lim = limits[i]
    df_sub = df[lim[0]:lim[1]]
    fig.add_trace(go.Scattergeo(
        locationmode = 'USA-states',
        lon = df_sub['lon'],
        lat = df_sub['lat'],
        text = df_sub['text'],
        marker = dict(
            size = df_sub['pop']/scale,
            color = colors[i],
            line_color='rgb(40,40,40)',
            line_width=0.5,
            sizemode = 'area'
        ),
        name = '{0} - {1}'.format(lim[0],lim[1])))

fig.update_layout(
        title_text = '2014 US city populations<br>(Click legend to toggle traces)',
        showlegend = True,
        geo = dict(
            scope = 'usa',
            landcolor = 'rgb(217, 217, 217)',
        )
    )

fig.show()

