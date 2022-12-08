import os
import json
# import pandas as pd
from pathlib import Path

append_tasks = True
write_results = False
path = "./data"
out_dir = "./results/"
dir_list = os.listdir(path)

for file_name in os.listdir(path):
  print("==>", file_name)
  try:
    doc = json.load(open(path + "/" + file_name, encoding='utf-8'))
  except json.JSONDecodeError as e:
    print(e) 
  outlist = [] 
  for app in doc:
    print("     ", app['title'])
    obj = {}
    obj['title'] = app['title']
    assessment = app['assessment']  
    obj['publisher'] = assessment['publisherName']
    obj['platform'] = assessment['platformType']
    obj['score'] = assessment['report']['score']
    is_game = False

    # is a game
    if ('game' in obj['publisher'].lower() or
        'game' in app['title'].lower() or
        'puzzle' in app['title'].lower() or
        'puzzle' in obj['publisher'].lower()):
      is_game = True
    if append_tasks:
      obj['tasks'] = []
      permissions = None
      urls = None
      for task_type, value in assessment['analysis']['task'].items():
        if value is None:
          continue
        result_location = value['result']
        if task_type == 'yaapStatic':
          result_location = value['result'][0]
        for task, task_output in result_location.items():
          task_obj = {}
          if not task_output:
            continue
          if type(task_output) == list:
            task_obj['data'] = task_output[0] 
          else:
            task_obj['data'] = task_output   
          task_obj['type'] = task_type
          task_obj['task'] = task
          obj['tasks'].append(task_obj)

          # Permissions
          if task == "myall":
            permissions = task_output['manifest']['print_permissions']['total']
          # Urls
          if task == "yaap_data":
            urls = task_output['urls']['info']['urls']['data']

    # Permissions
    if permissions:
      print("       ", permissions, 'permissions')
    if urls:
      print("       ", len(urls), 'urls')

    # Game
    if is_game:
      print("        is a game")
    else:
      print("        is not a game")

    print("       ", obj['score'], 'score')
    obj['findings'] = app['assessment']['report']['findings']
    outlist.append(obj)
      
  if write_results:
    json_obj = json.dumps(outlist, indent=2)
    with open(out_dir + file_name[:8]  + "-format.json", "w") as outfile:
      outfile.write(json_obj)