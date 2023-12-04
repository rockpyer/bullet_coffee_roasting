# bullet-roasting
For ingesting, transforming, displaying, and analyzing [Allio Bullet coffee roasting data](https://aillio.com/?page_id=23112).

<<<<<<< HEAD
Notebook: BulletRoastingAnalysisNotebook.ipynb
Stand alone load file: bulletPy_load.py

current state targeted for personal use, interested in expanding functionality with others. Please contact to collaborate
=======
- Data is extracted from .json roast files and cleaned up
- Enhanced point data features are created by calculating key events, times and ratios such as Turning Point, Yellowing Point, Yellowing Phase, etc...
- A Environment Variable Key for OpenAI is needed to determine Origin countried from the roastname

- Assumptions: All phase and key point temps are IBTS (drum) temps unless specifically noted. Turning point can only be calculated from beanTemp but the same index time is used to find the ibtsTemp at the time. 

Current state targeted for personal use due to several cleanup functions that cater my own practices, issues, and needs, however I'm interested in expanding functionality with others. Contact me anytime to make requests or collaborate
>>>>>>> 7ee3a754c9df0956422db5c37c78e7393d08467b

*Note: If your RoastTime isn't installed in the default MacOS location, edit 'base_path' (lines ~18-19)*

*Built for my bullet (hardware version) purchased in July 2020 - noteworthy because the data structure of the .json files have changed over time which requires some merges or gap fixes.*


![roasting data scatter plot](images/bulletRoastingEDA.png)


![roasting data with itbs ror](images/allRoastsPlt.png)


