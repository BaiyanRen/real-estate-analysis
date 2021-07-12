import streamlit as st
import streamlit.components.v1 as components

import pandas as pd

# visualization
import plotly.express as px
# machine learning
import pickle
st.set_page_config(layout='wide')


# Functions
@st.cache
def load_data(csv):
    '''
    Load csv into dataframe
    '''
    df = pd.read_csv(csv)
    return df

@st.cache
def zipmap(df, date, mapbox_token):
    '''
    Visualize the home values on the map on the zip code level
    '''

    df1 = df[hometype]
    px.set_mapbox_access_token(mapbox_token)
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
def Lineplot(df, zip):
    '''
    Visualize the home values change with time
    '''
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

def df_inputs():
    '''
    show user inputs in a dataframe
    '''
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

# Load data
king = load_data(
    'https://raw.githubusercontent.com/BaiyanRen/real-estate-analysis/main/Datasets/king_zip_zhvi.csv')

# Load estimator
estimator = pickle.load(open('estimator.sav', 'rb'))

# Load mapbox access token
with open('secret.txt', 'r') as f:
    mapbox_token = f.read()

# Preprocessing
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



# Web page

# Sidebar - overview of Real-estate market
st.sidebar.subheader('Overview')

hometype = st.sidebar.selectbox(label='Select your desired home type:',
                                options=list(range(len(home_label))),
                                index=4,
                                format_func=lambda x: home_label[x])

date = st.sidebar.select_slider(label='Select the date',
                                options=dates,
                                value='2021-03-31')


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


# Main page

st.title('Find Homes in Seattle')


# Visualizations

st.subheader('Home Values of {}'.format(home_label[hometype]))
st.write('on {}'.format(date))
fig2 = zipmap(home_data, date, mapbox_token)
st.plotly_chart(fig2, use_container_width=True)

st.subheader('Changes in Home Values in {}.'.format(selected_zip))

fig1 = Lineplot(king_time, selected_zip)
st.plotly_chart(fig1, use_container_width=True)

# Searching homes

components.html(
    '''
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Find Homes</title>
    </head>
    <body>
        <div id="zillow-large-search-box-widget-container" style="width:432px;overflow:hidden;background-color:#e7f1fd;color:#555; font: normal normal normal 13px verdana,arial,sans-serif;line-height:13px;margin:0 auto;padding:0;text-align:center;border:1px solid #adcfff;letter-spacing:0;text-transform:none;"><h2 style="color:#d61;text-align:left;font-size:20px;line-height:20px;font-weight:normal;float:left;width:200px;margin-left:10px;margin-top:5px;letter-spacing:0;text-transform:none;">Find Homes</h2><div style="float:right;"><a href="https://www.zillow.com/" target="_blank" rel="nofollow"><img alt="Zillow Real Estate Information" style="border:0;" src="https://www.zillow.com/widgets/GetVersionedResource.htm?path=/static/images/powered-by-zillow.gif"></img></a></div><iframe scrolling="no" src="https://www.zillow.com/widgets/search/LargeSearchBoxWidget.htm?did=zillow-large-search-box-iframe-widget&type=iframe&rgname=Seattle+WA&shvi=yes" width="430" frameborder="0" height="400"></iframe><table id="zillow-tnc-widget-footer-links" width="100%" style="font: normal normal normal 10px verdana,arial,sans-serif;text-align:left;line-height:12px;margin:10px 5px;padding:0;border-spacing:0;border-collapse:collapse;"><tbody style="margin:0;padding:0;"><tr style="margin:0;padding:0;"><td style="font-weight:bold;font-size:10px;color:#555;text-align:left;margin:0;padding:0;">QUICK LINKS:</td></tr><tr style="margin:0;padding:0;"><td style="margin:0;padding:0;"><span id="widgetFooterLink" class="regionBasedLink"><a href="https://www.zillow.com/seattle-wa/" target="_blank" rel="nofollow" style="color:#36b;font-family:verdana,arial,sans-serif;font-size:10px;margin:0 5px 0 0;padding:0;text-decoration:none;"><span class="region">Seattle</span> Real Estate Listing</a></span></td><td style="margin:0;padding:0;"><span id="widgetFooterLink"><a href="https://www.zillow.com/mortgage-rates/" target="_blank" rel="nofollow" style="color:#36b;font-family:verdana,arial,sans-serif;font-size:10px;margin:0 5px 0 0;padding:0;text-decoration:none;">Mortgage Rates</a></span></td><td style="margin:0;padding:0;"><span id="widgetFooterLink"><a href="https://www.zillow.com/refinance/" target="_blank" rel="nofollow" style="color:#36b;font-family:verdana,arial,sans-serif;font-size:10px;margin:0 5px 0 0;padding:0;text-decoration:none;">Refinancing</a></span></td></tr><tr style="margin:0;padding:0;"><td style="margin:0;padding:0;"><span id="widgetFooterLink" class="regionBasedLink"><a href="https://www.zillow.com/seattle-wa/foreclosures/" target="_blank" rel="nofollow" style="color:#36b;font-size:10px;margin:0 5px 0 0;padding:0;text-decoration:none;"><span class="region">Seattle</span> Foreclosures</a></span></td><td style="margin:0;padding:0;"><span id="widgetFooterLink"><a href="https://www.zillow.com/mortgage-calculator/" target="_blank" rel="nofollow" style="color:#36b;font-size:10px;margin:0 5px 0 0;padding:0;text-decoration:none;">Mortgage Calculators</a></span></td><td style="margin:0;padding:0;"><span id="widgetFooterLink"><a href="https://www.zillow.com/mortgage-rates/" target="_blank" rel="nofollow" style="color:#36b;font-size:10px;margin:0 5px 0 0;padding:0;text-decoration:none;">Purchase Loans</a></span></td></tr></tbody></table></div>
    </body>
''',
    height=600)

# Prediction

st.subheader('User Input Features')
inputs = df_inputs()
st.write(inputs)

prediction = estimator.predict(inputs)
st.subheader('Home Value Estimation')
st.write('$ {}'.format(prediction[0]))
