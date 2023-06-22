#this is creating two new df from the big old original df 
### curver_df as the individual temperature curves that are in a list and converting them to a dataframe
### point_df as single point attributes that are in a list and converting them to a dataframe
import pandas as pd
import numpy as np
import traceback

def deconstruct_temp_curves(df):
    try:
        temp_curve_df = pd.DataFrame()
        curve_df = pd.DataFrame()
        for index, row in df.iterrows():
            temp_curve_df = pd.DataFrame([pd.Series(row['beanTemperature'], name='beanTemperature', dtype='float64'),
                                        pd.Series(row['drumTemperature'], name='drumTemperature', dtype='float64'),
                                        pd.Series(row['beanDerivative'], name='beanDerivative', dtype='float64'),
                                        pd.Series(row['ibtsDerivative'], name='ibtsDerivative', dtype='float64')]).T
            temp_curve_df['roastName'] = row['roastName']
            temp_curve_df['indexTime'] = temp_curve_df.index
            temp_curve_df['softwareVersion'] = row['softwareVersion']
            curve_df = pd.concat([curve_df, temp_curve_df], ignore_index=True)
                        
        # Calculate second derivative
        ### first pass at 2nd Derivative, review and see how to improve and smooth
        curve_df['ibts2ndDerivative'] = curve_df.groupby('roastName')['ibtsDerivative'].apply(lambda x: x.diff())

        curve_df.fillna(value=np.nan, inplace=True)
    
        return curve_df
    
    except Exception as e:
        print("Error: Unable to deconstruct temperature curves.")
        print("Exception:", str(e))
        traceback.print_exc()

        
def develop_point_df(df, curve_df):
    # Create df of point sets (single entry per profile)
    point_list = ['roastName', 'dateTime', 'beanChargeTemperature', 'beanDropTemperature', 'drumChargeTemperature',
              'drumDropTemperature', 'preheatTemperature', 'roastStartIndex', 'roastEndIndex',
              'weightGreen', 'weightRoasted', 'weightLostPercent', 'ambient', 'humidity', 'Drop-ChargeDeltaTemp',
              'totalRoastTime', 'indexFirstCrackStart', 'indexFirstCrackEnd', 'indexYellowingStart',
              'comments', 'roastNumber', 'firmware', 'missingSeconds',
              'rating', 'beanId']
    point_df = pd.DataFrame(df, columns=point_list).reset_index()
    point_df.drop(columns='index', inplace=True)
    point_df.indexYellowingStart = point_df.indexYellowingStart.fillna(value=np.nan)
    #point_df.indexFirstCrackStart = point_df.indexFirstCrackStart.fillna(value=np.nan)
    
    # Find turning point index and index at 165 deg bean Temp
    sampleRate = 2
    roastName_df = curve_df.groupby(['roastName'])
    
    for name, group in roastName_df:
        minBT = group.beanTemperature.min()
        for i, row in group.iterrows():
            if row.beanTemperature == minBT and row.beanDerivative >= 0:
                point_df.loc[(point_df.roastName == name), 'indexTurningPoint'] = row.indexTime
                point_df.loc[(point_df.roastName == name), 'ibtsTurningPointTemp'] = row.drumTemperature
                break
        for i, row in group.iterrows():
            if row.indexTime > 120 and row.drumTemperature >= 165:
                autoYP165 = row.indexTime
                point_df.loc[(point_df.roastName == name), 'index165PT'] = autoYP165
                break
    
    point_df['turningPointTime'] = (point_df.indexTurningPoint) / 60 / sampleRate

    # Replace missing or bad YP pick with autoYP165
    point_df.loc[(point_df.indexYellowingStart < 1), 'indexYellowingStart'] = point_df.index165PT
    point_df.loc[(point_df.indexYellowingStart.isnull()), 'indexYellowingStart'] = point_df.index165PT
    point_df['yellowPointTime'] = point_df.indexYellowingStart / 60 / sampleRate

    # Replace bad FC points with np.nan
    point_df.loc[(point_df.indexFirstCrackStart == 0), 'indexFirstCrackStart'] = np.nan
    point_df.loc[(point_df.indexFirstCrackStart > 10000), 'indexFirstCrackStart'] = np.nan
    point_df['firstCrackTime'] = point_df.indexFirstCrackStart / 60 / 2

    # Time/Temp and Temp/Time calculations
    point_df['time/temp'] = point_df.totalRoastTime / point_df.beanDropTemperature
    point_df['temp/time'] = point_df.beanDropTemperature / point_df.totalRoastTime

    # ITBS BeanProbe difference for change over time plot
    point_df['deltaIBTS-BT'] = point_df.drumDropTemperature - point_df.beanDropTemperature

    return point_df


def check_missing_values(df):
    missing_cols = df.columns[df.isnull().any()].tolist()
    if missing_cols:
        print(f"In the dataframe passed, the following columns have missing values: {missing_cols}")
    else:
        print(f"No missing values found in the DataFrame passed.")
