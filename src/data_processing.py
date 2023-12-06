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
            temp_curve_df['indexFirstCrackStart'] = row['indexFirstCrackStart']
            temp_curve_df['softwareVersion'] = row['softwareVersion']
            curve_df = pd.concat([curve_df, temp_curve_df], ignore_index=True)
                        
        # Calculate second derivative ***
        ### first pass at 2nd Derivative, review and see how to improve and smooth
        curve_df['ibts2ndDerivative'] = curve_df.groupby('roastName')['ibtsDerivative'].apply(lambda x: x.diff())
        curve_df.fillna(value=np.nan, inplace=True)
    
        return curve_df
    
    except Exception as e:
        print("Error: Unable to deconstruct temperature curves.")
        print("Exception:", str(e))
        traceback.print_exc()

def create_point_df(df):
    # Create df of point sets (single entry per profile)
    point_list = ['roastName', 'dateTime', 'beanChargeTemperature', 'beanDropTemperature', 'drumChargeTemperature',
              'drumDropTemperature', 'preheatTemperature', 'roastStartIndex', 'roastEndIndex',
              'weightGreen', 'weightRoasted', 'weightLostPercent', 'ambient', 'humidity', 'Drop-ChargeDeltaTemp',
              'totalRoastTime', 'indexFirstCrackStart', 'indexFirstCrackEnd', 'indexYellowingStart',
              'comments', 'roastNumber', 'firmware', 'missingSeconds', 'rating', 'beanId']
    point_df = pd.DataFrame(df, columns=point_list).reset_index()
    point_df.drop(columns='index', inplace=True)
    
    print (point_df.info())
    point_df.indexYellowingStart = point_df.indexYellowingStart.fillna(value=np.nan)
    #point_df.indexFirstCrackStart = point_df.indexFirstCrackStart.fillna(value=np.nan)

    # Replace bad FC points with np.nan and create firstCrackTime 
    point_df.loc[(point_df.indexFirstCrackStart == 0), 'indexFirstCrackStart'] = np.nan
    point_df.loc[(point_df.indexFirstCrackStart > 10000), 'indexFirstCrackStart'] = np.nan
    point_df['firstCrackTime'] = point_df.indexFirstCrackStart / 60 / 2

    return point_df
    
