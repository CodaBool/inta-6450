import os
import json
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

path = "./data"
out_dir = "./results/"
dir_list = os.listdir(path)
main_output = []
list_of_relevant_findings = [
  'zip_file_in_transit_check_broken_ssl',
  'broken_ssl',
  'sensitive_data_cert_validation',
  'sensitive_data_http_bluetooth_mac',
  'leaked_data_in_files_bluetooth_mac',
  'leaked_logcat_data_bluetooth_mac',
  'leaked_logcat_data_build_fingerprint', 
  'leaked_logcat_data_android_id',
  'leaked_logcat_data_dns1',
  'sensitive_data_http_custom',
  'api_excessive_data_exposure',
  'sqlcipher_key_leakage_check',
  'potential_sqlcipher_key_leakage_check',
  'api_resource_misconfiguration',
  'writable_executable_files_private_check',
  'writable_executable_files_check',
]

for file_name in os.listdir(path):
  print("==>", file_name)

  # Read JSON file
  try:
    doc = json.load(open(path + "/" + file_name, encoding='utf-8'))
  except json.JSONDecodeError as e:
    print(e) 
  output = [] 
  for app in doc:
    print("     ", app['title'])
    obj = {
      'title': app['title'],
      'file': file_name,
      'publisher': app['assessment']['publisherName'],
      'score': app['assessment']['report']['score']
    }

    # Check if the app is a game
    is_game = False
    if ('game' in obj['publisher'].lower() or
        'game' in app['title'].lower() or
        'puzzle' in app['title'].lower() or
        'puzzle' in obj['publisher'].lower()):
      is_game = True
    obj['tasks'] = []
    permissions = None
    urls = None

    # Iterate over tasks
    for task_type, value in app['assessment']['analysis']['task'].items():
      if value is None:
        continue
      result_location = value['result']
      if task_type == 'yaapStatic':
        result_location = value['result'][0]
      for task, data in result_location.items():

        # Add Task
        task_obj = {}
        if not data:
          continue
        if type(data) == list:
          task_obj['data'] = data[0] 
        else:
          task_obj['data'] = data   
        task_obj['type'] = task_type
        task_obj['task'] = task
        obj['tasks'].append(task_obj)

        # Permissions
        if task == "myall":
          permissions = data['manifest']['print_permissions']['total']
        # Urls
        if task == "yaap_data":
          urls = data['urls']['info']['urls']['data']

    # Permissions
    if permissions:
      print("       ", permissions, 'permissions')
      obj['permissions'] = permissions
    if urls:
      print("       ", len(urls), 'urls')
      obj['urls'] = len(urls)

    # Game
    obj['game'] = is_game
    if is_game:
      print("        is a game")
    else:
      print("        is not a game")

    print("       ", obj['score'], 'score')
    obj['findings'] = app['assessment']['report']['findings']

    # Find specific findings
    print("        vulnerabilites")
    obj['targets'] = []
    for find in app['assessment']['report']['findings']:
      for check in list_of_relevant_findings:
        if check == find['checkId'] and find['affected']:
          print("         -", check)
          obj['targets'].append(check)
      
    output.append(obj)

  # Trim irrelevant output
  for app in output:
    del app['tasks']
    del app['findings']
    main_output.append(app)
      
# Write to JSON
json_obj = json.dumps(main_output, indent=2)
with open(out_dir + "main.json", "w") as outfile:
  outfile.write(json_obj)

# Load into Pandas
df = pd.read_json(json_obj)

# Write to CSV
df.to_csv(out_dir + 'main.csv', encoding='utf-8', index=False)

# correlation
print("correlation between urls & security", df['score'].corr(df['urls']))
print("correlation between permissions & security", df['score'].corr(df['permissions']))
print("correlation between being a game & security", df['score'].corr(df['game']))

# positive means when one goes up the other does too
# negative means when one goes down the other goes up
#  0 - .2 very weak
# .2 - .4 weak

# scatter graph urls
plt.rcParams.update({'figure.figsize':(10,8), 'figure.dpi':100})
sns.lmplot(x='urls', y='score', data=df)
plt.title("Are apps that have more URL Requests less secure?");
plt.show()

# scatter graph permissions
plt.rcParams.update({'figure.figsize':(10,8), 'figure.dpi':100})
sns.lmplot(x='permissions', y='score', data=df)
plt.title("Are apps that have more permissions less secure?");
plt.show()

# scatter graph game
plt.rcParams.update({'figure.figsize':(10,8), 'figure.dpi':100})
sns.lmplot(x='game', y='score', data=df)
plt.title("Are games less secure?");
plt.show()