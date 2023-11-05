#SCRAP NOTES ON GENERATING THE 1ST DERIVITIVE BEFORE IT WAS REGULARLY RECORDED BY ALLIO, AND SECOND+ DERIVITIVE STUFF FOR FUTURE WORK

####  below is a messy work in progress on 2nd Derivitive ignore #
def secondD(firstD):
    # returns the difference between post and pre
    return df.itbsDetivative.diff(firstD)
# TBD create IBTS 1st D and 2nd D
#for name, group in curve_df.groupby('roastName').ibtsDerivative:
#    if group.softwareVersion is np.isnan:
#        display ( group)
#        display (name,'dog')
#        break

# create itbs1stDerivative (ROR) for RT2 roasts
#for v in curve_df['softwareVersion']:
#    if v == np.isnan:
#        curve_df['ibtsDerivative'] = curve_df.groupby('roastName')['ibtsDerivative'].apply(lambda x:x.diff())
#    else:
#        curve_df['ibtsDerivative'] = curve_df.groupby('roastName')['ibtsDerivative'].apply(lambda x:x.diff()) #what was i doing here


#curve_df['ibtsDerivative'] = curve_df[curve_df['softwareVersion'] == np.isnan].groupby('roastName')['ibtsDerivative'].apply(lambda x:x.diff())
# create ibts2ndDerivative (ROR of ROR) for all roasts
curve_df['ibts2ndDerivative'] = curve_df.groupby('roastName')['ibtsDerivative'].apply(lambda x:x.diff())

#chris albon says....
#df.groupby('roastName')['ibtsDerivative'].apply(lambda x:x.rolling(center=False,window=2).mean())

#for name, group in curve_df.roastName:
#    print(name)
#   for i,row in group.iteritems():     
#        if i is 1:
#            curve_df.loc[(curve_df.roastName == name),'ibts2ndDerivative'] = 0
#        else: 
#            curve_df.loc[(curve_df.roastName == name),'ibts2ndDerivative'] = .......

#assert df.ibtsSecondDerivative[0] == 0