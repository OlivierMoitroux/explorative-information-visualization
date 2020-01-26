import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os
import pandas as pd
import plotly

import plotly.express as px

import numpy as np  # linear algebra
# https://plot.ly/python/v3/mixed-subplots/
# ====================================================================== #
#                     Documentation                                      #
# ====================================================================== #
# Timer:
# https://community.plot.ly/t/multiple-plots-running-on-frames/8235/6
# https://plot.ly/~empet/15012/animating-subplots-with-more-than-one-t/#/
# https://community.plot.ly/t/multiple-traces-in-multiple-animation-plots/15019
# https://plot.ly/python/animations/
# # https://plot.ly/python/range-slider/
#https://plot.ly/~harry11733/105/#code


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

for dirname, _, filenames in os.walk('../data'):
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
#                   Personalization                                      #
# ====================================================================== #

myColorScale=[
        # Let first 10% (0.1) of the values have color rgb(0, 0, 0)
        [0, "rgb(0, 0, 0)"],
        [0.1, "rgb(0, 0, 0)"],

        # Let values between 10-20% of the min and max of z
        # have color rgb(20, 20, 20)
        [0.1, "rgb(20, 20, 20)"],
        [0.2, "rgb(20, 20, 20)"],

        # Values between 20-30% of the min and max of z
        # have color rgb(40, 40, 40)
        [0.2, "rgb(40, 40, 40)"],
        [0.3, "rgb(40, 40, 40)"],

        [0.3, "rgb(60, 60, 60)"],
        [0.4, "rgb(60, 60, 60)"],

        [0.4, "rgb(80, 80, 80)"],
        [0.5, "rgb(80, 80, 80)"],

        [0.5, "rgb(100, 100, 100)"],
        [0.6, "rgb(100, 100, 100)"],

        [0.6, "rgb(120, 120, 120)"],
        [0.7, "rgb(120, 120, 120)"],

        [0.7, "rgb(140, 140, 140)"],
        [0.8, "rgb(140, 140, 140)"],

        [0.8, "rgb(160, 160, 160)"],
        [0.9, "rgb(160, 160, 160)"],

        [0.9, "rgb(180, 180, 180)"],
        [1.0, "rgb(180, 180, 180)"]
    ]
myColorBar=dict(
        tick0=0,
        dtick=1
    )


# Scale color
myColorScale2 = [ [0,"rgb(5, 10, 172)"],[0.35,"rgb(40, 60, 190)"],[0.5,
"rgb(70, 100, 245)"],[0.6,"rgb(90, 120, 245)"],[0.7,"rgb(106, 137, 247)"],[1,"rgb(220, 220, 220)"] ]


# ====================================================================== #
#                   Preprocessing of dataframe                           #
# ====================================================================== #

