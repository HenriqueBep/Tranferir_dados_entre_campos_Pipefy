import os
import requests

def download_pipefy_file(filepath, url):
    os.makedirs(filepath, exist_ok=True)
    name = url
    # Nome do arquivo para salvar
    name = name[name.find('uploads/')+9:]
    name = name[name.find('/')+1:name.find('?')]

    local_filename = os.path.join(filepath, name)

    # Faz a requisição HTTP ao link do anexo
    r = requests.get(url, stream=True)
    r.raise_for_status()
    # Abre um arquivo local para salvar o conteúdo baixado
    with open(local_filename , 'wb') as f:
        print(f)
        for chunk in r.iter_content(chunk_size=8192):
            f.write(chunk)
    
    return name

def upload_attachment_pipefy(pipefy_field, filenames, filepath, ids2):

    treated_link = []
    for filename in filenames:
        # step one
        token = ''

        headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "authorization": f"Bearer {token}"
        }

        url = "https://api.pipefy.com/graphql"


        payload = {'query':f'''
                            mutation{{
                                        createPresignedUrl(input: {{ organizationId: ##, fileName: "{filename}" }}){{
                                            clientMutationId
                                            url
                                        }}
                                    }}
                        '''
                }
        response = requests.post(url, json=payload, headers=headers)

        response_url = response.json()['data']['createPresignedUrl']['url']
        filepath_file = filepath+f'/{filename}'
        
        # step two
        with open(filepath_file, 'rb') as file_open:
            payload = file_open.read()
        headers = {
        'Content-Type': 'text/plain'
        }

        response = requests.put(response_url, data=payload, headers=headers)
        contador = 1
        while True:
            l = filename[len(filename)-contador:len(filename)]
            if l[:1] == '.':
                break
            contador += 1
        filetype = l[1:]
        treated_link.append(response_url[response_url.find('orgs'):response_url.find(filetype)+len(filetype)])

    __ = []
    for _ in treated_link:
        __.append('"'+str(_)+'"')
    str(__).replace("\'",'')

    # step three
    url = "https://api.pipefy.com/graphql"
    ___ = str(__).replace("']",'').replace("['",'').replace("\'",'')
    for card_id in ids2:
        payload = {'query':f'''
                            mutation {{
                                updateCardField(input: {{card_id: {card_id}, field_id: "{pipefy_field}", new_value: [{___}]}}) {{
                                    clientMutationId
                                    success
                                    }}
                                }}
                        '''}
        token = ''
        headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "authorization": f"Bearer {token}"
        }

        response = requests.post(url, json=payload, headers=headers)
 
def delete_pipefy_files(filepath):
    try:
        arquivos = os.listdir(filepath)
        for arquivo in arquivos:
            caminho_completo = os.path.join(filepath, arquivo)
            if os.path.isfile(caminho_completo):
                os.remove(caminho_completo)
        os.rmdir(filepath)
    except Exception:
        print(Exception)
    