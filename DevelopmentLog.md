### Development Notes

#### NEED better fix for bad data (currently replaceing row NAN)
RT2 - no ibtsDerivitive and no uid. (Calculate derivitive for this before staring 2nd D)
 - ibtsDerivative  is NaN is many many older roasts! - fill - ibtsDerivative  is NaN is many many older roasts! - fill
 
#### Problems and outliers
 - iterrows is SLOW - learn vectorization and itertuple (also df.colName. vs df['colName'] 
     - do this for indexFirstCrackStart, weightLostPercent, weightLostPercent in first cell
     - and point_df auto 165 and other values 
 - Many outliers and messes since 1/26 changes to pulling data from all roasts rather than select roasts
 - deltaTemp shows some 0 or negative values
  
##### RAW DATA Problems
 - bad intial YP (# 25 Kenya Mix 350/140 and prob more.... go thru 1by1..Delete OLD and restore NEW)

##### TEMP FIX
 Some other roast has 0 sec FC time - currently replaceing row NAN (check what line)
 
#### Work Log
- 12/20/20 ish - Started Project
- work since late december not recorded
- 1/17/21 roastName_df and indexTurningPoint in much better shape. however one point is 0 and one is missing (or many different)
- 1/18/21  fixed 165 auto YP with simlar method for iterating over groups for indexTurningPoint. Broke weightLoss
- 1/19/21  cleaned up documentation. removed PNG 24 (quite manually, can't figure out why, found roasts in    
 - Removed Ethiopia # 6 funny story..., also fixed stacked plot by breaking out ax1.scatter into 2 lines and s = 0.03 (very small!)
- 1/24/21  carried over RT2 ambientTemp and roomHumidity to RT3 ambient, humididty columns and dropped old.  Fixed 100% weightLostPercent
 - added simple liner regression of weight loss % and drop temp while removing nans. (Started f.w.bennies instagram)
- 1/25/21 brought in new roasts from RW, fixed up regression to show for specific beans in a list
- 1/26/21 changed to multiload2, cleaned up documentation, load straight out of library/ roasts folder to avoid scraping, found new errors based on loading more data (temp and other strings), fixed., added titles to regression charts, make list for 'kenya' in roast name and plotted results limiting to kenyans
- 1/29/21 uploaded to GitHub, cleaned up some notes and organization
- 1/30/21 created userId filter, starting trying to create 1stD for RT2 (problematic), created one-liner for 2ndDerivitive but problems creating 1stD only if Software version is np.nan (RT2)
- 1/31/21 plotting (changed a lot of plt. settings) 2ndD shows arrow cloud of +&- slopes, must consider challenges and uses, put on shelf for now.  Focus on Max ROR and phase time, fixed ambient temps = 0 with np.nan replacement
- 2/3/21 small changes in plotting. noted that 'drumChargeTemperature' is more accurate that preheatTemp due to errors in recording planned charge/preheat temp in early RT3 version
- 2/5/21 'drumChargeTemp' is not best when preheatTemp is x < x (x could be counted as 1 std dev?)
- 2/12/21 added calcuations for YP and FC Time not just index or second values, created function for linear regression with auto time and temp unit labels
- 9/30/21 no real work but re-touched with a few new houston roasts.  deleted a few bad roasts rather than keeping them around
- 01/24/23 - Well it's been a min. I figured I should get back into this.  Big effort to uninstall and (w/ many problems) reinstall Anaconda Navigator.
    - Immediate Errors:
    - First I found that .append was being depreciated, so I did a little work to replace them with pd.concat.
    - Now I really just want figure out what I was doing with my two different Google Drives (one wasn't syncing) and see if I'm working in the most recent space.
    - Also, wanted to figureout where I was exporting data as a .csv (I found several df_bulkloadBullet.csv files around but I can't find the code where I did that...)  Wanting to can put it into AML or DataRobot for additional learning.
    - Should try to play around with my ideas of imputing (rather than skipping) missing data and the statistical analysis of such.... if possible
 - 1/26/23 - Used ChatGPT to learn about beautiful soup and test scraping some sweetmaria's webdata using selenium. Good start but to the SM website is not always consistent with available data. Also I haven't tried to loop the request and gather a list of data to later be cleaned up or transformed.
 - 1/27/23 - Used ChatGPT to clean up some wonky code and reduce errors
 - 1/27/23 - need to clean up scatter matrix errors:
   * /Users/ryanweller/opt/anaconda3/lib/python3.9/site-packages/pandas/plotting/_matplotlib/misc.py:100: UserWarning: Attempting to set identical left == right == 0.925 results in singular transformations; automatically expanding. ax.set_xlim(boundaries_list[j])
 - 1/27/23 - Starting to clean up this big notebook into chunks of funcationality




## NEXT - calculate phases and DTR
- proper phase identification and times
- break out into different scripts
- cleanup and speed up code
- more PLOTS AS def FUNCTIONS 
- How about WL% / DTR (plot wl% vs DTR,   then WL%/DTR vs drop temp!
- (Delta ITBS and BT) vs roastDate [can we see the machine getting dirty and probes changing?, when did I change?]
- extract roast power and fan dictionary
- Max ROR relative to TP (work with intergral of ROR peak to quatify signifigance of ROR peak plateau, may need 2ndD)
- if drumbChargeTemp is much lower than PH - maybe don't just change it, but make a flag for bad roasts
- flag 'good roast, True/False

- tracking density - some data in google sheet, run EDA and try to correlate then project prediction to all other roasts.
- Create fun and beautiful visuals and art that may or may not be useful
- track amount of coffee roasted over time

- fill in ITBS derivitive for RT2 (RT3 algo is probably hidden, not easy)]
- potentially skip 2 calculus steps above and move on with data exploration and results
- - report out on bean probe correlation (charge, TP, yellow, FC, drop) 
- - effect on preheat (drumChargeTemperature) and events (TP, yellow, FC)
- - limited estimates from weight loss and acknowledged challenges
- tracking tasting notes.   - how to keep a simple and useful loger for this project?
- set future colors to deuteranomaly friendly palettes (avoid red+green)

- change all envirionmental temp (pittsburgh roasts) from F to C.   Since I moved to houston and RT3, I have been using C for enviro temp
- since i've started roasting >500-600g batches, I should break out 

- Plot difference between BT and ITBS at certain temps (100, 165, 180, 190, 200, 210, charge, and drop!) and batch size, look for trend over time or with batch sizes

 - add additional target points like 185, maybe 180 and 190 or others?
 - Add soak/no_soak boolean
 