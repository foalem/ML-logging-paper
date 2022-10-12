import csv
import pandas as pd
import os
import json

PATH = './data/'


def save_to_csv(data):
    repo_name = []
    fill_name = []
    file_url = []
    file_path = []
    mydata = pd.DataFrame()
    for info in data:
        try:
            repos = info['repository']['full_name']
            fill_names = info['name']
            file_urls = info['html_url']
            file_paths = info['path']
            repo_name.append(repos)
            fill_name.append(fill_names)
            file_url.append(file_urls)
            file_path.append(file_paths)
        except:
            None

    mydata['repo_names'] = repo_name
    # mydata['file_name'] = fill_name
    # mydata['file_path'] = file_path
    mydata['file_url'] = file_url
    # print(mydata)
    mydata.to_csv(PATH + 'my_data_final.csv', mode='a', index=False, header=False)
    return mydata


def read_Json(path):
    json_list = []
    with open(path) as json_file:
        jsondict = json.load(json_file)
        # for data in jsondict:
        # print(data['repository']['full_name'], data['html_url'], data['name'], data['path'])
        save_to_csv(jsondict)
    return json_list


def get_file(root_dir):
    file_set = []
    for dir_, _, files in os.walk(root_dir):
        for file_name in files:
            ext = os.path.splitext(file_name)[-1].lower()
            if ext == ".json":
                rel_file = os.path.join(dir_, file_name)
                file_set.append(rel_file)
    print(file_set)
    return file_set


if __name__ == '__main__':
    file_path = get_file(PATH)
    for file in file_path:
        read_Json(file)
    # csv_data = mydata.to_csv(PATH + 'my_data1.csv')
