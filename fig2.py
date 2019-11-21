import plotly.graph_objects as go
from plotly.subplots import make_subplots
terrorismDataPath = None

from plotly.subplots import make_subplots
import os
import pandas as pd
import plotly

import plotly.express as px

import numpy as np  # linear algebra


REMOVE_FAILED_KILLED_ATTEMPTS = False
REMOVE_UNKNOWN_KILLED = False
REMOVE_FAILED_WOUNDED_ATTEMPTS = False
REMOVE_UNKNOWN_WOUNDED = False
REMOVE_FAILED_CASUALITIES = False # -> influence a LOT the plto !! (cfr. USA VS
#  UK)

pd.set_option('display.max_columns', None)

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

attackTypeFreq = data
attackTypeFreq = data.attack_type.value_counts().astype('int32').reset_index().rename(columns={
    "index":"attack", "attack_type": "freq"})


attackTypeFreq = attackTypeFreq.astype({'freq': 'int32'})

print(attackTypeFreq.head())

labels = ["Eve", "Cain", "Seth", "Enos", "Noam", "Abel", "Awan", "Enoch", "Azura"]
parents = ["", "Eve", "Eve", "Seth", "Seth", "Eve", "Eve", "Awan", "Eve"]

attack = ["Bombing/Explosion", "Armed Assault", "Assassination",
          "Facility/Infrastructure Attack", "Hostage Taking (Kidnapping)"]
freq = [84322, 40353, 19233, 9788, 8610]

fig = make_subplots(
    cols = 2, rows = 1,
    column_widths = [0.4, 0.4],
    subplot_titles = ('branchvalues: <b>remainder<br />&nbsp;<br />', 'branchvalues: <b>total<br />&nbsp;<br />'),
    specs = [[{'type': 'treemap', 'rowspan': 1}, {'type': 'treemap'}]]
)

fig.add_trace(go.Treemap(
    labels = attack,
    parents = attack,
    values =  freq,
    textinfo = "label+value+percent parent+percent entry+percent root",
    ),
              row = 1, col = 1)

fig.add_trace(go.Treemap(
    branchvalues = "total",
    labels = labels,
    parents = parents,
    values = [65, 14, 12, 10, 2, 6, 6, 1, 4],
    textinfo = "label+value+percent parent+percent entry",
    outsidetextfont = {"size": 20, "color": "darkblue"},
    marker = {"line": {"width": 2}},
    pathbar = {"visible": False}),
              row = 1, col = 2)

fig.show()