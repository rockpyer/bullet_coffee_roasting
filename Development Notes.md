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
- 2/28/21 [planned - flag 'good roast, True/False]

## NEXT - calculate phases and DTR
- 
- more PLOTS AS def FUNCTIONS (duh)
- How about WL% / DTR (plot wl% vs DTR,   then WL%/DTR vs drop temp!
- (Delta ITBS and BT) vs roastDate [can we see the machine getting dirty and probes changing?]
- extract roast power and fan dictionary
- Max ROR relative to TP (work with intergral of ROR peak to quatify signifigance of ROR peak plateau, may need 2ndD)
- if drumbChargeTemp is much lower than PH - maybe don't just change it, but make a flag for bad roasts
- tracking tasting notes.   - how to keep a simple and useful loger for this project?
- tracking density - how to keep a good loger for this project?

- fill in ITBS derivitive for RT2 (RT3 algo is probably hidden, not easy)]
- potentially skip 2 calculus steps above and move on with data exploration and results
- - report out on bean probe correlation (charge, TP, yellow, FC, drop) 
- - effect on preheat (drumChargeTemperature) and events (TP, yellow, FC)
- - limited estimates from weight loss and acknowledged challenges
- set future colors to deuteranomaly friendly palettes (avoid red+green)