raw_data = data.copy()
# data = data[0:1000]
data = raw_data[raw_data["year"]==2001]

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
fig = dict(
    layout = dict(
        xaxis1 = {'domain': [0.0, 0.44], 'anchor': 'y1', 'title': '1', 'range': [-2.25, 3.25]},
        yaxis1 = {'domain': [0.0, 1.0], 'anchor': 'x1', 'title': 'y', 'range': [-1, 11]},
        xaxis2 = {'domain': [0.56, 1.0], 'anchor': 'y2', 'title': '2', 'range': [-2.25, 3.25]},
        yaxis2 = {'domain': [0.0, 1.0], 'anchor': 'x2', 'title': 'y', 'range': [-1, 11]},
        title  = '',
        margin = {'t': 50, 'b': 50, 'l': 50, 'r': 50},
        updatemenus = [{'buttons': [{'args': [['0', '1', '2', '3'], {'frame': {'duration': 500.0, 'redraw': False}, 'fromcurrent': True, 'transition': {'duration': 0, 'easing': 'linear'}}], 'label': 'Play', 'method': 'animate'}, {'args': [[None], {'frame': {'duration': 0, 'redraw': False}, 'mode': 'immediate', 'transition': {'duration': 0}}], 'label': 'Pause', 'method': 'animate'}], 'direction': 'left', 'pad': {'r': 10, 't': 85}, 'showactive': True, 'type': 'buttons', 'x': 0.1, 'y': 0, 'xanchor': 'right', 'yanchor': 'top'}],
        sliders = [{'yanchor': 'top', 'xanchor': 'left', 'currentvalue': {
            'font': {'size': 16}, 'prefix': 'Year: ', 'visible': True,
            'xanchor': 'right'}, 'transition': {'duration': 500.0, 'easing': 'linear'}, 'pad': {'b': 10, 't': 50}, 'len': 0.9, 'x': 0.1, 'y': 0,
                    'steps': [{'args': [['0'], {'frame': {'duration': 500.0, 'easing': 'linear', 'redraw': False}, 'transition': {'duration': 0, 'easing': 'linear'}}], 'label': '0', 'method': 'animate'},
                              {'args': [['1'], {'frame': {'duration': 500.0, 'easing': 'linear', 'redraw': False}, 'transition': {'duration': 0, 'easing': 'linear'}}], 'label': '1', 'method': 'animate'},
                              {'args': [['2'], {'frame': {'duration': 500.0, 'easing': 'linear', 'redraw': False}, 'transition': {'duration': 0, 'easing': 'linear'}}], 'label': '2', 'method': 'animate'},
                              {'args': [['3'], {'frame': {'duration': 500.0, 'easing': 'linear', 'redraw': False}, 'transition': {'duration': 0, 'easing': 'linear'}}], 'label': '3', 'method': 'animate'},
                    ]}]
    ),

    data = [
        {'type': 'scatter', 'name': 'f1', 'x': [-2.  , -1.  ,  0.01,  1.  ,  2.  ,  3.  ], 'y': [  4,   1,   1, 1,   4,   9], 'hoverinfo': 'name+text', 'marker': {'opacity': 1.0, 'symbol': 'circle', 'line': {'width': 0, 'color': 'rgba(50,50,50,0.8)'}}, 'line': {'color': 'rgba(255,79,38,1.000000)'}, 'mode': 'markers+lines', 'fillcolor': 'rgba(255,79,38,0.600000)', 'legendgroup': 'f1', 'showlegend': True, 'xaxis': 'x1', 'yaxis': 'y1'},
        {'type': 'scatter', 'name': 'f2', 'x': [-2.  , -1.  ,  0.01,  1.  ,  2.  ,  3.  ], 'y': [  2.5,   1,   1, 1,   2.5,   1], 'hoverinfo': 'name+text', 'marker': {'opacity': 1.0, 'symbol': 'circle', 'line': {'width': 0, 'color': 'rgba(50,50,50,0.8)'}}, 'line': {'color': 'rgba(79,102,165,1.000000)'}, 'mode': 'markers+lines', 'fillcolor': 'rgba(79,102,165,0.600000)', 'legendgroup': 'f2', 'showlegend': True, 'xaxis': 'x2', 'yaxis': 'y2'},
    ],

    frames = [
        {'name' : '0', 'layout' : {},
         'data': [
             {'type': 'scatter', 'name': 'f1', 'x': [-2.  , -1.  ,  0.01,  1.  ,  2.  ,  3.  ], 'y': [  5,   8,   3, 2,   4,   0], 'hoverinfo': 'name+text', 'marker': {'opacity': 1.0, 'symbol': 'circle', 'line': {'width': 0, 'color': 'rgba(50,50,50,0.8)'}}, 'line': {'color': 'rgba(255,79,38,1.000000)'}, 'mode': 'markers+lines', 'fillcolor': 'rgba(255,79,38,0.600000)', 'legendgroup': 'f1', 'showlegend': True, 'xaxis': 'x1', 'yaxis': 'y1'},
             {'type': 'scatter', 'name': 'f2', 'x': [-2.  , -1.  ,  0.01,  1.  ,  2.  ,  3.  ], 'y': [  3,   7,   4, 8,   5,   9], 'hoverinfo': 'name+text', 'marker': {'opacity': 1.0, 'symbol': 'circle', 'line': {'width': 0, 'color': 'rgba(50,50,50,0.8)'}}, 'line': {'color': 'rgba(79,102,165,1.000000)'}, 'mode': 'markers+lines', 'fillcolor': 'rgba(79,102,165,0.600000)', 'legendgroup': 'f2', 'showlegend': True, 'xaxis': 'x2', 'yaxis': 'y2'}],
        },

        {'name' : '1', 'layout' : {},
         'data': [
             {'type': 'scatter', 'name': 'f1', 'x': [-2.  , -1.  ,  0.01,  1.  ,  2.  ,  3.  ], 'y': [  4,   1,   1, 1,   4,   9], 'hoverinfo': 'name+text', 'marker': {'opacity': 1.0, 'symbol': 'circle', 'line': {'width': 0, 'color': 'rgba(50,50,50,0.8)'}}, 'line': {'color': 'rgba(255,79,38,1.000000)'}, 'mode': 'markers+lines', 'fillcolor': 'rgba(255,79,38,0.600000)', 'legendgroup': 'f1', 'showlegend': True, 'xaxis': 'x1', 'yaxis': 'y1'},
             {'type': 'scatter', 'name': 'f2', 'x': [-2.  , -1.  ,  0.01,  1.  ,  2.  ,  3.  ], 'y': [  2.5,   1,   1, 1,   2.5,   1], 'hoverinfo': 'name+text', 'marker': {'opacity': 1.0, 'symbol': 'circle', 'line': {'width': 0, 'color': 'rgba(50,50,50,0.8)'}}, 'line': {'color': 'rgba(79,102,165,1.000000)'}, 'mode': 'markers+lines', 'fillcolor': 'rgba(79,102,165,0.600000)', 'legendgroup': 'f2', 'showlegend': True, 'xaxis': 'x2', 'yaxis': 'y2'}],
        },

        {'name' : '2', 'layout' : {},
         'data': [
             {'type': 'scatter', 'name': 'f1', 'x': [-2.  , -1.  ,  0.01,  1.  ,  2.  ,  3.  ], 'y': [  5,   8,   3, 2,   4,   0], 'hoverinfo': 'name+text', 'marker': {'opacity': 1.0, 'symbol': 'circle', 'line': {'width': 0, 'color': 'rgba(50,50,50,0.8)'}}, 'line': {'color': 'rgba(255,79,38,1.000000)'}, 'mode': 'markers+lines', 'fillcolor': 'rgba(255,79,38,0.600000)', 'legendgroup': 'f1', 'showlegend': True, 'xaxis': 'x1', 'yaxis': 'y1'},
             {'type': 'scatter', 'name': 'f2', 'x': [-2.  , -1.  ,  0.01,  1.  ,  2.  ,  3.  ], 'y': [  3,   7,   4, 8,   5,   9], 'hoverinfo': 'name+text', 'marker': {'opacity': 1.0, 'symbol': 'circle', 'line': {'width': 0, 'color': 'rgba(50,50,50,0.8)'}}, 'line': {'color': 'rgba(79,102,165,1.000000)'}, 'mode': 'markers+lines', 'fillcolor': 'rgba(79,102,165,0.600000)', 'legendgroup': 'f2', 'showlegend': True, 'xaxis': 'x2', 'yaxis': 'y2'}],
        },

        {'name' : '3', 'layout' : {},
         'data': [
             {'type': 'scatter', 'name': 'f1', 'x': [-2.  , -1.  ,  0.01,  1.  ,  2.  ,  3.  ], 'y': [  4,   1,   1, 1,   4,   9], 'hoverinfo': 'name+text', 'marker': {'opacity': 1.0, 'symbol': 'circle', 'line': {'width': 0, 'color': 'rgba(50,50,50,0.8)'}}, 'line': {'color': 'rgba(255,79,38,1.000000)'}, 'mode': 'markers+lines', 'fillcolor': 'rgba(255,79,38,0.600000)', 'legendgroup': 'f1', 'showlegend': True, 'xaxis': 'x1', 'yaxis': 'y1'},
             {'type': 'scatter', 'name': 'f2', 'x': [-2.  , -1.  ,  0.01,  1.  ,  2.  ,  3.  ], 'y': [  2.5,   1,   1, 1,   2.5,   1], 'hoverinfo': 'name+text', 'marker': {'opacity': 1.0, 'symbol': 'circle', 'line': {'width': 0, 'color': 'rgba(50,50,50,0.8)'}}, 'line': {'color': 'rgba(79,102,165,1.000000)'}, 'mode': 'markers+lines', 'fillcolor': 'rgba(79,102,165,0.600000)', 'legendgroup': 'f2', 'showlegend': True, 'xaxis': 'x2', 'yaxis': 'y2'}],
        }
    ]
)
plotly.offline.plot(fig, filename='output/index_test.html')