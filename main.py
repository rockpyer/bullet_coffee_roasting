#%%
import logging
import os
import time
import pandas as pd
from importlib import reload
from pathlib import Path
from pprint import pprint
from src.data_load import load_roasting_data
from src.data_cleanup import basic_cleanup, drop_intermediate_columns
import src.data_processing #***
from src.data_processing import deconstruct_temp_curves, develop_point_df, check_missing_values
from src.data_processing import create_point_df, get_first_crack_temp

import src.data_processing #***
reload (src.data_processing)
from src.data_processing import deconstruct_temp_curves, develop_point_df, check_missing_values
from src.data_processing import create_point_df, get_first_crack_temp

from src.data_export import export_raw_data, export_processed_data
from src.plots import plot_scatter#, plot_bar, plot_box, plot_scatter_matrix
from src.AI import get_origin

logging.basicConfig(filename='log_file.log', level=logging.DEBUG)

# Set Max columns to 100
pd.set_option('display.max_columns', 100)
# set up the data frame to be more readable
pd.set_option('display.width', 1000)

# Load from roasTime repository on macOS
home = os.path.expanduser('~')
base_path = os.path.join(home, 'Library/Application Support/roast-time/roasts')
##  IF you have a specific set of roast profiles in another folder, uncomment and adjust the line below
# base_path = Path('/data')

# Load the roasting data
df = load_roasting_data(base_path)

# Perform basic data cleanup
df = basic_cleanup(df)
print ("Basic Cleanup Done")

# Export the raw DataFrame to a .csv file
export_raw_data(df)
print ("Export Raw Data Done")

# Create DataFrames for the temperture logs (time series) and point attribute data for each roast
# Deconstruct temp curves from lists to new curve_df
curve_df = deconstruct_temp_curves(df)
print ("Deconstruct Done")

# create point_df
point_df = create_point_df(df)
print ("Create Point_df Done")

# get first crack temp
point_df = get_first_crack_temp(curve_df, point_df)
print ("Get First Crack Temp Done")


#%%
# Develop Point_DF
point_df = develop_point_df(point_df, curve_df)
print ("Develop Point_DF Done")

#%% ####### Use OpenAI to get the origin from the roastName ########
start_time = time.time()

# def get_origin_with_delay(roast_name):
#     time.sleep(0)
#     return get_origin(roast_name)
#point_df['Origin'] = None # initialize the column ***  probably not needed but trying to work on the timeout issue
# dealing with ReadTimeout: The read operation timed out
#point_df['Origin'] = point_df['roastName'].apply(get_origin_with_delay)
point_df['Origin'] = point_df['roastName'].apply(get_origin)

print ("Get Origin Done")
end_time = time.time()
elapsed_time = end_time - start_time
print(f"Function took {elapsed_time} seconds to run.")

# %% Personaly checking some results with plots as i fix the phases ***
############################################################################
display (point_df)
# %%
display (curve_df)
#%%
###  not working right now
import plotly.express as px
# make the x axis indexTime go from 0 to 150
fig = px.line(curve_df.loc[curve_df.roastName == 'Ethiopia #4 w/ marcel', :], x='indexTime', y='beanTemperature', title='Bean Temperature over Time')

ax = fig.update_xaxes(range=[0, 150])
fig.show()


# %% ###### chcking out some data from the curve_df  ***
# make a new df of curve_df based on just the first 10 roastNames in point_df
new_df = curve_df.loc[curve_df.roastName.isin(point_df.roastName.head(10))]

# group roasts by roastName and plot the first 10 beanTemperatures for the first 10 roasts in curve_df
fig = px.line(new_df.groupby('roastName').head(10), x='indexTime', y='beanTemperature', color='roastName', 
              title='Bean Temperature over Time')
ax = fig.update_xaxes(range=[0, 950])

fig.update_layout(legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="right", x=1))
fig.show()

#print indexTime and beanTemperature for new_df, show at least 50 rows
print (new_df[['indexTime', 'beanTemperature']].head(50))

############################################################################
#%%
#### FINAL CLEANUP and EXPORT #####

# Post-process cleanup
point_df = drop_intermediate_columns(point_df)
print ("Post-process cleanup Done")

# Check
check_missing_values(point_df)

# Export the processed curve_df and point_df to a .csv file
export_processed_data(curve_df, point_df)
print ("Export Processed Data Done")
#%%
# Simple QC Plots #
# plot_bar(point_df)
# plot_box(point_df)
plot_scatter(point_df)

#plot_scatter_matrix(point_df) #currently has issuse with missing values
# In the dataframe passed, the following columns have missing values: 
# ['weightLostPercent', 'ambient', 'humidity', 'Drop-ChargeDeltaTemp', 
# 'comments', 'rating', 'beanId', 'indexTurningPoint', 'ibtsTurningPointTemp', 
# 'turningPointTime']


# %%

