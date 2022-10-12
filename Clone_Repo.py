import pandas as pd
import os
import subprocess

PATH = './data/final_data.csv'
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))


def clone_repository(url, target_path):
    os.chdir(target_path)
    git_clone_command = "git clone " + url
    print("git clone {} ...".format(url))
    p = subprocess.Popen(git_clone_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    output = ""
    for line in p.stdout.readlines():
        output = output + str(line) + '\n'
    retval = p.wait()
    if retval == 0:
        print(" Repository cloned successfully!")
    else:
        print(" Error in cloning!")
        print(output)
    return retval


def main():
    repo_target_path_root = ROOT_DIR + "/data/outputs/clones"
    df_topic = pd.read_csv(ROOT_DIR + '/data/final_data.csv')
    repo_name = df_topic["repo_name"].tolist()
    if not os.path.exists(ROOT_DIR+'/data/outputs'):
        os.makedirs(ROOT_DIR+'/data/outputs')
    if not os.path.exists(ROOT_DIR+'/data/outputs/clones'):
        os.mkdir(ROOT_DIR+'/data/outputs/clones')
    for index in range(len(repo_name)):
        repo = repo_name[index]
        print(index,repo)
        repository_url = "https://github.com/" + repo + ".git"
        clone_repository(repository_url, repo_target_path_root)


if __name__ == '__main__':
    main()