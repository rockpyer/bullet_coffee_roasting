# cleaning up the data prior to processing and after processing

def basic_cleanup(df):
    # Sort by time and remove rows with missing roastName
    df.sort_values(by='dateTime', inplace=True)
    df.dropna(subset=['roastName'], inplace=True)

    # Filter dataframe to only your User ID, this removes all the roasts you've saved from other users
    # Find most frequent userID and use that as your choiceUserID
    choiceUserID = df['userId'].value_counts().idxmax()
    #choiceUserID = '73009f59-2d2e-4215-b6ff-961946ee0b80'  # Option to enter your specific userID (extracted from .json roast file, or RoastWorld web address)
    df = df.query('userId == @choiceUserID and isFork != 1.0')

    # Define list of unused data 
    other_meta = ['userId', 'isFork', 'serialNumber', 'IRSensor', 'inventory.nextGreenWeight',
                  'inventory.previousGreenWeight', 'inventory.changeInGreenWeight', 'isPrivate',
                  'slug', 'updated_at', 'updatedAt', 'hardware', 'tagids', 'recipeID',
                  'parentUserId','parentUsername','overlayID', 'actions.actionTempList', 'deviceType']

    # Drop the extra data
    df = df.loc[:, ~df.columns.isin(other_meta)]
    #df.drop(other_meta, axis=1) #not using because this or inplace=True gave errors about setting on a copy
    
    # Shift column 'Name' to first position
    first_column = df.pop('roastName')
    df.insert(0, 'roastName', first_column)
    
    #reset index
    df.reset_index(drop=True, inplace=True)

    df = fix_zero_drop_temps(df)
    
    #print
    print (f'Removed unused columns from RoastTime: {other_meta}')
    
    return df

def fix_zero_drop_temps(df):
    # Some RT4 roasts (#138-#143) were saved with charge and drop temperatures of 0 and roastEndIndex=0.
    # Read them off the recorded curves instead (charge = roastStartIndex sample, drop = last sample)
    # so Drop-Charge delta, IBTS-BT at drop, time/temp and the RoR estimates aren't computed from 0.
    temp_cols = ['drumChargeTemperature', 'beanChargeTemperature', 'drumDropTemperature', 'beanDropTemperature']
    bad = ~(df[temp_cols].fillna(0) > 0).all(axis=1)
    for i in df.index[bad]:
        start = int(df.at[i, 'roastStartIndex']) if df.at[i, 'roastStartIndex'] > 0 else 0
        if not df.at[i, 'drumChargeTemperature'] > 0:
            df.at[i, 'drumChargeTemperature'] = df.at[i, 'drumTemperature'][start]
        if not df.at[i, 'beanChargeTemperature'] > 0:
            df.at[i, 'beanChargeTemperature'] = df.at[i, 'beanTemperature'][start]
        if not df.at[i, 'drumDropTemperature'] > 0:
            df.at[i, 'drumDropTemperature'] = df.at[i, 'drumTemperature'][-1]
        if not df.at[i, 'beanDropTemperature'] > 0:
            df.at[i, 'beanDropTemperature'] = df.at[i, 'beanTemperature'][-1]
        if not df.at[i, 'roastEndIndex'] > 0:
            df.at[i, 'roastEndIndex'] = len(df.at[i, 'beanTemperature']) - 1
    if bad.any():
        print(f"Filled zero charge/drop temperatures from the recorded curves for: {df.loc[bad, 'roastName'].tolist()}")
    return df

def fill_derivative_values(df):
    # Fill the leading NaN rows of ibtsDerivative/ibts2ndDerivative with 0 (usually just the first 1-2 rows, pretty negligible)
    # Only for roasts that have an IBTS derivative curve. RT2 roasts (2019-2020) never recorded one, so they stay NaN
    # instead of becoming a fake flat line of zeros.
    has_ibts = df.groupby('roastName')['ibtsDerivative'].transform(lambda x: x.notnull().any())
    for col in ['ibtsDerivative', 'ibts2ndDerivative']:
        df.loc[has_ibts, col] = df.loc[has_ibts, col].fillna(0)
    return df

def drop_intermediate_columns(df):
    # *** TBD drop columns that are not needed for analysis in point_df 
    # all index columns, others...
    unneeded = ['roastEndIndex', 'roastStartIndex', 'indexFirstCrackEnd','indexYellowingStart', 'missingSeconds',
                'roastNumber', 'roastDegree', 'tagids', 'recipeID','parentUserId','parentUsername','overlayID', ]
    df = df.loc[:, ~df.columns.isin(unneeded)]

    print (f'Removed potential intermediate columns: {unneeded}')
    return df

def reorder_columns(curve_df):
    # Reorder columns
    curve_df = curve_df[['roastName', 'dateTime', 'indexTime', 'beanTemperature', 'drumTemperature', 'ibtsDerivative', 'ibts2ndDerivative']]
    return curve_df
    