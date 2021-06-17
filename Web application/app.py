import streamlit as st
import numpy as np
import pandas as pd
from urllib.request import urlopen
import json
# visualization
import plotly.express as px
# machine learning
import pickle
import xgboost as xgb
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

## label: Yes/No
yes_no = ['No', 'Yes']

## label: poor to great
conditions = ['Very Poor', 'Poor', 'Average', 'Good', 'Excellent']


## Plotting functions
def Lineplot(df, zip):
    df1 = df[df['Zip'] == zip].copy()
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

## show dataframe containing user input features
def df_inputs():
    data = {'bedooms': bedrooms,
            'bathrooms': bathrooms,
            'sqft_living': livingarea,
            'sqft_log': lotarea,
            'floors': floors,
            'waterfront': waterfront,
            'view': view,
            'condition': condition,
            'grade': grade,
            'sqft_above': sqft_above,
            'sqft_basement': sqft_basement,
            'yr_built': yr_built,
            'yr_renovated': yr_renovated,
            'zipcode': zipcode,
            'lat': lat,
            'long': long,
            'sqft_living15': sqft_living15,
            'sqft_lot15': sqft_lot15,
            '30_FRM': frm_30,
            '15_FRM': frm_15}

    features = pd.DataFrame(data, index=['input'])
    return features
# Web

# Sidebar - overview of Real-estate market
st.sidebar.subheader('Overview')

hometype = st.sidebar.selectbox(label='Select your desired home type:',
                                options=list(range(len(home_label))),
                                index=4,
                                format_func=lambda x: home_label[x])

date = st.sidebar.select_slider(label='Select the date',
                                options=dates,
                                value='2021-03-31')

budget = st.sidebar.number_input(label='Your Budget ($):',
                                 min_value=100000,
                                 value=600000,
                                 step=10000,
                                 format='%g')

selected_zip = st.sidebar.selectbox(label='Select the zip code:',
                                    options=zip_list)

# Sidebar - prediction input variables
st.sidebar.subheader('User Input Variables')

bedrooms = st.sidebar.number_input(label='Bedrooms',
                                   value=3,
                                   min_value=0,
                                   step=1)
bathrooms = st.sidebar.number_input(label='Bathrooms',
                                    value=2,
                                    min_value=0,
                                    step=1)

livingarea = st.sidebar.number_input(label='Living Space (sqft)',
                                     value=2000,
                                     step=1)
lotarea = st.sidebar.number_input(label='Land Lot (sqft)',
                                  value=10000,
                                  step=1)
floors = st.sidebar.number_input(label='Floors',
                                 value=1,
                                 step=1)
waterfront = st.sidebar.radio(label='Waterfront',
                              options=[0, 1],
                              index=0,
                              format_func=lambda x: yes_no[x])
view = st.sidebar.selectbox(label='View of the Property',
                            options=[0, 1, 2, 3, 4],
                            index=2,
                            format_func=lambda x: conditions[x])
condition = st.sidebar.selectbox(label='Condition of the Property',
                                 options=[1, 2, 3, 4, 5],
                                 index=2,
                                 format_func=lambda x: conditions[x - 1])
grade = st.sidebar.slider(label = 'Quality Level of Construction and Design',
                          min_value=1,
                          max_value=13,
                          value=7,
                          step=1,
                          format='%g')
sqft_above = st.sidebar.number_input(label='Above Ground Living Area (sqft)',
                                     value=1000,
                                     step=1)
sqft_basement = st.sidebar.number_input(label='Basement Area (sqft)',
                                        value=500,
                                        step=1)
yr_built = st.sidebar.number_input(label='Year of Built',
                                    value=2010,
                                    step=1)

yr_renovated = st.sidebar.number_input(label='Year of Last Renovation',
                                    value=2015,
                                    step=1)
zipcode = st.sidebar.selectbox(label='Zipcode',
                                    options=zip_list)
lat = st.sidebar.number_input(label='Latitude',
                              value=47.1559,
                              step=0.0001)
long = st.sidebar.number_input(label='Longitude',
                               value=-122.5190,
                               step=0.0001)
sqft_living15 = st.sidebar.number_input(label='Averaged Living Space of Nearest 15 Neighbors (sqft)',
                                        value=2000,
                                        step=1)
sqft_lot15 = st.sidebar.number_input(label='Averaged Land Lots of Nearest 15 Neighbors (sqft)',
                                     value=10000,
                                     step=1)
frm_30 = st.sidebar.number_input(label='30-Year Fixed Mortgage Rates (%)',
                                 value=3.12,
                                 step=0.01)
frm_15 = st.sidebar.number_input(label='15-Year Fixed Mortgage Rates (%)',
                                 value=2.37,
                                 step=0.01)


estimator = pickle.load(open('estimator.sav', 'rb'))






# Main page
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

st.subheader('User Input Features')
inputs = df_inputs()
st.write(inputs)

prediction = estimator.predict(inputs)
st.subheader('Home Value Estimation')
st.write('$ {}'.format(prediction[0]))
