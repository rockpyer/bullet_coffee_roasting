#%%
import os
import pandas as pd
from pathlib import Path
from roasting_data import load_roasting_data
from data_cleanup import basic_cleanup
from data_processing import deconstruct_temp_curves, develop_point_df, check_missing_values
from data_export import export_raw_data, export_processed_data
from plots import plot_bar, plot_box, plot_scatter, plot_scatter_matrix
from pprint import pprint

# Load from roasTime repository on macOS
home = os.path.expanduser('~')
base_path = os.path.join(home, 'Library/Application Support/roast-time/roasts')
##  IF you have a specific set of roast profiles in another folder, uncomment the below
# base_path = Path('/data')

# Load the roasting data
df = load_roasting_data(base_path)

# Perform basic data cleanup
df = basic_cleanup(df)

# Export the raw DataFrame to a .csv file
export_raw_data(df)

# Create DataFrames for the temperture logs (time series) and point attribute data for each roast
# Deconstruct temp curves from lists to new curve_df
curve_df = deconstruct_temp_curves(df)

# Develop Point_DF
point_df = develop_point_df(df, curve_df)

# Check
check_missing_values(point_df)

# Print the resulting DataFrames
#print(df.head())
#print(curve_df)
print (point_df)

# Export the processed curve_df and point_df to a .csv file
export_processed_data(curve_df, point_df)

# Plot as you wish 
#plot_bar(point_df)
#plot_box(point_df)
#plot_scatter(point_df)

#plot_scatter_matrix(point_df) #currently has issuse with missing values
# In the dataframe passed, the following columns have missing values: 
# ['weightLostPercent', 'ambient', 'humidity', 'Drop-ChargeDeltaTemp', 
# 'comments', 'rating', 'beanId', 'indexTurningPoint', 'ibtsTurningPointTemp', 
# 'turningPointTime']

print ("Done")

# %%
