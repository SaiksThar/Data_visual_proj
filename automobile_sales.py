# -*- coding: utf-8 -*-
"""
Created on Tue Sep 19 23:13:17 2023

@author: saika
"""

import numpy as np
import pandas as pd

import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns
import folium
import pandas as pd

df = pd.read_csv('historical_automobile_sales.csv')
print('Data downloaded and read into a dataframe!')
print(df.columns)
describ = df.describe()


df_line_mean = df.groupby('Year')['Automobile_Sales'].mean()
df_line_sum = df.groupby('Year')['Automobile_Sales'].sum()

### Task 1.1  simple plot
df_line_mean.plot(kind='line',xlabel = 'years', ylabel = 'Sale Volumes', title ='Sale vol: over year', figsize=(10,6) )
plt.plot()

### with xticks and legends
years = df['Year'].unique().tolist()
plt.figure(figsize=(10, 6))
df_line_mean.plot(kind = 'line')
plt.xticks(years, rotation = 75)
plt.xlabel('years')
plt.ylabel('Sale Volumes')
plt.title('Sale vol: over year')
plt.text(1982, 650, '1981-82 Recession') # plt.text( x,y, 'Text to display') x,y are the coordinates on the plots
plt.legend()
plt.show()

### Task 1.2 
df_car_type = df.groupby(['Year','Vehicle_Type'],as_index = False)['Automobile_Sales'].sum()
df_car_type.set_index('Year',inplace = True)
df_car_type = df_car_type.groupby('Vehicle_Type')['Automobile_Sales']

for Vehicle_Type in df_car_type:
    print(Vehicle_Type)

df_car_type.plot(kind='line',xlabel = 'years', ylabel = 'Sale Volumes', title ='Sale vol: over year', figsize=(20,6))
plt.xticks(years, rotation = 90)
plt.legend()
plt.plot()

# Inference: From this plot, we can understand that during recession period, the sales for 'Sports type vehicles' declined because of the high cost of the vehicle.
# while sales of the superminicar and smallfamilycar increased.

### Task 1.3

df_recession = df.groupby('Recession')['Automobile_Sales'].mean().reset_index()
plt.figure(figsize=(10,6))
sns.barplot(x ='Recession',y = 'Automobile_Sales', hue = 'Recession', data = df_recession)
plt.xlabel('Recession')
plt.ylabel('Automobile Sales')
plt.title('Average Automobile Sales during Recession and Non-Recession')
plt.xticks(ticks=[0,1], labels = ['Non-Recession','Recession'])
plt.legend()
plt.plot()

rec_data = df[df['Recession']==1]

df_recdata =df.groupby(['Recession','Vehicle_Type'])['Automobile_Sales'].mean().reset_index()
plt.figure(figsize=(10,6))
sns.barplot(x ='Recession',y = 'Automobile_Sales', hue = 'Vehicle_Type', data = df_recdata)
plt.xlabel('Recession')
plt.ylabel('Automobile Sales')
plt.title('Average Automobile Sales during Recession and Non-Recession')
plt.xticks(ticks=[0,1], labels = ['Non-Recession','Recession'])
plt.legend()
plt.plot()

# Inference
# From this plot, we can understand that there is a drastic decline in the overall sales of the automobiles during recession.
# However, the most affected type of vehicle is executivecar and sports

### Task 1.4

rec_data = df[df['Recession']==1]
non_rec_data = df[df['Recession']==0]

# # creating figure
fig = plt.figure(figsize = (14,6))

# # Create different axes for subploting
ax0 = fig.add_subplot(1,2,1)
ax1 = fig.add_subplot(1,2,2)

# # 1st axis plot for recession
sns.lineplot(x = 'Year', y ='GDP', data = rec_data,label = 'Recession', ax = ax0)
ax0.set_xlabel('Year')
ax0.set_ylabel('GDP')
ax0.set_title('GDP Variation during Recession Period')

# # 2nd axis plot for non-recession
sns.lineplot(x ='Year', y ='GDP', data = non_rec_data, label = 'Non-Recession', ax = ax1)
ax1.set_xlabel('Year')
ax1.set_ylabel('GDP')
ax1.set_title('GDP Variation during Non-Recession Period')

