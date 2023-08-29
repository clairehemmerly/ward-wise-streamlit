import streamlit as st
import pandas as pd
import plotly.express as px
import json

#load spending data
data = pd.read_csv('spending_by_category.csv')

#load ward geometries
f = open('Boundaries - Wards (2015-2023).geojson')
geometry = json.load(f)

st.set_page_config(layout="wide")

st.title('Ward-Wise')
st.caption('Every year, Chicago alderpersons get $1.5 million to spend at their discretion on capital improvements on their ward.')
url = "https://jonathanortega2023.github.io/alderman-spending/#/"
st.write("To see a break down of spending in your ward go [here](%s)!" % url)

#create columns for layout
col1, col2 = st.columns(2)

with col1:
    st.header('Wards Spent the Most on...')

    year = st.selectbox(
        'Year',
        (2022, 2021, 2020, 2019))
    
    #filter data by drop down selections
    year_data = data[data['year'] == year]
    max_spend = year_data.sort_values('perc_spending', ascending=False).drop_duplicates(['ward'])

    #create figure
    fig2 = px.choropleth(max_spend, geojson=geometry, locations='ward', featureidkey="properties.ward",
                            color='category',
                            labels={'perc_spending': "Percent of Annual Spending"},
                            hover_data={'perc_spending':':.1f'}
                            )

    fig2.update_geos(fitbounds="locations", visible=False)
    fig2.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

    #show figure
    st.plotly_chart(fig2, use_container_width=True)

with col2:
    st.header('By Category')

    #create drop down to select category
    categories = data['category'].unique()
    category = st.selectbox(
        'Spending Category',
        (categories))    
    
    #create drop down to select year
    # year = st.selectbox(
    #     'Year',
    #     (2022, 2021, 2020, 2019))

    #filter data by drop down selections
    plot_data = data.loc[(data['year'] == year) & (data['category'] == category)]

    #create figure
    fig = px.choropleth(plot_data, geojson=geometry, locations='ward', featureidkey="properties.ward",
                            color='perc_spending',
                            color_continuous_scale="gnbu",
                            labels={'perc_spending': "Percent of Annual Spending"},
                            hover_data={'perc_spending':':.1f'}
                            )
    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

    #show figure
    st.plotly_chart(fig, use_container_width=True)


