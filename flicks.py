# import requests
# import json

# headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer {0}'.format(api_key)}
# api_key = "76b7eb9d74b21ff2bf120a4499967ac6"
# api_url_base = "https://api.themoviedb.org/3/search/movie?api_key="



# def get_flicks():
#     # api_url = 'api_url_base{0}'.format(api_key)
#     response = requests.get("https://api.themoviedb.org/3/trending/all/day?api_key=76b7eb9d74b21ff2bf120a4499967ac6")
#     if response.status_code == 200:
#         return json.loads(response.content.decode('utf-8'))
#     else:
#         return None