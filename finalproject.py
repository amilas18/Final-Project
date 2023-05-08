'''
Name: Alex Milas
Course: CS230-5
Date 5/5/2023
Assignment: Final Project
URL:
Purpose: The purpose of this assignment is to analyze a set of data and create charts and maps that are accessible to outside users. For my data set,
I analyzed data on roller coasters across the US. With this data set, I created several maps and charts to give users a breakdown of some useful
and interesting information regarding roller coasters across the country. My website can be utilized to help users plan their next family
vacation around which roller coasters are most tailored to what they are looking for. Overall, this program is a fun and interesting way
to analyze data and make it useful to individuals interested in roller coasters.
Websites used for assistance: https://docs.streamlit.io/library/api-reference/charts/st.pydeck_chart
https://favtutor.com/blogs/list-to-dataframe-python#:~:text=We%20can%20use%20the%20DataFrame,of%20the%20Pandas%20DataFrame%20class
https://docs.mapbox.com/api/maps/styles/
https://discuss.streamlit.io/t/how-to-draw-pie-chart-with-matplotlib-pyplot/13967
'''

#software needed to complete this program
import streamlit as st
import pydeck as pdk
import pandas as pd
import random as rd
from PIL import Image
import matplotlib.pyplot as plt
st.set_option('deprecation.showPyplotGlobalUse', False)

#This is the path that will be referenced throughout the program in order to call the file that I will be analyzing
path = "C:/Users/alexm/OneDrive - Bentley University/Bentley/Junior/Spring 2023/CS230/"

us_coasters = pd.read_csv(path + "RollerCoasters-Geo.csv")
us_coasters.rename(columns={"Latitude":"lat","Longitude":"lon"}, inplace=True)

#Default home page that opens when you run streamlit. The home page gives a brief overview of what the website is about as well as some pitcures of roller coasters
def home_page(us_coasters):
    st.title("Roller Coasters in the United States!")

    st.write("Take a look at some of the most popular roller coasters across the country!")
    st.write(us_coasters)

    first_image = Image.open("C:/Users/alexm/OneDrive - Bentley University/Bentley/Junior/Spring 2023/CS230/roller_coaster_1.jpg")
    st.image(first_image, width=1000)
    second_image = Image.open("C:/Users/alexm/OneDrive - Bentley University/Bentley/Junior/Spring 2023/CS230/roller_coaster_2.jpg")
    st.image(second_image, caption="Europe's fastest roller coaster", width=1000)

#These are the names of the different pages within the website that users have access to
webpages = ["Home Page","Basic Roller Coaster Map", "Detailed Roller Coaster Map", "Roller Coaster Maps Based on Specific Criteria", "US roller coaster data and charts"]

#This page gives a very basic plot map of roller coasters across the US. It does not provide much detail, but it can show users if there are any roller coasters in their area
def roller_coasters_1(us_coasters):
    st.title("Basic Map of Roller Coasters in the US")
    us_coasters.rename(columns={"Latitude": "lat", "Longitude": "lon"}, inplace=True)
    st.map(us_coasters)

#This page is more interactive as it also displays a map of roller coasters across the US. However, this map gives the user the ability to hover over each plot point on the map and gather detailed information about the roller coasters.
def roller_coasters_2(us_coasters):
    st.title(
        "Detailed Map of Roller Coasters in the US")
    us_coasters.dropna(inplace=True)
    view_state = pdk.ViewState(latitude=us_coasters['lat'].mean(), longitude=us_coasters['lon'].mean(), zoom=4, pitch=0)
    layer = pdk.Layer('ScatterplotLayer', data=us_coasters, get_position='[lon, lat]', get_radius=40000,
                      get_color=[rd.randint(0, 255)], pickable=True)
    tool_tip = {"html": "<b>Name: {Coaster}</b> <br/> <b>Location: {Park}<b> <br/> <b>Opened: {Year_Opened}",
                "style": {"backgroundColor": "yellow",
                          "color": "black"}}
    coaster_map = pdk.Deck(map_style='mapbox://styles/mapbox/navigation-day-v1', initial_view_state=view_state,
                           layers=[layer], tooltip=tool_tip)
    st.pydeck_chart(coaster_map)
