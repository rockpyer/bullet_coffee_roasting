import asyncio
import openai
import os
import json

async def get_origin_count(roast_name, OAI_model):
    """
    Asynchronously gets origin and roast count from a given roast name using OpenAI.

    Args:
        roast_name: The name of the roast.
        OAI_model: The OpenAI model to use.

    Returns:
        A tuple containing the origin and roast count.
    """
    # client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

    async with openai.AsyncOpenAI(api_key=os.environ.get("OPENAI_API_KEY")) as client:
        completion = await client.chat.completions.create(
            model=OAI_model,
            response_format={ "type": "json_object" },
            #response_format="json_object",
            messages=[
            {
              "role": "system",
              "content": '''You will be passed data from coffee roasting logs.
                                    You have two tasks:
                    1. Identify the country (Origin) in the roastName. Sometimes a region or abreviation will be named, always report the proper country name.
                    2. Identify the roast number (roastCount) in the roastName associated with the # symbol.
                    * for example "#48 Eth Yirgacheffe 3rd" would be roastCount: 48, Origin: Ethiopia
                    If there is no country, return 'None' for Origin.
                    If there is no roast number, return roastCount, 'None' 
                    Never return multiple origins or roastCounts, pick the most likely one and return an integer value.
                    Return a JSON with roastName, Origin, and roastCount.
                    
                    ### SCHEMA
                    {
                        "roastName": "roastName",
                        "Origin": "Origin",
                        "roastCount": "roastCount"
                    }
              '''

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
              # Parse the JSON content from the completion message
    content = json.loads(completion.choices[0].message.content)
    originName = content.get("Origin", None)
    roastCount = content.get("roastCount", None)
#     originName = completion.choices[0].message.get("Origin", None)
#     roastCount = completion.choices[0].message.get("roastCount", None)
# #    originName = json.loads(completion.choices[0].message.content).get("Origin", None)
# #    roastCount = json.loads(completion.choices[0].message.content).get("roastCount", None)
  
    return (originName, roastCount)

async def process_roast_names(roast_names, OAI_model):
    """
    Asynchronously processes a list of roast names and returns a list of tuples 
    containing origin and roast count for each name.

    Args:
        roast_names: A list of roast names.
        OAI_model: The OpenAI model to use.

    Returns:
        A list of tuples, where each tuple contains the origin and roast count.
    """
    tasks = [get_origin_count(roast_name, OAI_model) for roast_name in roast_names]
    results = await asyncio.gather(*tasks)
    return results
