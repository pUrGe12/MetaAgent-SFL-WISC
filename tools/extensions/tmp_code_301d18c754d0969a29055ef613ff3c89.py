 
import json
import os
import requests

os.environ['BING_SEARCH_V7_SUBSCRIPTION_KEY']="e5ac2ebcba064af1830740a2a270fb74"
subscription_key = os.environ['BING_SEARCH_V7_SUBSCRIPTION_KEY']
endpoint = "https://api.bing.microsoft.com/v7.0/search"

queries = [
    "If I Were A Rich Man Was a big hit from which stage show?",
    "Men Against the Sea and Pitcairn's Island were two sequels to what famous novel?",
    "What was Truman Capote's last name before he was adopted by his stepfather?",
    "In Lewis Carroll's poem The Hunting of the Snark, what did the elusive, troublesome snark turn into to fool hunters?",
    "In the Bible, who did the sun and moon stand still before?"
]

headers = { 'Ocp-Apim-Subscription-Key': subscription_key }

for query in queries:
    try:
        params = { 'q': query }
        response = requests.get(endpoint, headers=headers, params=params)
        response.raise_for_status()
        print(f"Query: {query}")
        print("The search results are:")
        print(response.json()['webPages']['value'][0]['snippet'])
    except Exception as ex:
        raise ex
