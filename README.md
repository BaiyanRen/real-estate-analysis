# Analysis of Home Values in Seattle

![Houses](https://github.com/BaiyanRen/real-estate-analysis/blob/main/Pictures/breno-assis-r3WAWU5Fi5Q-unsplash.jpeg)
*Photo by <a href="https://unsplash.com/@brenoassis?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText">Breno Assis</a> on <a href="/s/photos/house?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText">Unsplash</a>*

People who left their hometown and built the career in a new city, like me, would start thinking about settling down at some point. Choose a state, a city, a neighbor, then a life. But, when we are talking about home, what are we talking about? Family, warmth, dogs, cats, and of course, the "house" made by bricks and woods. 

Home is a special product in our life. Its value is dependent on so many factors, including but not limited to, size, neighbor, building material, interest rate, economy. I divide them into three groups: The first one contains the property of the home itself; the second one contains the features of the local area; the third one contains loan interest rates and economical situations, which exibit global impact on the real estate market. 

Seattle is a city with dynamic. It is also a good place for real estate investment. To help investors distinguish opportunities with high potential, I incoporated data visualization and machine learning into a web application, on which users could explore the general conditions of real estate market in Seattle, and acquire the estimated price of their home-of-interest. The comparison of the estimated price and the listing price would be informative and useful for investors before they making the decision.

The product consists of two parts:

## 1. Visualization of Home Values in Seattle

I made interactive visualizations and generated a web application by Streamlit and Heroku, which could be viewed [here](https://capstone-baiyan.herokuapp.com/)

Data source: [Zillow Housing Data](https://www.zillow.com/research/data/).


Packages:
- Plotly
- Streamlit

## 2. House Price Prediction

I built a LightGBM Regression model to predict house price based on the features of house.

Data source: [Kaggle competition](https://www.kaggle.com/c/house-prices-advanced-regression-techniques) (House Prices - Advanced Regression Techniques) using the [Ames Home Dataset](http://jse.amstat.org/v19n3/decock.pdf)


(I am currently updating and incoporating the house price prediction model into the web app.)