#This page allows for user input and provides user with three separate maps they can use to gather more information. Users are given the option select a specific type of roller coaster and the map will display only those roller coasters.
def roller_coasters_3(us_coasters):
    st.title(
        "Detailed Map of Roller Coasters in the US")
    us_coasters.dropna(inplace=True)

    type_list = []

    for i in us_coasters.Type:
        if i.lower().strip() not in type_list:
            type_list.append(i.lower().strip())

    sub_type_list = []

    for i in type_list:
        sub_type = us_coasters[us_coasters["Type"].str.lower().str.strip() == i]
        sub_type_list.append(sub_type)

    map_layer = []

    for sub_type in sub_type_list:
        layer = pdk.Layer('ScatterplotLayer', data=sub_type, get_position='[lon, lat]', get_radius=40000,
                          get_color=[rd.randint(0, 255)], pickable=True)
        map_layer.append(layer)
    tool_tip = {"html": "<b>Name: {Coaster}</b> <br/> <b>Location: {Park}<b> <br/> <b>Opened: {Year_Opened} </br> <b>Type: {Type}<b>",
                "style": {"backgroundColor": "yellow",
                          "color": "black"}}
    view_state = pdk.ViewState(latitude=us_coasters['lat'].mean(), longitude=us_coasters['lon'].mean(), zoom=4, pitch=0)

    type_list.insert(0,"")

    selected_type = st.text_input("Please enter a type of roller coaster (wooden or steel)")

    for i in range(len(type_list)):
        if selected_type.lower().strip() == type_list[i]:
            if i == 0:
                coaster_map = pdk.Deck(
                    map_style='mapbox://styles/mapbox/navigation-day-v1', initial_view_state=view_state,
                    layers=[map_layer], tooltip=tool_tip)
            else:
                coaster_map = pdk.Deck(
                    map_style = 'mapbox://styles/mapbox/navigation-day-v1', initial_view_state = view_state,
                layers = [map_layer[i-1]], tooltip = tool_tip)

            st.pydeck_chart(coaster_map)
#This function also ties to the previous page as it allows users to enter a specific design type of the roller coaster, and it also displays a map of the roller coasters with the given design.
def roller_coasters_4(us_coasters):
    us_coasters.dropna(inplace=True)

    design_list = []

    for i in us_coasters.Design:
        if i not in design_list:
            design_list.append(i)

    sub_design_list = []

    for i in design_list:
        sub_design = us_coasters[us_coasters["Design"] == i]
        sub_design_list.append(sub_design)

    map_layer = []

    for sub_design in sub_design_list:
        layer = pdk.Layer('ScatterplotLayer', data=sub_design, get_position='[lon, lat]', get_radius=40000,
                          get_color=[rd.randint(0, 255)], pickable=True)
        map_layer.append(layer)
    tool_tip = {
        "html": "<b>Name: {Coaster}</b> <br/> <b>Location: {Park}<b> <br/> <b>Opened: {Year_Opened} </br> <b>Design: {Design}<b>",
        "style": {"backgroundColor": "yellow",
                  "color": "black"}}
    view_state = pdk.ViewState(latitude=us_coasters['lat'].mean(), longitude=us_coasters['lon'].mean(), zoom=4, pitch=0)

    design_list.insert(0, "")

    selected_design = st.selectbox("Please select a design", design_list)

    for i in range(len(design_list)):
        if selected_design == design_list[i]:
            if i == 0:
                coaster_map = pdk.Deck(
                    map_style='mapbox://styles/mapbox/navigation-day-v1', initial_view_state=view_state,
                    layers=[map_layer], tooltip=tool_tip)
            else:
                coaster_map = pdk.Deck(
                    map_style='mapbox://styles/mapbox/navigation-day-v1', initial_view_state=view_state,
                    layers=[map_layer[i - 1]], tooltip=tool_tip)

            st.pydeck_chart(coaster_map)
#This is the last function that ties to the page mentioned above. This function allows users to select if they want a roller coaster with inversions (goes upside-down) and then it displays roller coasters with those criteria.
def roller_coasters_5(us_coasters):
    us_coasters.dropna(inplace=True)

    inversions_list = []

    for i in us_coasters.Inversions:
        if i not in inversions_list:
            inversions_list.append(i)

    sub_inversions_list = []

    for i in inversions_list:
        sub_inversions = us_coasters[us_coasters["Inversions"] == i]
        sub_inversions_list.append(sub_inversions)

    map_layer = []

    for sub_inversions in sub_inversions_list:
        layer = pdk.Layer('ScatterplotLayer', data=sub_inversions, get_position='[lon, lat]', get_radius=40000,
                          get_color=[rd.randint(0, 255)], pickable=True)
        map_layer.append(layer)
    tool_tip = {
        "html": "<b>Name: {Coaster}</b> <br/> <b>Location: {Park}<b> <br/> <b>Opened: {Year_Opened} </br> <b>Number of Inversions: {Num_of_Inversions}<b>",
        "style": {"backgroundColor": "yellow",
                  "color": "black"}}
    view_state = pdk.ViewState(latitude=us_coasters['lat'].mean(), longitude=us_coasters['lon'].mean(), zoom=4, pitch=0)

    inversions_list.insert(0, "")

    selected_inversions = st.radio("Do you want a roller coaster with inversions?", inversions_list)

    for i in range(len(inversions_list)):
        if selected_inversions == inversions_list[i]:
            if i == 0:
                coaster_map = pdk.Deck(
                    map_style='mapbox://styles/mapbox/navigation-day-v1', initial_view_state=view_state,
                    layers=[map_layer], tooltip=tool_tip)
            else:
                coaster_map = pdk.Deck(
                    map_style='mapbox://styles/mapbox/navigation-day-v1', initial_view_state=view_state,
                    layers=[map_layer[i - 1]], tooltip=tool_tip)

            st.pydeck_chart(coaster_map)
