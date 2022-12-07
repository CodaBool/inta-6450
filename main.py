import os
import json
# import pandas as pd
from pathlib import Path

append_tasks = True
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
    if append_tasks:
      obj['tasks'] = []
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
      print("       ", len(obj['tasks']), 'tasks')
    obj['findings'] = app['assessment']['report']['findings']
    print("       ", len(obj['findings']), 'findings')
    outlist.append(obj)
      
  json_obj = json.dumps(outlist, indent=2)
  with open(out_dir + file_name[:8]  + "-format.json", "w") as outfile:
    outfile.write(json_obj)