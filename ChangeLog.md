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
- 1/29/23 - Updates the github after the Australia Day BBQ. moved files and completed the refresh of the 'BulletRoastingAnalysisNotebook'.  Need to simplifly some names and break apart the notebook.
- 06/01/23 - varied work in modularizing the notebook, cleaning up functions and doing a little more 2nd D work
- 7/1/23 - NLP for origins, using SpaCy, FuzzyWuzzy, and pycountry.   got pretty bad results in 2 trys,  will try to limit the options to a list of coffee countries. 
- 7/2/23 - Third try with limited list of coffee producting countries and still bad results on 1/3 of roastNames.  half because I used slang or abreviations like Guat, Guate, PNG, 1/4 because of spelling errors like Columbia (Colombia), and 1/4 actually have Kenya or Ethiopia and its just not working.
- 9/2/23 - Used openAI api to read the roastName and respond witht the country.
  - Seemed to work like a charm and i get great results but then recalling the API key set in my environment starting causing me grief
 - 9/10/23 - Added phases durations (time) and temps, Added ROR-est values for each phase (plan as ML feature), Added peakROR Time and Temp as moving averages over 25 seconds (eyeball estimate). Also cleaned up the README and some other bits in main.py
   - ERRORS to deal with: ***
     - api_key = os.environ.get('OPENAI_API_KEY') - won't get it in my environment
     - also found-
       - TypeError: unsupported operand type(s) for -: 'int' and 'str'
- 10/2/23 + found successive errors after that type error in the data processing reformat with the addition of new phases and ROR vals
- 10/17/23  - worked through all the errors in new phase and time calcs.
  - Fix more errors. Currently I find that I'm making many decisions to drop columns that I'm not interested in but need to figure out if I should still be including in a very simple way.
  - also Allio added a few new columns that i'm dropping some in drop_intermediate_columns() in the data_processing.py file but it could be interesting to look at
  - I feel that this phase is complete and I can probably return to tableau and make the phase and ROR charts! YAY
  - Need to visually QC all the new calcs

11/5/23 - 
  - flying home from Porto, I found there were many issues with the data 
    - Seems like we don’t have:
      - beanTurningPtTemp - only IBTSTPTemp… why
          - I have index turning point, I need the temp at that value, maybe that’s messing with some of the RORs and phases
      - PeakROR
          - Empty everywhere
      - DevelopmentTime   -  Is not development Phase Time… numbers are very high  500-650+, not quite seconds or half seconds of the phase (I’d expect more at 1.5-2 mins
          - I couldn’t get ChatGPT to do that for me:
              - For each unique Roast Name the new calculated phase needs to be: Point time for Point Phase DevTime] = [Point Time: Point Phase, totalRoastTime] - [Point Time: Point Phase, firstCrackTime]
  - I fix the openAI API .env issue. should load correctly as long as you have OPENAI_API_KEY="YOU KEY" in your .env file
  - Fixed occasional missed Turning point because I had a filter to only include minBT when the derivative was >0
  - Next, 
    -  28  firstCrackTemp         1 non-null      float64
          -  related to dropping indexFirstCrackStart in data_cleanup?
    -  33  peakRoR                0 non-null      float64
    -  39  browiningPhaseTime     0 non-null      float64
    -  43  RoR-browning-est       0 non-null      float64
    -  14  Drop-ChargeDeltaTemp   0 non-null      float64




ADDITIONAL NOTES:

- Future: Also might need to try and look up the beanId ex: "beanId": "9e7d2b7e-1f51-4baf-bc3c-5b061d91acd8"  from roast.world
- Maybe scrape roast.world... check out third AI scraper


## NEXT - calculate phases and DTR
## Next - use framework in clean up to get rid of more columns and junk
- why is weight loss % not working
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
 
