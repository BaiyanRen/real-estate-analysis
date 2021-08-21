import streamlit as st
import pandas as pd
import pickle


def app():
    @st.cache
    def load_data(csv):
        '''
        Load csv into dataframe
        '''
        df = pd.read_csv(csv)
        return df

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

    # Load estimator
    estimator = pickle.load(open('pages/estimator.sav', 'rb'))

    ## label: Yes/No
    yes_no = ['No', 'Yes']

    ## label: poor to great
    conditions = ['Very Poor', 'Poor', 'Average', 'Good', 'Excellent']

    king = load_data(
        'https://raw.githubusercontent.com/BaiyanRen/real-estate-analysis/main/Datasets/king_zip_zhvi.csv')

    king_time = pd.melt(king,
                        id_vars=['HomeType', 'Latitude', 'Longitude', 'Zip', 'State', 'City', 'Metro', 'CountyName'],
                        var_name='Time',
                        value_name='HomeValues')

    ## save zip codes into a list
    zip_list = king['Zip'].unique().tolist()

    st.sidebar.markdown('''
                        **Introduction** 
                        
                        
                        If you have a house on your list,
                        
                        try estimate its price here!
                        
                        ''')

    bedrooms = st.number_input(label='Bedrooms',
                                       value=3,
                                       min_value=0,
                                       step=1)
    bathrooms = st.number_input(label='Bathrooms',
                                        value=2,
                                        min_value=0,
                                        step=1)

    livingarea = st.number_input(label='Living Space (sqft)',
                                         value=2000,
                                         step=1)
    lotarea = st.number_input(label='Land Lot (sqft)',
                                      value=10000,
                                      step=1)
    floors = st.number_input(label='Floors',
                                     value=1,
                                     step=1)
    waterfront = st.radio(label='Waterfront',
                                  options=[0, 1],
                                  index=0,
                                  format_func=lambda x: yes_no[x])
    view = st.selectbox(label='View of the Property',
                                options=[0, 1, 2, 3, 4],
                                index=2,
                                format_func=lambda x: conditions[x])
    condition = st.selectbox(label='Condition of the Property',
                                     options=[1, 2, 3, 4, 5],
                                     index=2,
                                     format_func=lambda x: conditions[x - 1])
    grade = st.slider(label='Quality Level of Construction and Design',
                              min_value=1,
                              max_value=13,
                              value=7,
                              step=1,
                              format='%g')
    sqft_above = st.number_input(label='Above Ground Living Area (sqft)',
                                         value=1000,
                                         step=1)
    sqft_basement = st.number_input(label='Basement Area (sqft)',
                                            value=500,
                                            step=1)
    yr_built = st.number_input(label='Year of Built',
                                       value=2010,
                                       step=1)

    yr_renovated = st.number_input(label='Year of Last Renovation',
                                           value=2015,
                                           step=1)
    zipcode = st.selectbox(label='Zipcode',
                                   options=zip_list)
    lat = st.number_input(label='Latitude',
                                  value=47.1559,
                                  step=0.0001)
    long = st.number_input(label='Longitude',
                                   value=-122.5190,
                                   step=0.0001)
    sqft_living15 = st.number_input(label='Averaged Living Space of Nearest 15 Neighbors (sqft)',
                                            value=2000,
                                            step=1)
    sqft_lot15 = st.number_input(label='Averaged Land Lots of Nearest 15 Neighbors (sqft)',
                                         value=10000,
                                         step=1)
    frm_30 = st.number_input(label='30-Year Fixed Mortgage Rates (%)',
                                     value=3.12,
                                     step=0.01)
    frm_15 = st.number_input(label='15-Year Fixed Mortgage Rates (%)',
                                     value=2.37,
                                     step=0.01)

    st.subheader('User Input Features')
    inputs = df_inputs()
    st.write(inputs)
    prediction = estimator.predict(inputs)

    if st.button('Estimate the Price'):
        st.subheader('Home Value Estimation')
        st.write('$ {}'.format(prediction[0]))
