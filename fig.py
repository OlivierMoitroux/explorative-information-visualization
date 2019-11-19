import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os
import pandas as pd

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
#https://plot.ly/~harry11733/105/#code


# ====================================================================== #
#                    Hyperparameters of the visualization                #
# ====================================================================== #
# COlorscale

REMOVE_FAILED_KILLED_ATTEMPTS = False
REMOVE_UNKNOWN_KILLED = False
REMOVE_FAILED_WOUNDED_ATTEMPTS = False
REMOVE_UNKNOWN_WOUNDED = False
REMOVE_FAILED_CASUALITIES = True # -> influence a LOT the plto !! (cfr. USA VS
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
#                   Building dashboard visualization                     #
# ====================================================================== #

data = data[0:1000]

# Frequency for each countries
freq = data
# test = freq.country.value_counts().reset_index()
freq = freq.country.value_counts().reset_index().rename(columns={
    "country":"events", "index": "country"})
print(freq.head(10))

# Initialize figure with subplots
fig = make_subplots(
    rows=2, cols=2,
    column_widths=[0.6, 0.4],
    row_heights=[0.55, 0.45],
    specs=[[{"type": "scattergeo", "rowspan": 2}, {"type": "bar"}],
           [            None                    , {"type": "xy"}]],
    #subplot_titles=["hello", "hello", "hello"] # API VERY BUGGY
    # animation_frame=data["year"]
)






# Add terrorism events locations on globe map
fig.add_trace(
    go.Scattergeo(lat=data["lat"],
                  lon=data["long"],
                  mode="markers",
                hoverinfo='text',
                  # hovertext=data["country"], # $%{y:.2f}
                  #   hovertemplate =
                  #       '<b>Country</b>: %{text}<br>'+
                  #       '<i>Casualities</i>: %{marker.color:,}<br>',
                  # text = data["country"], # $%{y:.2f}

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





#
#
# ['(sepal length: '+'{:.2f}'.format(sl)+', sepal width:'+'{:.2f}'.format(sw)+')'+
#   '<br>(petal length: '+'{:.2f}'.format(pl)+', petal width:'+'{:.2f}'.format(pw)+')'
#   for sl, sw, pl, pw in zip(list(df['sepal length (cm)']), list(df['sepal width (cm)']),
#                            list(df['petal length (cm)']), list(df['petal width (cm)'])) ]



                  showlegend=False,
                  name= "Attack", # would appear on hover otherwise. data[
                  # "attack_type"] does not work unfortunately
                  marker=dict(
                      # colorscale = scl,
                      colorscale="Portland", #"Viridis", "Portland", "YlOrRd"
                      color=data['casualities'],
                      reversescale = False,
                      autocolorscale = False,
                        colorbar=dict(
                                    title={"text": "Casualities",
                                           "side":"top"},
                                     x=0.57,
                                    y = 0.55,
                                    xanchor= 'center',

                            yanchor="middle",

                                ),
                      # color="crimson",

                      size=8, # 4
                      opacity=0.8,
                      line = dict(
                                  width=1,
                                  color='rgba(102, 102, 102)'
                              ),


                  ),


                  # animation_frame="year"

                  # marker = dict(
                  #             size = 8,
                  #             opacity = 0.8,
                  #             reversescale = True,
                  #             autocolorscale = False,
                  #             symbol = 'square',
                  #             line = dict(
                  #                 width=1,
                  #                 color='rgba(102, 102, 102)'
                  #             ),
                  #             colorscale = scl,
                  #             cmin = 0,
                  #             color = df['cnt'],
                  #             cmax = df['cnt'].max(),
                  #             colorbar=dict(
                  #                 title="Incoming flightsFebruary 2011"
                  #             )


    ), # ,
    # symbol="asterisk" ) -> does not work
    row=1, col=1
)


# Add locations bar chart
fig.add_trace(
    go.Bar(x=freq["country"][0:10],y=freq["events"][0:10], marker=dict(
        color="crimson"), name="Number of attacks", showlegend=True),
    row=1, col=2
)



fig.add_trace(
    go.Histogram(
        x=data["country"], name="number of events"
    ),
    row=2, col=2
)
#
# # Add 3d surface of volcano
# fig.add_trace(
#     go.Surface(z=df_v.values.tolist(), showscale=False),
#     row=2, col=2
# )
#

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


# colorbar(title = 'GDP (log)') %>%
#      layout(title = '', geo = g)



# Rotate x-axis labels
fig.update_xaxes(tickangle=45)


# Set theme, margin, and annotation in layout
fig.update_layout(
    template="plotly_dark",
    margin=dict(r=10, t=80, b=40, l=10),
    annotations=[
        go.layout.Annotation(
            text="Source: Global Terrorism Database (GTD - Kaggle)",
            showarrow=False,
            xref="paper",
            yref="paper",
            x=0,
            y=-0.1),
        # DOES NOT WORK unfortunately
        # go.layout.Annotation(
        #     xref= 'subplot',
        #     subplot= [1],
        #     x= 0.5,
        #     xanchor= 'center',
        #     text= 'Hello'
        # ),

        go.layout.Annotation(
                    xref= 'paper',
                    showarrow=False,
                    x= 0.82,
                    y = 1.025,
                    font= {"size": 18},
                    xanchor= 'center',
            yref="paper",
                    yanchor="top",
                    text= '<b>Number of attacks</b>'
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
    # title = {'text':"My title", "font": {"size": 30}, "xanchor":"auto",
    #          "xref":"container"}
    # title=go.layout.Title(text="A Bar Chart",
    #                           font=go.layout.title.Font(size=30)))
    # title_text="Worldwide terrorism across time", title_font_size=30
# xanchor: "auto" | "left" | "center" | "right"
)

fig.show()


#
# import plotly.express as px
# gapminder = px.data.gapminder()
# px.scatter(gapminder, x="gdpPercap", y="lifeExp", animation_frame="year", animation_group="country",
#            size="pop", color="continent", hover_name="country",
#            log_x=True, size_max=55, range_x=[100,100000], range_y=[25,90])