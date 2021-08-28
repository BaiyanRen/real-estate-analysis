# Web-based Prediction Model of Real-estate market in Seattle

![Houses](https://github.com/BaiyanRen/real-estate-analysis/blob/main/Pictures/breno-assis-r3WAWU5Fi5Q-unsplash.jpeg)
*Photo by <a href="https://unsplash.com/@brenoassis?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText">Breno Assis</a> on <a href="/s/photos/house?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText">Unsplash</a>*

With the increasing inflation rate and historical low mortgage rate, real estate becomes a popular choice for investment. Among the big cities in US, Seattle is one with high potential. 

To help house buyers distinguish opportunities with high potential, and house sellers estimate the value of their house by themselves, I built a web-based prediction model of home values in Seattle. I incoporated data visualization and machine learning into a web application, on which users could explore the general conditions of real estate market in Seattle, and acquire the estimated price of a specific house. 

The product consists of two parts:

## 1. Visualization of Home Values in Seattle

I made interactive visualizations and generated a web application by Streamlit and Heroku:[click here](https://capstone-baiyan.herokuapp.com/)

Data source: 
- [Zillow Housing Data](https://www.zillow.com/research/data/)

Data Visualization Packages:
- Plotly
- Streamlit

## 2. House Price Prediction

I built a XGBoost Regression model to predict house price based on the features of house and mortgage rate.

Data source: 
- [Kaggle House Sales in King County Dataset](https://www.kaggle.com/harlfoxem/housesalesprediction)

Machine Learning Packages:
- [XGBoost](https://xgboost.readthedocs.io/en/latest/index.html)
- [Hyperopt](http://hyperopt.github.io/hyperopt/)

This model predicts the house price with percentage error as 11%.

