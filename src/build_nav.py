
import os
import json
import yaml
from collections import OrderedDict




def buildNav():

    dirname = os.path.dirname(__file__)

    settings_file = os.path.join(dirname, '../templates/mkdocs.yml')
    settings = open(settings_file)

    yaml_def = yaml.full_load(settings)
    settings.close()

    doc_dir = os.path.join(dirname,'../docs/qlik')


    doc_list = {}
    root_items = {}
    qlik_items = {}
    qrs_items = {}

    for root, dirs, files in os.walk(doc_dir):
        
        for f in files:

            path = os.path.join(root,f).replace(doc_dir+'/','')


            page = {}
            if '/' not in path:
                if path[0] != '.':
                    root_items[path.replace('.md','')] ='qlik/'+path

            elif 'qrs' in path:
                path_parts = path.split('/')

                if len(path_parts) == 2:
                    qrs_items['_qrs'] = [{path[path.rfind('/')+1:len(path)-3]:'qlik/'+path}]
                
                else:
                    folder = path_parts[1]

                    if folder not in qrs_items:
                        qrs_items[folder]=[]
                    
                    qrs_items[folder].append({path[path.rfind('/')+1:len(path)-3]:'qlik/'+path})
            
            else:
                path_parts = path.split('/')
                folder = path_parts[0]
                if folder not in qlik_items:
                    qlik_items[folder]=[]
                
                qlik_items[folder].append({path[path.rfind('/')+1:len(path)-3]:'qlik/'+path})



    qrs_items = OrderedDict(sorted(qrs_items.items()))


    for l in qrs_items:
        qrs_items[l] = sorted(qrs_items[l], key=lambda d: list(d.keys()))


    qrs_items = {"qrs" if k=="_qrs" else k:v for k,v in qrs_items.items()}
    qrs_items['qrs'] = qrs_items['qrs'][0]['qrs']

    for l in qlik_items:
        qlik_items[l] = sorted(qlik_items[l], key=lambda d: list(d.keys()))

    qlik_items = OrderedDict(sorted(qlik_items.items()))
    qlik_items = dict(qlik_items)
    qlik_items['qrs'] = qrs_items

    root_items = OrderedDict(sorted(root_items.items()))
    nav = {}
    for k,v in root_items.items():
        nav[k] = v

    for k,v in qlik_items.items():
        nav[k] = v

    qlik_nav = {'Qlik CLI Reference': nav}

    for y in range(len(yaml_def['nav'])):
        if 'Qlik CLI Reference' in yaml_def['nav'][y]:
            yaml_def['nav'][y] = qlik_nav


    with open(os.path.join(dirname,'../mkdocs.yml'), 'w') as s:

        yaml.safe_dump(yaml_def, s, indent=2, default_flow_style=True,default_style='\'',width=float("inf"),sort_keys=False)
            

