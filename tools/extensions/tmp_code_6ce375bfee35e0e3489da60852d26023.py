
from serpapi import GoogleSearch

queries = [
    "Rita Coolidge sang the title song for which Bond film?",
    "What was the last US state to reintroduce alcohol after prohibition?",
    "Which actress was voted Miss Greenwich Village in 1942?",
    "What was the name of Michael Jackson's autobiography written in 1988?",
    "In which decade did stereo records first go on sale?"
]

api_key = "98c2d9f0994ffaa96e660dbe908c35288312c63c3e6a7f4cda7798669ee688b6"

for query in queries:
    params = {
        "q": query,
        "api_key": api_key
    }

    search = GoogleSearch(params)
    results = search.get_dict()

    organic_results = results.get("organic_results", [])[:1]
    print(f"Results for '{query}':", organic_results)