#12/05 fix for firstCrackTime and firstCrackTemp
def get_first_crack_temp(df, point_df):  # *** rename this function
    for name, group in df.groupby('roastName'):
        minBT = group.beanTemperature.min()
        for i, row in group.iterrows():
            if row.beanTemperature == minBT:  # previously-  and row.beanDerivative >= 0  but a small % of roasts were assigned nan
                point_df.loc[(point_df.roastName == name), 'indexTurningPoint'] = row.indexTime
                point_df.loc[(point_df.roastName == name), 'ibtsTurningPointTemp'] = row.drumTemperature
                break
        for i, row in group.iterrows():
            if row.indexTime > 120 and row.drumTemperature >= 165:
                autoYP165 = row.indexTime
                point_df.loc[(point_df.roastName == name), 'index165PT'] = autoYP165
                break
        if 'indexFirstCrackStart' in group.columns:
            first_crack_start = group['indexFirstCrackStart'].iloc[0]
            if not pd.isna(first_crack_start):
                first_crack_temp = group.loc[group['indexTime'] == first_crack_start, 'drumTemperature'].values[0]
                point_df.loc[point_df['roastName'] == name, 'firstCrackTemp'] = first_crack_temp
            else:
                print(f"No 'indexFirstCrackStart' for roastName: {name}")
        else:
            print(f"No 'indexFirstCrackStart' column in the group for roastName: {name}")
    return point_df
        
        #this is the old code thats not working anyway good thing i'm in dev for now
        #ah crap did i need that for Turning Point?  I think so##### ****
        
        
    # create a new df from curve_df grouped by roastName
    # roastName_df = curve_df.groupby(['roastName'])
    # print (roastName_df.describe())
    # print (roastName_df.head())
    # for name, group in roastName_df:
    #     minBT = group.beanTemperature.min()
    #     for i, row in group.iterrows():
    #         if row.beanTemperature == minBT:  # previously-  and row.beanDerivative >= 0  but a small % of roasts were assigned nan
    #             point_df.loc[(point_df.roastName == name), 'indexTurningPoint'] = row.indexTime
    #             point_df.loc[(point_df.roastName == name), 'ibtsTurningPointTemp'] = row.drumTemperature
    #             break
    #     for i, row in group.iterrows():
    #         if row.indexTime > 120 and row.drumTemperature >= 165:
    #             autoYP165 = row.indexTime
    #             point_df.loc[(point_df.roastName == name), 'index165PT'] = autoYP165
    #             break
    #     # For each roastName get the drumTemperature from the curve_df at the index of firstCrackStart (indexFirstCrackStart)
    #     # in the point_df and put it in the point_df as firstCrackTemp
    #     print (f'starting firstCrackTime Section for {name}')
    #     for i, row in group.iterrows():
    #         name_condition = (point_df.roastName == name)
    #         if name_condition.loc[i]:  # Check if name_condition is True for this row
    #             print('name_condition,i, row')
    #             print(name_condition,i, row)
    #         # Check if indexFirstCrackStart is null/NaN
    #         if pd.isna(point_df.loc[name_condition, 'indexFirstCrackStart']).any():
    #             point_df.loc[name_condition, 'firstCrackTemp'] = np.nan
    #         else:
    #             index_condition = (row.indexTime == point_df.loc[name_condition, 'indexFirstCrackStart'])
    #             if index_condition.any():
    #                 point_df.loc[name_condition, 'firstCrackTemp'] = row.drumTemperature
    #             else:
    #                 print(f"No rows where indexTime equals indexFirstCrackStart for roastName {name}")
    #         break

    #     # for i, row in group.iterrows():
    #     #     name_condition = (point_df.roastName == name)
    #     #     index_condition = (row.indexTime == point_df.loc[name_condition, 'indexFirstCrackStart'])
            
    #     #     if index_condition.any():
    #     #         point_df.loc[name_condition, 'firstCrackTemp'] = row.drumTemperature
    #     #         break