#This is the last page of the website and it shows three different charts, two bar charts and a pie chart that display interesting information regarding the roller coasters in the given data set
def roller_coasters_6(us_coasters):
    st.title("Charts of Specific Roller Coaster Statistics")
    us_coasters = pd.read_csv(path + "RollerCoasters-Geo.csv", index_col="Coaster")
    coaster_speed = us_coasters.drop(columns=["State", "Age_Group", "Park", "City", "Type", "Max_Height", "Design", "Year_Opened", "Latitude", "Longitude", "Drop", "Length", "Duration", "Inversions", "Num_of_Inversions"])
    top_speed = coaster_speed[coaster_speed.Top_Speed >75]
    updated_speed = top_speed["Top_Speed"].sort_values(ascending=False)
    updated_speed.plot(kind = "bar", color = ['lightblue', 'purple'])
    plt.xlabel("Coaster Names")
    plt.ylabel("Maximum Speed")
    plt.title("Roller Coasters with a top speed of greater than 75 miles per hour")
    st.pyplot()

    tall_coasters = us_coasters.drop(columns=["Age_Group", "Park", "City", "State","Type", "Design", "Year_Opened", "Latitude", "Longitude", "Top_Speed", "Length", "Duration", "Inversions", "Num_of_Inversions"])
    high_coasters = tall_coasters[(tall_coasters.Max_Height >125)&(tall_coasters.Drop>200)]
    final_height = high_coasters["Max_Height"].sort_values(ascending=True)
    final_height.plot(kind = "bar", color = ['orange', 'green'])
    plt.xlabel("Coaster Names")
    plt.ylabel("Maximum Height")
    plt.title("Roller Coasters with a maximum height of greater than 125 feet and a drop of greater than 200 feet")
    st.pyplot()

    st.title("Breakdown of what percentage of all the roller coasters opened in which time period")
    old_coasters = us_coasters.drop(columns=["Length", "Type", "Age_Group", "Park", "City", "State", "Design", "Latitude", "Longitude", "Top_Speed", "Max_Height", "Drop", "Duration", "Inversions", "Num_of_Inversions"])
    old_coasters1 = old_coasters[(old_coasters.Year_Opened >= 1915) & (old_coasters.Year_Opened <= 1935)]
    old_coasters2 = old_coasters[(old_coasters.Year_Opened > 1935) & (old_coasters.Year_Opened <= 1955)]
    old_coasters3 = old_coasters[(old_coasters.Year_Opened > 1955) & (old_coasters.Year_Opened <= 1975)]
    old_coasters4 = old_coasters[(old_coasters.Year_Opened > 1975) & (old_coasters.Year_Opened <= 1995)]
    old_coasters5 = old_coasters[old_coasters.Year_Opened > 1995]
    count0 = old_coasters.count()
    count1 = old_coasters1.count()
    count2 = old_coasters2.count()
    count3 = old_coasters3.count()
    count4 = old_coasters4.count()
    count5 = old_coasters5.count()
    percentage1 = count1/count0 *100
    percentage2 = count2/count0 *100
    percentage3 = count3/count0 *100
    percentage4 = count4/count0 *100
    percentage5 = count5/count0 *100
    percentage_breakdown = [percentage1, percentage2, percentage3, percentage4, percentage5]
    percentage_df = pd.DataFrame(percentage_breakdown)
    years_percentage = percentage_df["Year_Opened"]
    percentages = []
    for i in years_percentage:
        percentages.append(i)
    labels = '1915-1935', '1936-1955', '1956-1975', '1976-1995', '1995-Present'

    lbl1, num1 = plt.subplots()
    num1.pie(percentages, labels=labels, autopct="%.2f%%")
    st.pyplot()

#This is the sidebar displayed on the side of the website where users can toggle between specific pages
st.sidebar.write("Please select a webpage you would like to navigate to:")
selected_webpage = st.sidebar.radio("Please select one of the following", webpages)

def webpage_selection(selected_webpage):
    if selected_webpage == "Home Page":
        home_page(us_coasters)
    elif selected_webpage == "Basic Roller Coaster Map":
        roller_coasters_1(us_coasters)
    elif selected_webpage == "Detailed Roller Coaster Map":
        roller_coasters_2(us_coasters)
    elif selected_webpage == "Roller Coaster Maps Based on Specific Criteria":
        roller_coasters_3(us_coasters)
        roller_coasters_4(us_coasters)
        roller_coasters_5(us_coasters)
    else:
        roller_coasters_6(us_coasters)

webpage_selection(selected_webpage)
