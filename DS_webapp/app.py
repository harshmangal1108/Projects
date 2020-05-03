import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk  ## for interactive map plot
data_url=("mvc.csv")
st.title("Motor Vehicle Collision in  NY 🔥😈")
st.markdown("This app is streamlit dashborad that can " "be used to analyse MVC data of NY city ")
##using function cache to not perform computation everytime it reruns
@st.cache(persist=True)
def load_data(nrows):
    data=pd.read_csv(data_url,nrows=nrows,parse_dates=[['CRASH_DATE','CRASH_TIME']])
    data.dropna(subset=['LATITUDE','LONGITUDE'],inplace=True) ## this is droping of NA values across longitude and lattitude
    lowercase=lambda x: str(x).lower()
    data.rename(lowercase ,axis='columns',inplace=True)
    data.rename(columns={'crash_date_crash_time':'date/time'},inplace=True)
    return data


## calling funcn and loading only 100000 
data=load_data(20000)
original_data=data
st.header("Where are most people injured in NYC")
injured=st.slider("Number of Persons injured",0,19)
st.map(data.query("injured_persons >=@injured")[["latitude","longitude"]].dropna(how="any"))
##### Filtereing Data and Interactive table
st.header("How Many Collision occur during a given time of day")
##using DropDown
#hour=st.selectbox("Hour to look at",range(0,24),1)  ##1 is seprated by diff 1
#hour=st.sidebar.slider("Hour to look at",0,24) >sidebar will move slider to left navigation bar
hour=st.slider("Hour to look at",0,23)
data=data[data['date/time'].dt.hour==hour]
midpoint=(np.average(data['latitude']),np.average(data['longitude'])) ## for particular view ex newyork city
st.markdown("Vehicle Collision bw %i:00 and %i:00" %(hour,(hour+1)%24))
st.write(pdk.Deck(
    map_style="mapbox://styles/mapbox/light-v9",
    initial_view_state={
        "latitude":midpoint[0],
        "longitude":midpoint[1],
        "zoom":11,
        "pitch":50,
    },### till here it was empty map
    layers=[
        pdk.Layer(
            "HexagonLayer",
            data=data[['date/time','latitude','longitude']],
            get_position=['longitude','latitude'],
            radius=100,
           extruded=True, ##it shows that upwards bar comming
            pickable=True,
            elevation_scale=4,
            elevation_range=[0,2000],
        ),
    ],
))
import plotly.express as px
st.subheader("Breakdown by minute %i:00 and %i:00"%(hour,(hour+1)%24))
## filtered DAta
filtered=data[(data['date/time'].dt.hour>=hour) & (data['date/time'].dt.hour<(hour+1))]
hist=np.histogram(filtered['date/time'].dt.minute,bins=60,range=(0,60))[0]
chart_data=pd.DataFrame({'minute':range(60),'crashes':hist})
fig=px.bar(chart_data,x='minute',y='crashes',hover_data=['minute','crashes'],height=400)
st.write(fig)

st.header("Top 5 dangerous streets by affected type ")
select=st.selectbox('Affected type of People',['Pedestrains','Cyclists','Motorists'])
if select == 'Pedestrians':
    st.write(original_data.query("injured_pedestrians >= 1")[["on_street_name", "injured_pedestrians"]].sort_values(by=['injured_pedestrians'], ascending=False).dropna(how="any")[:5])

elif select == 'Cyclists':
    st.write(original_data.query("injured_cyclists >= 1")[["on_street_name", "injured_cyclists"]].sort_values(by=['injured_cyclists'], ascending=False).dropna(how="any")[:5])

else:
    st.write(original_data.query("injured_motorists >= 1")[["on_street_name", "injured_motorists"]].sort_values(by=['injured_motorists'], ascending=False).dropna(how="any")[:5])
## write data
if st.checkbox("show data ",False):
    st.subheader('RAW DATA')
    st.write(data)
