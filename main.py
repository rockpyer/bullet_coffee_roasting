#%%
import logging
logging.basicConfig(filename='my_log_file.log', level=logging.DEBUG)
import os
import pandas as pd
from pathlib import Path
from roasting_data import load_roasting_data
from data_cleanup import basic_cleanup, drop_intermediate_columns
from data_processing import deconstruct_temp_curves, develop_point_df, check_missing_values
#from AI import  api_key, get_origin
from data_export import export_raw_data, export_processed_data
from plots import plot_bar, plot_box, plot_scatter, plot_scatter_matrix
from pprint import pprint

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

#%%
# Develop Point_DF
point_df = develop_point_df(df, curve_df)
print ("Develop Point_DF Done")

#%% 
from AI import  api_key, get_origin
import time
start_time = time.time()

# Use OpenAI to get the origin from the roastName 
point_df['Origin'] = point_df['roastName'].apply(get_origin)
print ("Get Origin Done")

end_time = time.time()
elapsed_time = end_time - start_time
print(f"Function took {elapsed_time} seconds to run.")

#%% 
#################
# %%
# #from the curve_df plot the Bean Temperature and indexTime for the roastName = "Ethiopia #4 w/ marcel"
import plotly.express as px
# make the x axis indexTime go from 0 to 150
fig = px.line(curve_df.loc[curve_df.roastName == 'Ethiopia #4 w/ marcel', :], x='indexTime', y='beanTemperature', title='Bean Temperature over Time')

ax = fig.update_xaxes(range=[0, 150])
fig.show()

# %%
# make a new df of curve_df based on just the first 10 roastNames in point_df
new_df = curve_df.loc[curve_df.roastName.isin(point_df.roastName.head(10))]

# %%
#group roasts by roastName and plot the first 10 beanTemperatures for the first 10 roasts in curve_df
fig = px.line(new_df.groupby('roastName').head(10), x='indexTime', y='beanTemperature', color='roastName', 
              title='Bean Temperature over Time')
ax = fig.update_xaxes(range=[0, 950])
fig.show()

#%%
#print indexTime and beanTemperature for new_df, show at least 50 rows
print (new_df[['indexTime', 'beanTemperature']].head(50))







############################################################################
#%%
# Post-process cleanup
point_df = drop_intermediate_columns(point_df)
print ("Post-process cleanup Done")

# Check
check_missing_values(point_df)
print ("Missing Values Check Done")

# Review the results
#print(df.head())
#print(curve_df)
print ('Results')
display (point_df)

# Export the processed curve_df and point_df to a .csv file
export_processed_data(curve_df, point_df)
#%%
# Plot as you wish #
# plot_bar(point_df)
# plot_box(point_df)
plot_scatter(point_df)

#plot_scatter_matrix(point_df) #currently has issuse with missing values
# In the dataframe passed, the following columns have missing values: 
# ['weightLostPercent', 'ambient', 'humidity', 'Drop-ChargeDeltaTemp', 
# 'comments', 'rating', 'beanId', 'indexTurningPoint', 'ibtsTurningPointTemp', 
# 'turningPointTime']

print ("Done")


# %%
import pandas as pd
from datetime import datetime

timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
point_filename = f'point_data_{timestamp}.csv'
curve_filename = f'curve_data_{timestamp}.csv'

# Export the DataFrame to a CSV file with the timestamp in the file name
point_df.to_csv(f'csvExports/{point_filename}', index=False)
curve_df.to_csv(f'csvExports/{curve_filename}', index=False)

print (f'Exported {point_filename} and {curve_filename} to csvExports folder')

# %%