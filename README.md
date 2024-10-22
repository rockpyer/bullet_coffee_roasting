# Aillio Bullet Coffee Roasting Data Analysis

This project transforms and analyzes data from the [Aillio Bullet coffee roaster](https://aillio.com/?page_id=23112) in order to measure and understand the various factors that influence roast quality. This is a project of my own pasion and interests https://www.instagram.com/f.w.bennies

![@f.w.bennies](images/friendshipsign.png)

## Key Features

- **Data Transformation**: The raw data is pulled out of hidden and obscured JSON files into a data frame for  analysis. Raw data is exported to a .csv file.

- **Data Cleaning**: The data is cleaned for common errors, outliers, and unwanted records.

- **Temperature Curve Deconstruction**: The temperature curves are deconstructed from lists to a new DataFrame (`curve_df`) and saved as curve_data_*timestamp*.csv

- **Point DataFrame Creation**: A DataFrame (`point_df`) is created to hold point attribute data for each roast and saved as time_data_*timestamp*.csv

- **Phase and Feature Engineering**: The `point_df` DataFrame is enhanced with additional points (e.g.turningPointTime, yellowingPhaseTime, and avgYellowingPhaseROR) to characterize and quantify relationships throughout the roast.

- **Origin Determination**: The origin of the coffee is determined based on the roast name using OpenAI and added to the `point_df` DataFrame.

## Usage
To run the analysis, simply run the `main.py` script. The script will print messages to the console to indicate the progress of the analysis.

## Results
.csv outputs have enabled several other projects and analysis that help guide my roasting and learning.
- For example a my [Bullet Coffee Roasting Dashboard](https://public.tableau.com/app/profile/ryan.weller/viz/BulletCoffeeRoastingDashboard/OverviewDash?publish=yes)
- An unpublished LangChain project to query the data as a .csv or SQL database.
- One off visualizations and conversations.

![roasting data scatter plot](images/bulletRoastingEDA.png)

![roasting data with itbs ror](images/allRoastsPlt.png)

## Assumptions
  - Phase and key point temps are IBTS (drum) temps unless specifically noted. Turning point can only be calculated from beanTemp but the same index time is used to find the ibtsTemp at that time. 
 - Several cleanup functions are catered to my own practices, issues, and needs. For example, I rarely roast into second crack and always record ambient temp, humidity and green weight. If you don't record many of these values, the application will likely filter out those rows or create errors.
 - Assumed that your RoastTime is installed in the default MacOS location. Else edit 'base_path'
 - Built for my V2 Bullet purchased in July 2020 - the data structure of the .json files have changed from Aillio's updates over the years (roast color, Roast Degree). At times I have exclude attributes that have been added or removed, this may need to be updated in the future.
 - 
## Future Work

Future work on this project will involve more detailed analysis of the data, including statistical analysis and machine learning to predict the quality of the roast based on the available data. Please contact or comment for any questions or collaboration.


