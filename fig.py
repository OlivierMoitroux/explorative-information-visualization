import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os
import pandas as pd
import plotly

import plotly.express as px

import numpy as np  # linear algebra


# ====================================================================== #
#                    Hyperparameters of the visualization                #
# ====================================================================== #

REMOVE_FAILED_KILLED_ATTEMPTS = False
REMOVE_UNKNOWN_KILLED = False
REMOVE_FAILED_WOUNDED_ATTEMPTS = False
REMOVE_UNKNOWN_WOUNDED = False
REMOVE_FAILED_CASUALITIES = False # -> influence a LOT the plto !! (cfr. USA VS
#  UK)

pd.set_option('display.max_columns', None)

# ====================================================================== #
#                        List data folders                               #
# ====================================================================== #
# Input data files are available in the "./data/" directory.
print("Listing data folder ...\n")
terrorismDataPath = None

for dirname, _, filenames in os.walk('./data'):
    for filename in filenames:
        print(filename)
        if "terrorism" in filename:
            terrorismDataPath = os.path.join(dirname, filename)


# ====================================================================== #
#                        Importing and cleaning data                     #
# ====================================================================== #

print("Loading Terrorism dataset from {} ...".format(terrorismDataPath))

data= pd.read_csv(terrorismDataPath, encoding='ISO-8859-1')
nRowsOriginal = data['iyear'].count()
print("Terrorism dataset has {} rows\n".format(nRowsOriginal))

# Keep only interesting columns:
data = data[['iyear', 'imonth', 'longitude', 'latitude', 'country_txt', 'region_txt', 'attacktype1_txt', 'nkill', 'nwound', 'gname', 'targtype1_txt', 'weaptype1_txt', 'success', 'summary', 'natlty1_txt', 'nperps', 'motive']]

# Rename columns
data.rename(columns={'iyear':'year','imonth':'month','iday':'day','country_txt':'country','region_txt':'region','attacktype1_txt':'attack_type','nkill':'nkilled','nwound':'nwounded','gname':'group','targtype1_txt':'target_type','weaptype1_txt':'weapon_type', 'longitude':'long', 'latitude':'lat', 'natlty1_txt':'natlty_target'},inplace=True)

# FILTERING
# ---------

# Remove NaN values in nKilled column
data = data[np.isfinite(data['nkilled'])]

if REMOVE_FAILED_KILLED_ATTEMPTS is True:
    data = data[data["nkilled"] > 0]

if REMOVE_FAILED_WOUNDED_ATTEMPTS is True:
    data = data[data["nwounded"] > 0]

if REMOVE_UNKNOWN_KILLED is True:
    data = data[np.isfinite(data['nkilled'])]
else:
    # Change NaN to 0 such that casualities will be a finite number
    data = data.fillna(value={"nkilled":0})

if REMOVE_UNKNOWN_WOUNDED is True:
    data = data[np.isfinite(data['nwounded'])]
else:
    # Change NaN to 0 such that casualities will be a finite number
    data = data.fillna(value={"nwounded": 0})

# Get a true number for casualities by replacing unknown variable with 0

data['casualities']= data['nkilled'] + data['nwounded']

if REMOVE_FAILED_CASUALITIES is True:
    data = data[data["casualities"] > 0]

# data['casualities']=(data['nkilled']and np.isfinite(data['nkilled']))+(data[
#                                                                       'nwounded'] and np.isfinite(data[
#                                                                            'nwounded']))

nRowsAfterFiltering = data["year"].count()
print("After cleaning, terrorism dataset has {} rows. Removed {}\% of "
      "data".format(nRowsAfterFiltering,
                    (nRowsAfterFiltering/nRowsOriginal)*100))

# ====================================================================== #
#                   Preprocessing of dataframe                           #
# ====================================================================== #

raw_data = data.copy()









data=raw_data[raw_data["year"]==2001]
# Frequency for each countries
freq = data
# test = freq.country.value_counts().reset_index()
freq = freq.country.value_counts().reset_index().rename(columns={
    "country":"events", "index": "country"})
