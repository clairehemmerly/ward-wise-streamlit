import streamlit as st
import pandas as pd
import plotly.express as px
import json

# st.set_page_config(layout="wide")

#creat functions that will cache selected data
@st.cache_data
def load_data():
    print("loading data")
    cat_data = pd.read_csv('spending_by_category.csv')
    max_data = pd.read_csv('max_spend.csv')

    #load ward geometries
    f = open('Boundaries - Wards (2015-2023).geojson')
    geometry = json.load(f)
    return (cat_data, max_data, geometry)

@st.cache_data
def year_select(year):
    print('filtering data by year')
    max_spend = max_data[max_data['year'] == year]
    return max_spend

@st.cache_data
def category_select(year, category):
    print('filtering data by year and cat')
    cat_spend = cat_data.loc[(cat_data['year'] == year) & (cat_data['category'] == category)]
    return cat_spend


cat_data, max_data, geometry = load_data()


st.title('Ward-Wise')
st.write('Every year, Chicago alderpersons get $1.5 million to spend at their discretion on capital improvements on their ward.')
option = st.radio('Select data to display:', ['Maximum spending by year', 'Ward spending by category'])

with st.sidebar:
    url = "https://jonathanortega2023.github.io/alderman-spending/#/"
    st.write("To see a break down of spending in your ward go [here](%s)!" % url)
    st.write("Don't know you ward number? Enter your address below")
    st.components.v1.iframe(
    src="https://gisapps.chicago.gov/WardGeocode/?embed=true",
    height=450,
    width=400)


#create columns for layout
# col1, col2 = st.columns(2)

# with col1:
if option == "Maximum spending by year":
    st.write('Choose a year to see where each ward spent the most money')

    year = st.selectbox(
        'Year',
        (2022, 2021, 2020, 2019))
    
    #filter data by drop down selections
    max_spend = year_select(year)

    #create figure
    fig = px.choropleth(max_spend, geojson=geometry, locations='ward', featureidkey="properties.ward",
                            color='category',
                            labels={'perc_spending': "Percent of Annual Spending"},
                            hover_data={'perc_spending':':.1f'},
                            height=300
                            )

    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

    #show figure
    st.plotly_chart(fig, use_container_width=True)

# with col2:
if option == "Ward spending by category":
    st.write('Select a category to see how much was spent on it each year')

    col1, col2 = st.columns(2)

    with col1:
    #create drop down to select category
        categories = cat_data['category'].unique()
        category = st.selectbox(
            'Spending Category',
            (categories))  

    with col2:
        year = st.selectbox(
        'Year',
        (2022, 2021, 2020, 2019))  
    
    #filter data by drop down selections
    plot_data = category_select(year, category)

    #create figure
    fig = px.choropleth(plot_data, geojson=geometry, locations='ward', featureidkey="properties.ward",
                            color='perc_spending',
                            color_continuous_scale="gnbu",
                            labels={'perc_spending': "Percent of Annual Spending"},
                            hover_data={'perc_spending':':.1f'},
                            height=300
                            )
    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

    #show figure
    st.plotly_chart(fig, use_container_width=True)


