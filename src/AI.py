# %%
# This script uses OpenAI to identify the country of origin from the roastName
import os
from openai import OpenAI
import json
#previously using the OAI key ending 'dm0k2'
#now using key ending M6I9A

## Set the API key and model name
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

#OAI_model = "gpt-3.5-turbo" # currently stuck on this model under a the Free Tier until I spend more $$
OAI_model = "gpt-4o" 
def get_origin(roast_name):
  completion = client.chat.completions.create(
      model=OAI_model,
      response_format={ "type": "json_object" },
      messages=[
        {
          "role": "system",
          "content": "You will be passed data from coffee roasting logs.\n\
                Your job is to identify the country (Origin) in the roastName. \n\
                Sometimes a region or abreviation will be named, but you need to report the proper name of the country. \n\
                Return a JSON with roastName, Origin. \n\
                If there is no country return roastName, 'None' "
        },
        {
          "role": "user",
          "content": roast_name
        }
        ],
      seed=42, #using seed to get consistent results but this takes a lot longer to run (2.5 secs with vs 0.8 w/out)
      max_tokens=70, # Using <20 certainly threw errors, also a few at 30 
      temperature=0.5,
      top_p=1,
      frequency_penalty=0,
      presence_penalty=0
    )
  
  # .loads converts string to dict, .get returns value of key "Origin" or None if not present
  originName = json.loads(completion.choices[0].message.content).get("Origin", None) 
  #print (roast_name, originName)
  return (originName)

# %%
