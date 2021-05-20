import streamlit as st
import numpy as np
import pandas as pd
from urllib.request import urlopen
import json
# visualization
import plotly.express as px

st.set_page_config(layout='wide')


@st.cache
def load_data(csv):
    df = pd.read_csv(csv)
    return df


# Load data
king = load_data(
    'https://raw.githubusercontent.com/BaiyanRen/real-estate-analysis/main/processed_data/king_zip_zhvi.csv')

# Pre-process data
## melt to make lineplot
king_time = pd.melt(king,
                    id_vars=['HomeType', 'Latitude', 'Longitude', 'Zip', 'State', 'City', 'Metro', 'CountyName'],
                    var_name='Time',
                    value_name='HomeValues')

## save zip codes into a list
zip_list = king['Zip'].unique().tolist()

## group by home types, save home types in a list
homes = king.groupby('HomeType')
home_label = [label for label, data in homes]
home_data = [data for label, data in homes]

## save dates into a list
dates = king.columns.tolist()[8:]


@st.cache
def Lineplot(df, zip):
    df1 = df[df['Zip'] == selected_zip].copy()
    fig = px.line(df1, x='Time', y='HomeValues', color='HomeType',
                  color_discrete_sequence=px.colors.qualitative.Set2,
                  template='simple_white',
                  labels={'HomeValues': 'Home Values',
                          'HomeType': 'Home Types'},
                  hover_name='Time',
                  hover_data={'HomeValues': ':$,.0f'}
                  )
    fig.update_layout(paper_bgcolor='rgba(0, 0, 0, 0)',  # rgba color: (red, green, blue, alpha)
                      plot_bgcolor='rgba(0, 0, 0, 0)')

    fig.update_layout(legend=dict(yanchor="top",
                                  y=0.99,
                                  xanchor="left",
                                  x=0.01
                                  ))
    return fig


@st.cache
def zipmap(df, date):
    df1 = df[hometype]
    px.set_mapbox_access_token(
        'pk.eyJ1IjoiYmFpeWFucmVuIiwiYSI6ImNrbTV3amFsZDBpaDMydXFiNjRwNTEyZTMifQ.ti6dUHMEzzlzG3rNGoFhTA')
    fig = px.scatter_mapbox(df1, lat='Latitude', lon='Longitude', color=df1[date],
                            hover_name='Zip',
                            hover_data={'Latitude': False,
                                        'Longitude': False,
                                        '2021-01-31': ':$,.0f',
                                        'City': True
                                        },
                            zoom=8,
                            color_continuous_scale=px.colors.sequential.Turbo,
                            mapbox_style='basic')
    fig.update_traces(marker=dict(size=15,
                                  opacity=.8),
                      selector=dict(type='scattermapbox'))
    fig.update_layout(coloraxis_colorbar=dict(title='$',
                                              thicknessmode='pixels',
                                              thickness=15,
                                              lenmode='pixels',
                                              len=300))

    return fig


@st.cache
def zipmap_budget(df, date, budget):
    df1 = df[hometype]
    df2 = df1[df1[date] < budget]
    px.set_mapbox_access_token(
        'pk.eyJ1IjoiYmFpeWFucmVuIiwiYSI6ImNrbTV3amFsZDBpaDMydXFiNjRwNTEyZTMifQ.ti6dUHMEzzlzG3rNGoFhTA')
    fig = px.scatter_mapbox(df2, lat='Latitude', lon='Longitude', color=df2[date],
                            hover_name='Zip',
                            hover_data={'Latitude': False,
                                        'Longitude': False,
                                        '2021-01-31': ':$,.0f',
                                        'City': True
                                        },
                            zoom=8,
                            color_continuous_scale=px.colors.sequential.Turbo,
                            mapbox_style='basic')
    fig.update_traces(marker=dict(size=15,
                                  opacity=.8),
                      selector=dict(type='scattermapbox'))
    fig.update_layout(coloraxis_colorbar=dict(title='$',
                                              thicknessmode='pixels',
                                              thickness=15,
                                              lenmode='pixels',
                                              len=300))
    return fig


# Web

# Sidebar - overview of Real-estate market
st.sidebar.subheader('Overview')

selected_zip = st.sidebar.selectbox(label='Select the zip code:',
                                    options=zip_list)

hometype = st.sidebar.selectbox(label='Select your desired home type:',
                                options=list(range(len(home_label))),
                                index=4,
                                format_func=lambda x: home_label[x])

budget = st.sidebar.number_input(label='Your Budget ($):',
                                 min_value=100000,
                                 value=300000,
                                 step=10000,
                                 format='%g')

date = st.sidebar.select_slider(label='Select the date',
                                options=dates,
                                value='2021-03-31')

# Sidebar - prediction input variables
st.sidebar.subheader('User Input Variables')

livingarea = st.sidebar.number_input(label='Living Area:',
                                     value=2000,
                                     step=1)

garagesize = st.sidebar.number_input(label='Garage Size:',
                                     value=2,
                                     step=1)

yearbuilt = st.sidebar.number_input(label='Year of Built:',
                                    value=2021,
                                    step=1)
row1_1, row1_2 = st.beta_columns((1, 1))

with row1_1:
    st.title('Analysis of Real-estate Market in Seattle')

with row1_2:
    st.markdown(
        '''
        
            Assessing Real Estate Investment in Seattle.
            
            By selecting the house type and sliding the time, you can explore the home values at different zip codes and
            filter it by your budget. 
            
            Home values are based on Zillow Home Value Index from [Zillow Housing Data](https://www.zillow.com/research/data/)
            
        '''
    )

st.write(
    '''

    '''
)

# Visualizations

st.subheader('Home Values of {}'.format(home_label[hometype]))
st.write('on {}'.format(date))

fig2 = zipmap(home_data, date)
st.plotly_chart(fig2, use_container_width=True)

st.subheader('With budget of ${:,}'.format(budget))

fig3 = zipmap_budget(home_data, date, budget)
st.plotly_chart(fig3, use_container_width=True)

st.subheader('Changes in Home Values in {}.'.format(selected_zip))

fig1 = Lineplot(king_time, selected_zip)
st.plotly_chart(fig1, use_container_width=True)
