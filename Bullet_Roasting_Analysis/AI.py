# %%
# This script uses GPT-3.5 to identify the country of origin from the roastName
import os
import openai
import pandas as pd
import json
from dotenv import load_dotenv

#openai.api_key = api_key
#openai.api_key = os.getenv("OPENAI_API_KEY")
#openai.api_key = os.environ['OPENAI_API_KEY'] 
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
#api_key = os.environ.get('OPENAI_API_KEY')
if api_key:
  openai.api_key = api_key
  print(r'OPENAI_API_KEY good to go')
else:
  print (api_key)
  print("OPENAI_API_KEY not set")
  openai.api_key = "** Something is not right **"
  
  
#load point_df.csv from csvExports folder as point_df
#point_df = pd.read_csv('../csvExports/point_df.csv')

def get_origin(roast_name):
    response = openai.ChatCompletion.create(
      model="gpt-3.5-turbo",
      messages=[
        {
          "role": "system",
          "content": "You will be passed data from coffee roasting logs.\n\
                Your job is to identify the country (Origin) in the roastName. \n\
                Sometimes a region or abreviation will be named, but you need to report the proper name of the country. \n\
                Return the results in a dictionary with roastName, Origin"
        },
        {
          "role": "user",
          "content": roast_name
        }
      ],
      temperature=0.1,
      max_tokens=960,
      top_p=0.77,
      frequency_penalty=0,
      presence_penalty=0
    )
    content = response.choices[0].message['content']
    origin = json.loads(content)['Origin']
    return origin


# new_df = pd.DataFrame()
# new_df['Origin'] = point_df['roastName'].apply(get_origin)



# # Display the DataFrame with thSe 'roastName' and 'Origin' columns
# display(point_df[['roastName', 'Origin']])

# # %%
# import plotly.express as px
# #count the number of roasts per origin
# origin_count = point_df['Origin'].value_counts()

# #Plot a bar chart of the number of roasts per origin in plotly
# fig = px.bar(origin_count, x=origin_count.index, y=origin_count.values, title="Number of Roasts per Origin")
# #include the total number of roasts in the title
# fig.update_layout(title_text="Number of Roasts per Origin (Total Roasts: " + str(len(point_df)) + ")")
# # make the y axis say "Number of Roasts" and x-axis say "Country of Origin"
# fig.update_layout(yaxis_title="Number of Roasts", xaxis_title="Country of Origin")
# fig.show()

# # %%
# # plot the number of roasts per origin in plotly as above in a really interesting sunburst chart
# fig = px.sunburst(origin_count, path=origin_count.index, values=origin_count.values, title="Number of Roasts per Origin")
# fig.update_layout(title_text="Number of Roasts per Origin (Total Roasts: " + str(len(point_df)) + ")")
# fig.show()


# %%