"""
This script performs coffee roasting data analysis and visualization for RoasTime data from the Allio Bullet.
It has code cell markers to help naviate and run the code in VS Code or Jupyter Notebook extensions.
1. Load roasting data from a specified directory.
2. Perform basic data cleanup.
3. Deconstruct temperature curves from lists to a new curve DataFrame & create a point DataFrame.
4. Fill NaN values.
5. Develop the point DataFrame by adding derived attributes.
6. Use an AI model to extract the origin of the coffee beans.
7. Export the processed curve DataFrame and point DataFrame to CSV files.
8. Clean up, check and visualize some data.
"""
import logging
import os
import time
import numpy as np
import pandas as pd
#from importlib import reload
#from pathlib import Path
#from pprint import pprint
from src.data_load import load_roasting_data
from src.data_cleanup import basic_cleanup, fill_derivative_values, drop_intermediate_columns
from src.data_processing import deconstruct_temp_curves, develop_point_df, check_missing_values, create_point_df, get_first_crack_temp
from src.data_export import export_raw_data, export_processed_data
from src.plots import plot_scatter#, plot_bar, plot_box, plot_scatter_matrix
from src.plots import plot_scatter#, plot_bar, plot_box, plot_scatter_matrix
from src.AI import get_origin

logging.basicConfig(filename='log_file.log', level=logging.DEBUG)

# Set Max columns to 100
pd.set_option('display.max_columns', 100)
# set up the data frame to be more readable
pd.set_option('display.width', 1000)

# Load from roasTime repository on macOS
home = os.path.expanduser('~')
base_path = os.path.join(home, 'Library/Application Support/roast-time/roasts')
##  IF you have a specific set of roast profiles in another folder, uncomment and adjust the line below
# base_path = Path('/data')

# Load the roasting data
df = load_roasting_data(base_path)

# Perform basic data cleanup
df = basic_cleanup(df)
print ("Basic Cleanup Done")

# Export the raw DataFrame to a .csv file
export_raw_data(df)
print ("Export Raw Data Done")

# Create DataFrames for the temperture logs (time series) and point attribute data for each roast
# Deconstruct temp curves from lists to new curve_df
curve_df = deconstruct_temp_curves(df)
print ("Deconstruct Done")

# create point_df
point_df = create_point_df(df)
print ("Create Point_df Done")

curve_df = fill_derivative_values(curve_df)
print ('Filled nan values in derivative')

# get first crack temp
point_df = get_first_crack_temp(curve_df, point_df)
print ("Get First Crack Temp Done")

# Develop Point_DF
point_df = develop_point_df(point_df, curve_df)
point_df = develop_point_df(point_df, curve_df)
print ("Develop Point_DF Done")

####### Use OpenAI to get the origin from the roastName ########
from src.AI import get_origin

start_time = time.time()

# def get_origin_with_delay(roast_name):
#     time.sleep(0)
#     return get_origin(roast_name)
#point_df['Origin'] = None # initialize the column ***  probably not needed but trying to work on the timeout issue
# dealing with ReadTimeout: The read operation timed out
#point_df['Origin'] = point_df['roastName'].apply(get_origin_with_delay)
point_df['Origin'] = point_df['roastName'].apply(get_origin)

print ("Get Origin Done")
end_time = time.time()
elapsed_time = end_time - start_time
print(f"Function took {elapsed_time} seconds to run.")

# View results  ***
############################################################################
display (point_df)
display (curve_df)

#### FINAL CLEANUP and EXPORT #####

# Post-process cleanup
point_df = drop_intermediate_columns(point_df)
print ("Post-process cleanup Done")

# Check
check_missing_values(point_df)

##########
# Export the processed curve_df and point_df to a .csv file
#######
export_processed_data(curve_df, point_df)
print ("Export Processed Data to csv Done")



#%%
# Simple QC Plots #
# plot_bar(point_df)
# plot_box(point_df)
plot_scatter(point_df)

#plot_scatter_matrix(point_df) #currently has issuse with missing values
# In the dataframe passed, the following columns have missing values: 
# ['weightLostPercent', 'ambient', 'humidity', 'Drop-ChargeDeltaTemp', 
# 'comments', 'rating', 'beanId', 'indexTurningPoint', 'ibtsTurningPointTemp', 
# 'turningPointTime']



# %%
#view outliers
# Calculate the Z-score for each observation in the 'beanChargeTemperature' column
z_scores = np.abs((point_df['beanChargeTemperature'] - point_df['beanChargeTemperature'].mean()) / point_df['beanChargeTemperature'].std())

# Set a threshold for the Z-score to identify outliers
threshold = 3

# Filter the dataframe to only include observations with a Z-score greater than the threshold
outliers = point_df[z_scores > threshold]

# Print the outliers
print(outliers[['roastName', 'beanChargeTemperature']])



# %%
import seaborn as sns
import matplotlib.pyplot as plt

# Load your data

# Calculate correlation matrix
corr_matrix = point_df.corr()

# Plot heatmap
plt.figure(figsize=(12, 8))
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm')
plt.title('Correlation Matrix of Coffee Roasting Data')
plt.show()

# Scatter plot example
sns.scatterplot(x='beanChargeTemperature', y='firstCrackTemp', data=data, hue='countryOfOrigin')
plt.title('Bean Charge Temperature vs First Crack Temperature')
plt.show()
# %%
