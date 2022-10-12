import pandas as pd
import subprocess
import json
import os
import sys

DIR = r'C:\Users\fpatr\PycharmProjects\GitHub\data\outputs\clones'
ROOT_DIR = sys.path[1]
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))


def compute_size(rootdir):
    data_csv = pd.DataFrame()
    project_name = []
    num_file = []
    project_size = []
    for file in os.listdir(rootdir):
        d = os.path.join(rootdir, file)
        if os.path.isdir(d):
            print(d)
            command = "cloc {} --json".format(d)
            p = subprocess.Popen(command, cwd='{}'.format(d), shell=True, stdout=subprocess.PIPE)
            retval = p.wait()
            (out, err) = p.communicate()
            if retval == 0:
                print(" Compute successfully!")
                # with open(out, encoding='utf-8', errors='ignore') as json_data:
                #     res = json.loads(json_data, strict=False)
                res = json.loads(out)
                loc = res["Python"]["code"]
                fil = res["Python"]["nFiles"]
                num_file.append(fil)
                project_name.append(file)
                project_size.append(loc)
                print(file)
                print("total line of code {}".format(loc))
            else:
                print(" Error computing!")
                print(err)
    data_csv['project_name'] = project_name
    data_csv['number_file'] = num_file
    data_csv['LOC'] = project_size
    data_csv.to_csv(PROJECT_DIR + 'project_size2.csv', mode='w', index=False, header=True)


if __name__ == '__main__':
    compute_size(DIR)