def develop_point_df(point_df, curve_df):

    # Create a turningPointTime column to mark the TP time
    sampleRate = 2
    point_df['turningPointTime'] = (point_df.indexTurningPoint) / 60 / sampleRate

 
    #convert WG and WR to numeric values
    point_df['weightGreen'] = pd.to_numeric(point_df['weightGreen'])
    point_df['weightRoasted'] = pd.to_numeric(point_df['weightRoasted'])
    # If weightGreen and weightRoasted are non-zero, calculate weightLostPercent, else set to np.nan
    point_df.loc[(point_df.weightGreen > 0) & (point_df.weightRoasted > 0), 'weightLostPercent'] = (point_df.weightGreen - point_df.weightRoasted) / point_df.weightGreen * 100

    # Replace missing or bad YP pick with autoYP165
    point_df.loc[(point_df.indexYellowingStart < 1), 'indexYellowingStart'] = point_df.index165PT
    point_df.loc[(point_df.indexYellowingStart.isnull()), 'indexYellowingStart'] = point_df.index165PT
    point_df['yellowPointTime'] = point_df.indexYellowingStart / 60 / sampleRate


    # Create a yellowPointTemp165 column to mark the YP temp as 165 always
    point_df['yellowPointTemp165'] = 165
   

    # Determine the max ROR for each roastName using an average moving window of 50 points (25 seconds)
    point_df['peakRoR'] = curve_df.groupby('roastName')['ibts2ndDerivative'].rolling(50, center=True).mean().groupby(level=1).max().reset_index(drop=True)
    window_size = 50
    roll_max = curve_df.groupby('roastName')['ibts2ndDerivative'].apply(lambda x: x.rolling(window=window_size, center=True).mean().idxmax() / 60 / sampleRate).reset_index(drop=True)
    point_df['peakRoRTime'] = roll_max
    

    # Time/Temp and Temp/Time calculations for the IBTS drum temp
    point_df['time/temp'] = point_df.totalRoastTime / point_df.drumDropTemperature
    point_df['temp/time'] = point_df.drumDropTemperature / point_df.totalRoastTime
   

    # IBTS BeanProbe difference for change over time plot
    point_df['deltaIBTS-BT-atDrop'] = point_df.drumDropTemperature - point_df.beanDropTemperature


    # Calculate Yellowing Phase Duration, time from Turning point to Yellowing Point
    point_df['yellowingPhaseTime'] = point_df.yellowPointTime - point_df.turningPointTime


    # Calculate Browning Phase Duration, time from Yellowing Point to First Crack Start
    # if first crack time is > 0 calc browning phase, else if firstCrackTime is NaN or blank set browningPhaseTime to NaN
    point_df.loc[(point_df.firstCrackTime.isnull()) | 
        (point_df.firstCrackTime == '') |
        (point_df.firstCrackTime <= 0), 'browningPhaseTime'] = np.nan
    point_df.loc[(point_df.firstCrackTime > 0), 'browningPhaseTime'] = point_df.firstCrackTime - point_df.yellowPointTime


    # Calculate Development Duration, time from First Crack Start to First Crack End or Drop
    # if first crack time is true, run, else if firstCrackTime is NaN or blank set developmentTime to NaN
    point_df.loc[(point_df.firstCrackTime.isnull()) | 
        (point_df.firstCrackTime == '') |
        (point_df.firstCrackTime <= 0), 'developmentTime'] = np.nan
    point_df.loc[(point_df.firstCrackTime > 0), 'developmentTime'] = point_df.totalRoastTime - point_df.firstCrackTime

    # Calculate RoR from Turning Point to Yellowing Point (estimated from straight point to point) *** future TBD - check against the actual mean values from curve_df
    point_df['RoR-yellowing-est'] = (165 - point_df.ibtsTurningPointTemp) / point_df.yellowingPhaseTime


    # Calculate RoR from in the Browing phase (Yellowing Point to First Crack Start)
    # if first crack time is true, run, else if firstCrackTime is NaN or blank set RoR-browning-est to NaN
    point_df.loc[(point_df.firstCrackTime.isnull()) | 
        (point_df.firstCrackTime == '') |
        (point_df.firstCrackTime <= 0), 'RoR-browning-est'] = np.nan
    point_df.loc[(point_df.firstCrackTime > 0), 'RoR-browning-est'] = (point_df.firstCrackTemp - 165) / point_df.browningPhaseTime


    # Calculate RoR from First Crack Start to First Crack End or Drop
    # if first crack time is true, run, else if firstCrackTime is NaN or blank set RoR-development-est to NaN
    point_df.loc[(point_df.firstCrackTime.isnull()) | 
        (point_df.firstCrackTime == '') |
        (point_df.firstCrackTime <= 0), 'RoR-development-est'] = np.nan
    point_df.loc[(point_df.firstCrackTime > 0), 'RoR-development-est'] = (point_df.totalRoastTime - point_df.firstCrackTime) / point_df.developmentTime

    # Calculate the fullRoastROR from Turning Point to Drop Temp *** (future fix, this might be better if from Peak ROR to Drop)
    point_df['RoR-fullRoast-est'] = (point_df.drumDropTemperature - point_df.ibtsTurningPointTemp) / (point_df.totalRoastTime - point_df.turningPointTime)

    
    return point_df


def check_missing_values(df):
    missing_cols = df.columns[df.isnull().any()].tolist()
    if missing_cols:
        print(f"In the dataframe passed, the following columns have missing values: \n{missing_cols}")
    else:
        print(f"No missing values found in the DataFrame passed.")


# store of additional coffee regions
# Flores, Java, Sulawesi, Sumatra, Timor, Bali
