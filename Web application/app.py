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
county = load_data(
    'https://raw.githubusercontent.com/BaiyanRen/real-estate-analysis/main/processed_data/tx_county_zhvi.csv')
city = load_data(
    'https://raw.githubusercontent.com/BaiyanRen/real-estate-analysis/main/processed_data/tx_city_zhvi.csv')

houston_zip = load_data(
    'https://raw.githubusercontent.com/BaiyanRen/real-estate-analysis/main/processed_data/houston_zip_zhvi.csv')
dallas_zip = load_data(
    'https://raw.githubusercontent.com/BaiyanRen/real-estate-analysis/main/processed_data/dallas_zip_zhvi.csv')
austin_zip = load_data(
    'https://raw.githubusercontent.com/BaiyanRen/real-estate-analysis/main/processed_data/austin_zip_zhvi.csv')
san_antonion_zip = load_data(
    'https://raw.githubusercontent.com/BaiyanRen/real-estate-analysis/main/processed_data/san_antonio_zip_zhvi.csv')

with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
    counties = json.load(response)
# Pre-process data
## Convert 'HomeType' to ordered categorical variable
for df in [county, city]:
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
                    id_vars=['HomeType', 'SizeRank', 'City', 'State', 'Metro', 'CountyName'],
                    var_name='Time',
                    value_name='HomeValue')
## select the top 10 largest cities as the list
city_list = list(city_zhvi['City'][:10])


## zip level data
## select 'hometype'
houston = houston_zip.groupby('HomeType')
houston_data = [data for label, data in houston]
dallas = dallas_zip.groupby('HomeType')
dallas_data = [data for label, data in dallas]
austin = austin_zip.groupby('HomeType')
austin_data = [data for label, data in austin]
san_antonion = san_antonion_zip.groupby('HomeType')
san_data = [data for label, data in san_antonion]

## County level data
## select 'hometype' in select box
## then select dates to show home value and home value changes
homes = county.groupby('HomeType')
home_label = [label for label, data in homes]
county_data = [data for label, data in homes]

dates = county.columns.tolist()[6:]


# Percentage change data in counties visualizaiton function

def countyPctFig(date1, date2):
    # Calculate percentage change between date2 and date1
    pct = 100 * (county[date2] - county[date1]) / county[date1]
    pct_ = pct.to_frame()
    pct_.rename(columns={0: 'change'}, inplace=True)
    df_pct = pd.merge(county[['FIPS', 'HomeType', 'CountyName', 'Metro', date1, date2]],
                      pct_,
                      left_index=True,
                      right_index=True)

    changes = df_pct.groupby('HomeType')
    change = [data for label, data in changes]

    df_ = change[hometype]
    color = 'change'
    p = px.choropleth(df_, geojson=counties, locations='FIPS', color=color,
                      color_continuous_scale='fall',
                      color_continuous_midpoint=0,
                      scope='usa',
                      hover_name='CountyName',
                      hover_data={'Metro': True,
                                  date1: ':$,.0f',
                                  date2: ':$,.0f',
                                  'Percentage change': (':.2%', df_['change'] / 100),
                                  'FIPS': False,
                                  'change': False}
                      )
    # zoom the map to show just Texas
    p.update_geos(fitbounds='locations')
    p.update_layout(coloraxis_colorbar=dict(title='%',
                                            tickfont=dict(size=12),
                                            thicknessmode='pixels',
                                            thickness=10,
                                            lenmode='pixels',
                                            len=300))
    st.plotly_chart(p, use_container_width=True)

def countyPctFig_budget(date1, date2):
    # Calculate percentage change between date2 and date1
    pct = 100 * (county[date2] - county[date1]) / county[date1]
    pct_ = pct.to_frame()
    pct_.rename(columns={0: 'change'}, inplace=True)
    df_pct = pd.merge(county[['FIPS', 'HomeType', 'CountyName', 'Metro', date1, date2]],
                      pct_,
                      left_index=True,
                      right_index=True)

    changes = df_pct.groupby('HomeType')
    change = [data for label, data in changes]

    df_ = change[hometype]
    df_final = df_[df_[date2] < budget]
    color = 'change'
    p = px.choropleth(df_final, geojson=counties, locations='FIPS', color=color,
                      color_continuous_scale='fall',
                      color_continuous_midpoint=0,
                      scope='usa',
                      hover_name='CountyName',
                      hover_data={'Metro': True,
                                  date1: ':$,.0f',
                                  date2: ':$,.0f',
                                  'Percentage change': (':.2%', df_final['change'] / 100),
                                  'FIPS': False,
                                  'change': False}
                      )
    # zoom the map to show just Texas
    p.update_geos(fitbounds='locations')
    p.update_layout(coloraxis_colorbar=dict(title='%',
                                            tickfont=dict(size=12),
                                            thicknessmode='pixels',
                                            thickness=10,
                                            lenmode='pixels',
                                            len=300))
    st.plotly_chart(p, use_container_width=True)

