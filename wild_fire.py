# -*- coding: utf-8 -*-
"""
Created on Tue Sep 12 00:03:07 2023

@author: saika
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


df = pd.read_csv('Historical_Wildfires.csv')
# print(df.dtypes)

# initially, Date in df is object, need to convert into date_time format

import datetime as dt
## creating 'Year' column and converting date into datetime format put the year into the new column
year_data = pd.to_datetime(df['Date']).dt.year
month_data = pd.to_datetime(df['Date']).dt.month

df.insert(1,'Month',month_data)
df.insert(2,'Year',year_data)

## estimated fire area over time (year)
fire_area = df.groupby(df['Estimated_fire_area']).sum()

##filter out the mean of estimated fire area

'''Task 1.1 lineplot with year '''

#### lineplot with px.line

df_fire_area_ot = df.groupby('Year')['Estimated_fire_area'].mean().to_frame()
import plotly.graph_objects as go
import plotly.offline as pyo
import plotly.express as px

fig_line = px.line(x= df_fire_area_ot.index, y = df_fire_area_ot['Estimated_fire_area'])
fig_line.update_layout( title = 'Estimated Fire Area over year', xaxis_title='Year', yaxis_title='Average Fire area (km²)')
pyo.plot(fig_line)


'''Task 1.2 lineplot with month, year '''
### lineplot with regular plot
plt.figure(figsize=(12, 6))

df_lineplot=df.groupby(['Year','Month'])['Estimated_fire_area'].mean()
print(df_lineplot.dtypes)
df_lineplot.plot(x = df_lineplot.index, y = df_lineplot.values )
plt.xlabel('Year, Month')
plt.ylabel('Average Estimated Fire Area (km²)')
plt.title('Estimated Fire Area over Time')
plt.show()

'''Task 1.3 barplot'''

#### barplot with px

df_region = df.groupby('Region')['Mean_estimated_fire_brightness'].mean().to_frame()
# # df['Region'].unique()
import plotly.graph_objects as go
import plotly.offline as pyo
import plotly.express as px

### barplot 1 : px
fig_line = px.bar(x= df_region.index, y = df_region['Mean_estimated_fire_brightness'])
fig_line.update_layout( title = 'Estimated Fire Area over year', xaxis_title='Region', yaxis_title='Average Fire Brightness')
pyo.plot(fig_line)

import matplotlib.pyplot as plt
import seaborn as sns
import folium
df_region = df_region.squeeze()

## barplot 2
df_region.plot(kind = 'bar',x =df_region.index, y = df_region.values )
plt.xlabel('Region')
plt.ylabel('Mean Estimated Fire Brightness (Kelvin)')
plt.title('Distribution of Mean Estimated Fire Brightness across Regions')
plt.show()

## barplot 3 : sns
sns.barplot(data = df, x = 'Region', y = 'Mean_estimated_fire_brightness')
plt.xlabel('Region')
plt.ylabel('Mean Estimated Fire Brightness (Kelvin)')
plt.title('Distribution of Mean Estimated Fire Brightness across Regions')
plt.show()

'''Task 1.4 pie '''

### piechart 1: px
df_region = df.groupby('Region')['Count'].sum().to_frame()
df_region['Count'].plot(kind='pie',
                            figsize=(10,10),
                            autopct='%1.1f%%', # add in percentages
                            startangle=0,     # start angle 90° (Africa)
                            shadow=True)  
                            # pctdistance=1.5,      # the ratio between the pie center and start of text label
                            # explode = explode_list)
plt.title('Plot 1:Total',size=20)
plt.axis('equal') # Sets the pie chart to look like a circle.
plt.legend(labels=df_region.index, loc='upper left') 
plt.show()


### piechart 2: regular
plt.figure(figsize=(10,6))
plt.pie(df_region.squeeze(), labels = df_region.index, autopct= '%1.1f%%')
plt.title('Plot 2: ')
plt.axis('equal')
plt.show()

'''Task 1.5 Histogram'''
### hist 1
plt.figure(figsize = (10,6))
plt.hist(df['Mean_confidence'], bins= 20)
plt.xlabel('Mean Estimated Fire Brightness (Kelvin)')
plt.ylabel('Count')
plt.title('Histogram of Mean Estimated Fire Brightness')
plt.show()

## hist 2 : sns
sns.histplot(data=df, x='Mean_estimated_fire_brightness', hue='Region')
plt.show()

sns.histplot(data=df, x='Mean_estimated_fire_brightness', hue='Region', multiple='stack')
plt.show()

## hist 3
df['Mean_confidence'].plot(kind='hist',figsize=(10,6), bins = 20)
plt.show()

''' Task 1.6 Scatterplot'''

# sns.scatterplot(x=df['Mean_estimated_fire_radiative_power'], y = df['Mean_confidence'])
sns.scatterplot(data = df, x='Mean_estimated_fire_radiative_power', y = 'Mean_confidence')
plt.xlabel('Mean Estimated Fire Radiative Power (MW)')
plt.ylabel('Mean Confidence')
plt.title('Mean Estimated Fire Radiative Power vs. Mean Confidence')
plt.show()

plt.figure(figsize =(10,6))
plt.scatter(x = df['Mean_estimated_fire_radiative_power'], y = df['Mean_confidence'])
plt.xlabel('Mean Estimated Fire Radiative Power (MW)')
plt.ylabel('Mean Confidence')
plt.title('Mean Estimated Fire Radiative Power vs. Mean Confidence')
plt.show()
plt.show()


''' Task 1.7 folium map'''
import folium
aus_reg = folium.map.FeatureGroup()

region_data = {'region':['NSW','QL','SA','TA','VI','WA','NT'], 'Lat':[-31.8759835,-22.1646782,-30.5343665,-42.035067,-36.5986096,-25.2303005,-19.491411], 
               'Lon':[147.2869493,144.5844903,135.6301212,146.6366887,144.6780052,121.0187246,132.550964]}
reg=pd.DataFrame(region_data)

Aus_map = folium.Map(location=[-25, 135], zoom_start=4)

# loop through the region and add to feature group
for lat, lng, lab in zip(reg.Lat, reg.Lon, reg.region):
    aus_reg.add_child(
        folium.features.CircleMarker(
            [lat, lng],
            popup=lab,
            radius=5, # define how big you want the circle markers to be
            color='red',
            fill=True,
            fill_color='blue',
            fill_opacity=0.6
        )
    )
    
Aus_map.add_child(aus_reg)
Aus_map.save('Aus_map.html')