# freq = freq.country.value_counts()
print(freq.head(10))


attackTypeFreq = data
attackTypeFreq = data.attack_type.value_counts().astype('int32').reset_index().rename(columns={
    "index":"attack", "attack_type": "freq"})

attackTypeFreq = attackTypeFreq.astype({'freq': 'int32'})

data["hash_attack_type"] = data["attack_type"].apply(hash)
attackTypeFreq["hash_attack_type"] = attackTypeFreq["attack"].apply(hash)

# ====================================================================== #
#                   Building dashboard visualization  (UI)               #
# ====================================================================== #


# Initialize figure with subplots
fig = make_subplots(
    rows=2, cols=3,
    column_widths=[0.6, 0.3, 0.1],
    row_heights=[0.55, 0.45],
    specs=[[{"type": "scattergeo", "rowspan": 2}, {"type": "bar",
                                                   "colspan":2}, None],
           [            None                    , {"type": "domain"}, None]
           ],
)


# Add terrorism events locations on globe map
fig.add_trace(
    go.Scattergeo(lat=data["lat"],
                  lon=data["long"],
                  mode="markers",
                  ids= data["hash_attack_type"],

                hoverinfo='text',
                  text=['<b>Country</b>: {}<br>'.format(cntry)\
                        +'<i>Attack type</i>: {}<br>'.format(atype)
                        +'<i>Casualities</i>: {}<br>'.format(cas)\
                        +'  - <i>Killed</i>: {}<br>'.format(kill)\
                        +'  - <i>Wounded</i>: {}'.format(wounded)\
                        for cntry, atype, cas, kill, wounded in zip(
                          list(data["country"]),
                          list(data["attack_type"]),
                          list(data["casualities"]),
                          list(data["nkilled"]),
                          list(data["nwounded"])
                         )
                        ],

                  showlegend=False,
                  name= "Attack",
                  marker=dict(
                      # colorscale = scl,
                      showscale=True,
                      colorscale="Portland", #"Viridis", "Portland", "YlOrRd", 'RdBu'
                      color=np.log(data['casualities']), # np.log
                      reversescale = False,
                      autocolorscale = False,
                        colorbar=dict(
                                    title={"text": "log(casualities)",
                                           "side":"top"},
                                    x=0.57,
                                    y = 0.55,
                                    xanchor= 'center',
                                    yanchor="middle",
                                    len=0.96
                                ),
                      size=8, # 4
                      opacity=0.8,
                  ),
    ),
    row=1, col=1
)


# Add locations bar chart
fig.add_trace(
    go.Bar(x=freq["country"][0:10],y=freq["events"][0:10], marker=dict(
        color="crimson"), name="Number of attacks", showlegend=False),
    row=1, col=2
)


fig.add_trace(
    go.Pie(
        labels = attackTypeFreq["attack"],
        values = attackTypeFreq["freq"],
        name="Attack type",
        ids= attackTypeFreq["hash_attack_type"],
        showlegend=True,
        hole=.3,
    ),
    row=2, col=2
)

# Update geo subplot properties
fig.update_geos(
    projection_type="orthographic",
    landcolor="lightgrey", # white
    # resolution = 110,
    oceancolor="rgb(6,66,115)",#MidnightBlue
    showocean=True,
    lakecolor="LightBlue",
    showcountries=True,
    showrivers = True,
    rivercolor = '#99c0db'

)

# Rotate x-axis labels
fig.update_xaxes(tickangle=45)


