"""TODO(hoivan): DO NOT SUBMIT without one-line documentation for get_labels.
# Two things to run this script
# 1. run "pip install graphqlclient"
# 2. Fill in <API-KEY-HERE> (https://app.labelbox.com/settings/apikey)
"""
import json
import time
import numpy as np
import io
import urllib.request, json
from PIL import Image
from keras.preprocessing.image import load_img

from graphqlclient import GraphQLClient
client = GraphQLClient('https://api.labelbox.com/graphql')
client.inject_token('Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VySWQiOiJjanNpaXV3cXkxdWxwMDcyODdhb2kxeHl3Iiwib3JnYW5pemF0aW9uSWQiOiJjanNpaXV3cWgxdWxqMDcyOGhqcXBxZXZ2IiwiYXBpS2V5SWQiOiJjanNsY3ludjl2dWtwMDcyOHR1YTVnZnIzIiwiaWF0IjoxNTUxMTYwNTg1LCJleHAiOjIxODIzMTI1ODV9.xJQLaWQL_d70Vpq_rsZrg3hAwidi4OlfVJJU1PqPCrs')

def get_export_url(project_id):
    res_str = client.execute("""
    mutation GetExportUrl($project_id: ID!){
      exportLabels(data:{
        projectId: $project_id
      }){
        downloadUrl
        createdAt
        shouldPoll
      }
    }
    """, {'project_id': project_id})
    res = json.loads(res_str)
    return res['data']['exportLabels']

def get_project_labels(project_id):
  export_job = get_export_url(project_id)
  if (export_job['shouldPoll']):
    print('Export Generating...')
    time.sleep(3)
    return get_project_labels(project_id)

  with urllib.request.urlopen(export_job['downloadUrl']) as url:
      labels = json.loads(url.read().decode())
      with open(str(project_id) + '.json', 'w') as outfile:
        json.dump(labels, outfile, sort_keys = True, indent = 4, ensure_ascii = False)
      return labels

def get_projects():
    res_str = client.execute("""
    query GetAProjectFromOrganization {
      projects {
        id
        name
      }
    }
    """)

    res = json.loads(res_str)
    return res['data']['projects']

def extract_bumper_data_from_json(labels):
  images = []
  boxes = []
  n = 0
  print(len(labels))
  for i in range(len(labels)):

    if "Bumper" in labels[i]["Label"]:
      images.append(labels[i]["Labeled Data"])
      boxes.append(np.empty(len(labels[i]['Label']['Bumper'])*5, dtype='float32'))
      for j,box in enumerate(labels[i]["Label"]["Bumper"]):
        #box = labels[i]["Label"]["Bumper"][0]
        y0 = box["geometry"][0]["y"]
        x0 = box["geometry"][0]["x"]
        y2 = box["geometry"][2]["y"]
        x2 = box["geometry"][2]["x"]
        xmin = min(x0,x2) * (min(x0,x2) > 0)
        ymin = min(y0,y2) * (min(y0,y2) > 0)
        xmax = max(x0,x2)
        ymax = max(y0,y2)
        boxes[n][j*5] = 0 # 0 corresponds to bumper class
        boxes[n][j*5+1] = xmin
        boxes[n][j*5+2] = ymin
        boxes[n][j*5+3] = xmax
        boxes[n][j*5+4] = ymax
      print(boxes[n])
      #print(boxes[n].reshape((-1,5)))
      n+=1
  data = {"images": images, "boxes": boxes}
  return data

if __name__ == "__main__":
  project_id = get_projects()[0]['id']
  labels = get_project_labels(project_id)
  #print(labels)
  data = extract_bumper_data_from_json(labels)
  with open(str(project_id) + '.npz', 'wb') as outfile:
    np.save(outfile, data)
