# Copyright (C) 2024 Xiaomi Corporation.
# Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at
# http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.



data_prompt = '''
[Task description]:{task_description}
[Examples]:{examples}
[Sampled APP list]:{app_list}
[Sampled API list]:{api_list}
[Other requirements]:{requirement}'''

multiapp_requirement = '''
Please produce ten queries in line with the given requirements and inputs. These ten queries should display a diverse range of sentence structures: 
some queries should be in the form of imperative sentences, others declarative, and yet others interrogative. 
Equally, they should encompass a variety of tones, with some being polite, others straightforward. Ensure they vary in length and contain a wide range of subjects: 
myself, my friends, family, and company. 
Keep in mind that for each query, invoking just one APP won’t suffice; each query should call upon two to five APPs.
Aim to include a number of engaging queries as long as they relate to APP calls. 
However, try to avoid explicitly specifying which APP to employ in the query. Each query should consist of a minimum of twenty words.
'''

'''For instance, if the APP ‘Traveloka’ has function description: 
'Get exclusive travel deals and enjoy the award-winning customer service! Traveloka app is your one-stop travel platform! Book with us for great deals on:
    Flights: International and domestic flights at great rates
    Hotels: Choose from over 1.2million hotels, resorts, and apartments around the world
    Trains: Book tickets for United Kingdom, Germany, Italy, Spain, France, Switzerland, South Korea, and more.'
Your query should articulate something akin to: 'I am going on a business trip to Xiaomi Technology Park in Beijing this Friday. 
Please help me check the suitable air tickets and train tickets, and then help me check the following hotels closest to there.'
This query exemplifies how to take advantage of all of the ‘Traveloka’ app features. '''

multiapp_description = '''
You will be provided with an available APP list with descriptions, an available API list including ADB Command, Function Description and Parameter Information.
Your task involves creating 10 varied, innovative, and detailed user queries that employ multiple APPs of a tool, API can be used as an auxiliary to provide basic functions.

Additionally, you must incorporate the input parameters required for each call. 
Generate random information for required parameters such as IP address, location, coordinates, etc. 
For instance, don’t merely say ‘an address’, provide the exact road and district names. 
Don’t just mention ‘a product’, specify wearables, milk, a blue blanket, a pan, etc. 
Don’t refer to ‘my home’, use a name of a real place. 

The first seven of the ten queries should be very specific. 
Each single query should combine at least two APPs in different ways and include the necessary parameters. 
Note that you shouldn’t ask ‘which APP to use’, rather, simply state your needs that can be addressed by these APPs. 
You should also avoid asking for the input parameters required by the APP call, but instead directly provide the parameter in your query.
The final three queries should be complex and lengthy, describing a complicated scenario where all the APPs can be utilized to provide assistance within a single query. 

You should first think about possible related APP combinations, then give your query.
The final queries should be complex and lengthy, describing a complicated scenario where all the APP calls can be utilized to provide assistance within these queries. 
You should first think about possible related APP and API combinations, then give your query. Related APP and apis can be used for a give query; 
those Related APP and apis have to strictly come from the provided lists. For different queries, overlap of related APPs should be as little as possible. 
Deliver your response in this format: 
[Query1: ......, ‘related APPs’:[api1, api2, api3...],Query2: ......, ‘related APPs’:[api4, api5, api6...],Query3: ......, ‘related APPs’:[api1, api7, api9...], ...]
'''

multiapp_examples = '''
“Query”: “My fiancée and I are about to go to California for our honeymoon. The travel time is not important, but you need to recommend a suitable hotel to me. At least you need to tell me about the swimming pool, restaurant, Wifi, and elevators. As far as I know, there are many suitable hotels in California. For travel activities, please make a simple arrangement for us, including where you need to go every day, how much it costs, and how long you can travel for.”, 
“related APPs”: [’Traveloka’, ‘Google Search’, ‘Maps’, ‘Weather’] 
“Query”: “Who is Trump? Can you tell me about his life? As far as I know, he likes to participate in public welfare undertakings. Are there any recent news reports about his participation in public welfare activities? tell me the details.”, 
“related APPs”: [’BBC News’, ‘Wikipedia’] 
'''

sample_apiapp = '''

'''