# Set theme, margin, and annotation in layout
fig.update_layout(

updatemenus = [
    {'buttons': [{'args': [[str(i) for i in raw_data["year"].unique()],
                    {'frame': {
                    'duration': 700.0, 'redraw': False}, 'fromcurrent': True,
                    'transition':{'duration': 0, 'easing': 'linear'}}],
                    'label': 'Play', 'method':'animate'},

                 {'args': [[None],
                    {'frame': {'duration': 0, 'redraw': False}, 'mode':
                    'immediate', 'transition': {'duration': 0}}],
                  'label': 'Pause',
                  'method': 'animate'}],
     'direction': 'left', 'pad': {'r': 10, 't': 85}, 'showactive': True, 'type': 'buttons', 'x': 0.1, 'y': 0, 'xanchor': 'right', 'yanchor': 'top',  "font":dict(color="black")}
],

sliders = [{'yanchor': 'top', 'xanchor': 'left', 'currentvalue': {'font': {
    'size': 16}, 'prefix': 'Year: ', 'visible': True, 'xanchor': 'right'},
            'transition': {'duration': 500.0, 'easing': 'linear'}, 'pad': {'b': 10, 't': 50}, 'len': 0.9, 'x': 0.1, 'y': 0,
                    'steps': [{'args': [[str(i)], {'frame': {'duration': 500.0,
                                                        'easing': 'linear',
                                                        'redraw': False},
                                              'transition': {'duration': 0,
                                                             'easing':
                                                                 'linear'}}], 'label': str(i), 'method': 'animate'} for i in raw_data["year"].unique()]
            }],

    # example to use frames:
    # frames=[
    #     {'name': '0', 'layout': {},
    #      'data': [
    #          {'type': 'scattergeo', 'name': 'scattergeo',
    #           'x': [-2., -1., 0.01, 1., 2., 3.], 'y': [5, 8, 3, 2, 4, 0],
    #           'hoverinfo': 'name+text',
    #           'marker': {'opacity': 1.0, 'symbol': 'circle',
    #                      'line': {'width': 0, 'color': 'rgba(50,50,50,0.8)'}},
    #           'line': {'color': 'rgba(255,79,38,1.000000)'},
    #           'mode': 'markers+lines', 'fillcolor': 'rgba(255,79,38,0.600000)',
    #           'legendgroup': 'f1', 'showlegend': True, 'xaxis': 'x1',
    #           'yaxis': 'y1'},
    #          {'type': 'scatter', 'name': 'f2',
    #           'x': [-2., -1., 0.01, 1., 2., 3.], 'y': [3, 7, 4, 8, 5, 9],
    #           'hoverinfo': 'name+text',
    #           'marker': {'opacity': 1.0, 'symbol': 'circle',
    #                      'line': {'width': 0, 'color': 'rgba(50,50,50,0.8)'}},
    #           'line': {'color': 'rgba(79,102,165,1.000000)'},
    #           'mode': 'markers+lines',
    #           'fillcolor': 'rgba(79,102,165,0.600000)', 'legendgroup': 'f2',
    #           'showlegend': True, 'xaxis': 'x2', 'yaxis': 'y2'}],
    #      },],


    template="plotly_dark",
    margin=dict(r=10, t=80, b=40, l=10),
    legend_orientation="v",
    legend=dict(x=0.85, y=.05),
    annotations=[
        go.layout.Annotation(
            text="Source: Global Terrorism Database (GTD - Kaggle)",
            showarrow=False,
            xref="paper",
            yref="paper",
            x=0,
            y=-0.05),

        go.layout.Annotation(
            text="<b>Total: </b>{} attacks".format(attackTypeFreq[
                                                      "freq"].sum()),
            showarrow=False,
            font= {"size": 18},
            xref="paper",
            yref="paper",
            x=1.009, #.75 .95 if no attack in name
            y=0), # .18


        go.layout.Annotation(
                    xref= 'paper',
                    showarrow=False,
                    x= 0.82,
                    y = 1.025,
                    font= {"size": 15},
                    xanchor= 'center',
            yref="paper",
                    yanchor="top",
                    text= '<b>Top 10 countries with highest number of '
                          'attacks</b>'
            # https://codepen.io/mdnasirfardoush/pen/gjovjO?editors=1010
                ),
    ],
    title= {
      "text": 'Evolution of worldwide terrorism across time',
      "xanchor": 'center',
      "yanchor": 'middle',
      "x": 0.5,
      "y": 0.95,
      "xref": 'paper',
      "yref": 'container',
      "font": {"size": 30}
    },
)

# fig.show()
plotly.offline.plot(fig, filename='output/index.html')