plt.tight_layout()
plt.plot()

# alternative ways
plt.subplot(1, 2, 1)
sns.lineplot(x = 'Year', y ='GDP', data = rec_data,label = 'Recession')
plt.xlabel('Year')
plt.ylabel('GDP')
plt.legend()
#subplot 1
plt.subplot(1, 2, 2)
sns.lineplot(x ='Year', y ='GDP', data = non_rec_data, label = 'Non-Recession')
plt.xlabel('Year')
plt.ylabel('GDP')
plt.legend()
    
plt.tight_layout()
plt.show()

### Task 1.5

non_rec_data = df[df['Recession']==0]

s=non_rec_data['Seasonality_Weight'] #for bubble effect
plt.figure(figsize=(10,6))
sns.scatterplot( data = non_rec_data, x='Month', y = 'Automobile_Sales',size= s)
plt.xlabel('Month')
plt.ylabel('Automobile Sales')
plt.plot()

# Inference
# From this plot, it is evident that seasonality has not affected on the overall sales. However, there is a drastic raise in sales in the month of April

### Task 1.6

rec_data = df[df['Recession']==1]

plt.scatter(rec_data['Consumer_Confidence'], rec_data['Automobile_Sales'])
    
plt.xlabel('Consumer_Confidence')
plt.ylabel('....Automobile_Sales...')
plt.title('..........')
plt.show()

sns.scatterplot(data= rec_data, x = 'Price',y ='Automobile_Sales', label ='Price')
plt.title(' Price vs Automobile Sales')
plt.xlabel('Price')
plt.ylabel('Automobile sale units')
plt.plot()

## Task 1.7
rec_data     = df[df['Recession']==1]
non_rec_data = df[df['Recession']==0]

rec_exp = rec_data['Advertising_Expenditure'].sum()
non_rec_exp = non_rec_data['Advertising_Expenditure'].sum()

size = [rec_exp,non_rec_exp]
labels = ['Recession', 'Non-Recession']
plt.figure(figsize=(10,6))
plt.pie(size ,labels = labels,  autopct='%1.1f%%',startangle=90)
plt.title('Advertising Expenditure during Recession and Non-Recession Periods')
plt.plot()

## Task 1.8
df_car = rec_data.groupby('Vehicle_Type')['Advertising_Expenditure'].sum()

label = df_car.index
data_car = df_car.values

plt.figure(figsize = (10,6))
plt.pie(data_car,labels = label, autopct= '%1.1f%%', startangle=90)
plt.title('Advertising Expenditure by type of cars during Recession ')
plt.plot()

## Task 1.9 count plot ### 
 
plt.figure(figsize=(20,6))

sns.countplot(data = rec_data, x ='unemployment_rate', hue = 'Vehicle_Type')
plt.ylabel('Count')
plt.title('Effect of Unemployment Rate on Vehicle Type and Sales')
plt.legend(loc='upper right')
plt.show()

# Inference  During recession, buying pattern changed, the sales of low range vehicle like superminicar,smallfamilycar and Mediumminicar


path = 'https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/us-states.json'

# filename = "us-states.json"

  # Filter the data for the recession period and specific cities
recession_data = df[df['Recession'] == 1]

    # Calculate the total sales by city
sales_by_city = recession_data.groupby('City')['Automobile_Sales'].sum().reset_index()

    # Create a base map centered on the United States
map1 = folium.Map(location=[37.0902, -95.7129], zoom_start=4)

    # Create a choropleth layer using Folium
choropleth = folium.Choropleth(
        geo_data= path,  # GeoJSON file with state boundaries
        data=sales_by_city,
        columns=['City', 'Automobile_Sales'],
        key_on='feature.properties.name',
        fill_color='YlOrRd',
        fill_opacity=0.7,
        line_opacity=0.2,
        legend_name='Automobile Sales during Recession'
    ).add_to(map1)


    # Add tooltips to the choropleth layer
choropleth.geojson.add_child(
        folium.features.GeoJsonTooltip(['name'], labels=True)
    )

    # Display the map
map1.save('US_Car_sales.html')