def countyFig(date2):
    df_county = county_data[hometype]
    color = date2
    p = px.choropleth(df_county, geojson=counties, locations='FIPS', color=color,
                      color_continuous_scale='Inferno',
                      scope='usa',
                      hover_name='CountyName',
                      hover_data={'Metro': True,
                                  date2: ':$,.0f',
                                  'FIPS': False}
                      )
    p.update_geos(fitbounds='locations')
    p.update_layout(coloraxis_colorbar=dict(title='$',
                                            tickfont=dict(size=12),
                                            thicknessmode='pixels',
                                            thickness=10,
                                            lenmode='pixels',
                                            len=300))
    st.plotly_chart(p, use_container_width=True)

def countyFig_budget(date2):
    df_county = county_data[hometype]
    df_county_final = df_county[df_county[date2] < budget]
    color = date2
    p = px.choropleth(df_county_final, geojson=counties, locations='FIPS', color=color,
                      color_continuous_scale='Inferno',
                      scope='usa',
                      hover_name='CountyName',
                      hover_data={'Metro': True,
                                  date2: ':$,.0f',
                                  'FIPS': False}
                      )
    p.update_geos(fitbounds='locations')
    p.update_layout(coloraxis_colorbar=dict(title='$',
                                            tickfont=dict(size=12),
                                            thicknessmode='pixels',
                                            thickness=10,
                                            lenmode='pixels',
                                            len=300))
    st.plotly_chart(p, use_container_width=True)
# monthly data in four cities visualization function

def cityFig(df):
    tile_provider = get_provider(Vendors.CARTODBPOSITRON_RETINA)
    source = ColumnDataSource(data=df)
    color_mapper = linear_cmap(field_name=selected_date, palette=tuple(reversed(Inferno256)),
                               low=df[selected_date].min(),
                               high=df[selected_date].max())
    tooltips = [('Zip code', '@Zip'),
                ('CountyName', '@CountyName')]

    p = figure(plot_width=580, plot_height=450,
               x_axis_type='mercator', y_axis_type='mercator',
               x_axis_label='Longitude', y_axis_label='Latitude',
               tooltips=tooltips)

    p.add_tile(tile_provider)

    p.circle(source=source,
             x='mercator_x', y='mercator_y',
             fill_color=color_mapper,
             fill_alpha=0.5,
             line_color='black',
             size=10)

    format_tick = NumeralTickFormatter(format='$ 0,0[.]00')

    color_bar = ColorBar(color_mapper=color_mapper['transform'],
                         formatter=format_tick,
                         width=10,
                         background_fill_alpha=0,
                         label_standoff=15,
                         location=(0, 0))
    p.add_layout(color_bar, 'right')
    st.bokeh_chart(p, use_container_width=True)


row1_1, row1_2 = st.beta_columns((1, 1))

with row1_1:
    st.title('Analysis of Real-estate Market in Texas')

with row1_2:
    st.markdown(
        '''
        
            Assessing how home values change over time in the State of Texas and at its major cities.
            
            By selecting the home type and sliding the time, you can explore the house values of your desired home 
            filtered by your budget. 
            
            Home values are based on Zillow Home Value Index from [Zillow Housing Data](https://www.zillow.com/research/data/)
            
        '''
    )

st.write(
    '''

    '''
)

col1, col2 = st.beta_columns(2)

with col1:
    hometype = st.selectbox(label='Select your desired home type:',
                            options=list(range(len(home_label))),
                            index=4,
                            format_func=lambda x: home_label[x])
with col2:
    budget = st.number_input(label='Your Budget ($):',
                             min_value=50000,
                             value=300000,
                             step=10000,
                             format='%g')

date1 = st.select_slider(label='From:',
                         options=dates,
                         value='2011-01-31')

date2 = st.select_slider(label='To:',
                         options=dates,
                         value='2021-01-31')

row2_1, row2_2 = st.beta_columns((1, 1))

with row2_1:
    st.subheader('Return on Investment of {}'.format(home_label[hometype]))
    st.write('from {} to {}.'.format(date1, date2))

    countyPctFig(date1, date2)

with row2_2:
    st.subheader('Home Values of {}'.format(home_label[hometype]))
    st.write('on {}'.format(date2))

    countyFig(date2)



st.subheader('With budget of ${:,}'.format(budget))

row3_1, row3_2 = st.beta_columns((1, 1))

with row3_1:
    st.subheader('Return on Investment of {}'.format(home_label[hometype]))
    st.write('from {} to {}.'.format(date1, date2))

    countyPctFig_budget(date1, date2)

with row3_2:
    st.subheader('Home Values of {}'.format(home_label[hometype]))
    st.write('on {}'.format(date2))

    countyFig_budget(date2)

selected_city = st.selectbox(label='Select your desired city:',
                             options=city_list)

st.write('Changes in Home Values in {}.'.format(selected_city))

df = city_zhvi[city_zhvi['City'] == selected_city].copy()
fig = px.line(df, x='Time', y='HomeValue', color='HomeType',
              color_discrete_sequence=px.colors.qualitative.Set2,
              template='simple_white',
              labels={'HomeValue': 'Home Values',
                      'HomeType': 'Home Types'},
              hover_name='Time',
              hover_data={'HomeValue': ':$,.0f'}
              )
fig.update_layout(paper_bgcolor='rgba(0, 0, 0, 0)', # rgba color: (red, green, blue, alpha)
                  plot_bgcolor='rgba(0, 0, 0, 0)')

st.plotly_chart(fig, use_container_width=True)
