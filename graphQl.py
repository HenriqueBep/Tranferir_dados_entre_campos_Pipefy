import requests
def queryGraphQL(query):
    token = ''
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "authorization": f"Bearer {token}"
    }
    url = "https://api.pipefy.com/graphql"
    response = requests.post(url, json=query, headers=headers)
    return response.json()