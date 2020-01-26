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

df = data.astype({'year': 'int32'})
df = df["year"].value_counts().sort_index().to_frame()
df = df.rename(columns={"year": "Number of attacks"})
df['year'] = df.index



fig = px.line(df, x="year", y="Number of attacks", title='Evolution of '
                                                         'number of '
                                                         'terrorist attacks '
                                                         'worldwide', template="plotly_dark")
fig.show()

# fig.show()
plotly.offline.plot(fig, filename='output/line_plot.html')