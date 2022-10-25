import pandas as pd
import streamlit as st

from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

header = st.container()
dataset = st.container()
features = st.container()
model_training = st.container()

@st.cache
def get_data(filename):
    return pd.read_parquet(filename)

with header:
    st.title("Welcome to my aweone data science project!")
    st.text('In this project, I look into transactions of taxis in NYC...')

with dataset:
    st.header("NYC taxi driver dataset")
    st.text("I found this dataset on blablabla.com, ...")
    
    taxi_data = get_data("data/yellow_tripdata.parquet")
    st.write(taxi_data.head())
    
    st.subheader("Pick-up location ID distribution on the NYC dataset")
    pulocation_dist = pd.DataFrame(taxi_data["PULocationID"].value_counts()).head(50)
    st.bar_chart(pulocation_dist)

with features:
    st.header("The feature I created")
    
    st.markdown("* **first feature: ** I created this feature becaus of this... I calculated it using this logic")
    st.markdown("* **second feature: ** I created this feature becaus of this... I calculated it using this logic")
    
with model_training:
    st.header("Time to train the model!")
    st.text("Here you get to choose the hyperparameters of the model and see \nhow the perfomance changes!")
    
    sel_col, disp_col = st.columns(2)
    max_depth = sel_col.slider("What should be the max_depth of the model?", min_value=10, max_value=100, value=20, step=10)
    n_estimators = sel_col.selectbox("How many trees should there be?", options=[100, 200, 300, "No limit"], index=0)    
    
    sel_col.text("Here is a list of features in my data: ")
    sel_col.write(taxi_data.columns)
    input_feature = sel_col.text_input("Which feature should be used as the input feature?", value="PULocationID")
    
    if n_estimators == "No limit":
        regr = RandomForestRegressor(max_depth=max_depth)
    else:
        regr = RandomForestRegressor(max_depth=max_depth, n_estimators=n_estimators)
    
    X= taxi_data[[input_feature]]
    y = taxi_data[['trip_distance']]
    
    regr.fit(X, y.values.ravel())
    prediction = regr.predict(y)
    
    disp_col.subheader('Mean Absolute Error (MAE): ')
    disp_col.write(mean_absolute_error(y, prediction))
    disp_col.subheader('Mean Squared Error (MSE): ')
    disp_col.write(mean_squared_error(y, prediction))
    disp_col.subheader('R-squred: ')
    disp_col.write(r2_score(y, prediction))