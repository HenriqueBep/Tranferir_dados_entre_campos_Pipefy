from graphQl import queryGraphQL
from get_all_cards import get_all_cards
import pandas as pd
from validators import validator_pdf_type

def update_field(card_id:int, field_id:str, value):
    
    query = {'query':f'''mutation {{
                                    updateCardField(input: {{card_id: {card_id}, field_id: "{field_id}", new_value: ["{value}"]}}){{
                                        clientMutationId
                                        success
                                        }}
                                    }}'''
            }
    return queryGraphQL(query)

def get_fields_value(card_id):
    query = {'query':f'''{{
                                card(id:{card_id}){{
                                    fields{{
                                    name
                                    value
                                    field{{
                                    id
                                    }}
                                    }}
                                }}
                        }}'''}
    return queryGraphQL(query)


def field_transfer(pipe_id_o, field_id_o, field_id_f, subscribe, process:int, model):
    print('Começando field transfer')
    cards_o = get_all_cards(pipe_id_o)
    if len(cards_o) != 0:
        ii=0
        for card_id in cards_o.ID_CARDS:
            log=''
            data = get_fields_value(card_id)
            df = pd.DataFrame(data['data']['card']['fields'])
            if len(df) !=0:
                field_ids=[]
                for i in df['field'].values:
                    try:
                        field_ids.append(i['id'])
                    except:
                        field_ids.append('')
                try:
                    value = df['value'][field_ids.index(field_id_o)]
                    if subscribe == 'Não':
                        if (field_id_f in field_ids) == False:
                            if validator_pdf_type(value, field_id_f, card_id) == False:
                                    response = update_field(card_id, field_id_f, value)
                                    log=f'Alterado card.' # -- log --
                        elif df['value'][field_ids.index(field_id_f)] == '' or df['value'][field_ids.index(field_id_f)] == '[]' or df['value'][field_ids.index(field_id_f)] == []:
                                if validator_pdf_type(value, field_id_f, card_id) == False:
                                    response = update_field(card_id, field_id_f, value)
                                    log=f'Alterado card.' # -- log --
                        else:
                            log=f'Não alterado card, já existe valores no campo.' # -- log --
                    else:
                        if validator_pdf_type(value, field_id_f, card_id) == False:
                            response = update_field(card_id, field_id_f, value)
                            log=f'Alterado card.' # -- log --
                except:
                    log= f'Sem valor do campo "{field_id_o}"' # -- log --

            ii +=1
            model.objects.filter(process=process).update(doing=ii)
    else:
        log = f'Sem cards no pipe {pipe_id_o}' # -- log --
