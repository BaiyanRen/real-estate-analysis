import streamlit as st
import numpy as np
import pandas as pd
from urllib.request import urlopen
import json
# visualization
import plotly.express as px

from bokeh.io import output_notebook, show, output_file
from bokeh.plotting import figure, ColumnDataSource, gmap
from bokeh.tile_providers import get_provider, Vendors
from bokeh.transform import linear_cmap
from bokeh.palettes import Inferno256
from bokeh.layouts import row, column
from bokeh.models import GeoJSONDataSource, LinearColorMapper, ColorBar, NumeralTickFormatter, GMapOptions

import os
import webbrowser

st.set_page_config(layout='wide')

webbrowser.open('zillowSearchBox.html')

@st.cache
def load_data(csv):
    df = pd.read_csv(csv)
    return df

# Load data
county = load_data('https://raw.githubusercontent.com/BaiyanRen/real-estate-analysis/main/processed_data/tx_county_zhvi.csv')
city = load_data('https://raw.githubusercontent.com/BaiyanRen/real-estate-analysis/main/processed_data/tx_city_zhvi.csv')
houston_zip = load_data('https://raw.githubusercontent.com/BaiyanRen/real-estate-analysis/main/processed_data/houston_zip_zhvi.csv')
dallas_zip = load_data('https://raw.githubusercontent.com/BaiyanRen/real-estate-analysis/main/processed_data/dallas_zip_zhvi.csv')
austin_zip = load_data('https://raw.githubusercontent.com/BaiyanRen/real-estate-analysis/main/processed_data/austin_zip_zhvi.csv')
san_antonion_zip = load_data('https://raw.githubusercontent.com/BaiyanRen/real-estate-analysis/main/processed_data/san_antonio_zip_zhvi.csv')

# Pre-process data
## Convert 'HomeType' to ordered categorical variable
for df in [county, city, houston_zip, dallas_zip, austin_zip, san_antonion_zip]:
    df['HomeType'] = pd.Categorical(df['HomeType'], ordered=True,
                                        categories=['Condominium and Co-operative Homes',
                                                    'Single-family Residences',
                                                    'One Bedroom',
                                                    'Two Bedrooms',
                                                    'Three Bedrooms',
                                                    'Four Bedrooms',
                                                    'Five Bedrooms And More'])
## City level data
## melt to make lineplot
city_zhvi = pd.melt(city,
                    id_vars = ['HomeType', 'SizeRank', 'City', 'State', 'Metro', 'CountyName'],
                    var_name = 'Time',
                    value_name = 'HomeValue')
## zip level data
## select 'dates' to show home values at different zipcode
dates = houston_zip.columns.tolist()[11:]
## County level data
## select 'hometype' in select box
## select 'period' to show home value changes
homes = county.groupby('HomeType')
home_label = [label for label, data in homes]
home_data = [data for label, data in homes]
periods = county.columns.tolist()[-4:]

# The first row of web
col1_1, col1_2 = st.beta_columns((3, 4))

with col1_1:
    st.title('Home Values in Texas')
    hometype = st.selectbox(label='Select your interested home type:',
                        options=list(range(len(home_label))),
                        index=0,
                        format_func = lambda x: home_label[x])

with col1_2:
    st.write(
        '''
        Assessing how home values change over time in the State of Texas and at its major cities.
        
        By selecting the home type and sliding the time, you can explore the house values in your desired future home.
        '''
    )

col2_1, col2_2, col2_3 = st.beta_columns((2, 1, 4))

with col2_1:
    select_period = st.select_slider(label='Select period:',
                                     options=periods)

with col2_3:
    selected_date = st.select_slider(label='Select the date of record:',
                                     options=dates)


col3_1, col3_2, col3_3, col3_4, col3_5 = st.beta_columns((3, 1, 1, 1, 1))

with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
    counties = json.load(response)

with col3_1:
    df = home_data[hometype]
    color = select_period
    st.write('**Housing Value Changes (%) in TX in {}**'.format(select_period))
    st.write('{}'.format(home_label[hometype]))
    fig = px.choropleth(df, geojson=counties, locations='FIPS', color=color,
                        color_continuous_scale='fall',
                        color_continuous_midpoint=0,
                        scope='usa',
                        labels={'3ychange': 'Three-year Changes (%)'},
                        hover_name='CountyName',
                        hover_data=['2021-01-31'])
    # zoom the map to show just Texas
    fig.update_geos(fitbounds='locations')
    fig.update_layout(coloraxis_colorbar=dict(title='Changes (%)',
                                              thicknessmode='pixels',
                                              thickness=15))

    st.plotly_chart(fig, use_container_width=True)
