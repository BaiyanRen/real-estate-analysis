import streamlit as st
import plotly.express as px
import pandas as pd



def app():
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


    # Load data
    king = load_data(
        'https://raw.githubusercontent.com/BaiyanRen/real-estate-analysis/main/Datasets/king_zip_zhvi.csv')
    # Load mapbox access token
    with open('pages/secret.txt', 'r') as f:
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

    st.subheader('Real Estate Market Visualization in Seattle')

    hometype = st.selectbox(label='Select your desired home type:',
                                    options=list(range(len(home_label))),
                                    index=4,
                                    format_func=lambda x: home_label[x])

    date = st.select_slider(label='Select the date',
                                    options=dates,
                                    value='2021-03-31')

    st.subheader('Home Values of {}'.format(home_label[hometype]))
    st.write('on {}'.format(date))
    fig2 = zipmap(home_data, date, mapbox_token)
    st.plotly_chart(fig2, use_container_width=True)

    selected_zip = st.selectbox(label='Select the zip code:',
                                        options=zip_list)

    st.subheader('Changes in Home Values in {}.'.format(selected_zip))

    fig1 = Lineplot(king_time, selected_zip)
    st.plotly_chart(fig1, use_container_width=True)