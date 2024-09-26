import requests
import pandas as pd

def get_all_cards(pipe_id):
    url = "https://api.pipefy.com/graphql"
    
    token = ''
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "authorization": f"Bearer {token}"
    }
    
    query = {'query':f'''
                query{{pipe(id:{pipe_id}){{
                phases{{
                id
                name
                            }}
                        }}
                    }}
            '''}
    response = requests.post(url, json=query, headers=headers)
    data = response.json()
    try:
        phases = pd.DataFrame(data['data']['pipe']['phases'])
        id_cards=[]
        phase_cards=[]
        for phase in phases.id.values:
            after=''
            while True:
                query = {'query':f'''query{{
                            phase(id:{phase}){{
                                cards(first:100{after}){{
                                pageInfo{{
                                    endCursor
                                    hasNextPage
                                }}
                                        nodes{{
                                            id
                                        }}
                                    }}
                                }}
                            }}
                        '''}
                response = requests.post(url, json=query, headers=headers)
                data = response.json()
                for _ in data['data']['phase']['cards']['nodes']:
                    id_cards.append(_['id'])
                    phase_cards.append(phase)

                #print('processando fase:',phase)
                
                if data['data']['phase']['cards']['pageInfo']['hasNextPage'] == True:
                    end = data['data']['phase']['cards']['pageInfo']['endCursor']
                    after=f',after:"{end}"'
                else:
                    break
        df1=pd.DataFrame({'ID_CARDS':id_cards,'PHASE_CARDS':phase_cards})
        total_cards = pd.merge(df1,phases, left_on='PHASE_CARDS',right_on='id',how='left').drop(columns=['PHASE_CARDS','id'])
        return total_cards
    except:
        return []







