import os
from processo_de_migracao_CRUD import download_pipefy_file, upload_attachment_pipefy, delete_pipefy_files
folderpath=fr'{os.getcwd()}\app\scripts\upload_attachmet_pipefy\downloads'

def validator_pdf_type(value, field_id_f, card_id):
    if 'https:' in value:
        print('--Baixando anexos--')
        __ = value.replace('["','').replace('"]','').split(',')
        if value != '[]' and value != '' and value != ['']:
            delete_pipefy_files(folderpath)
            for link in __:
                link = link.replace('"','').strip()
                donwlaod_pipefy_file(folderpath, link)
            filenames = os.listdir(folderpath)
            print(f'Deveria ter {len(__)} e tem {len(filenames)} downloads.')
            upload_attachment_pipefy(field_id_f, filenames, folderpath, card_id)
            delete_pipefy_files(folderpath)
        return True
    else:
        return False