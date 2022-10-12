import pandas as pd
import json
import urllib.request
import random
import time
import os
import Get_repo

PATH = './data/'


class GitMeta:
    def __init__(self, repo, ct):

        self.ct = ct
        self.repo = repo

    def get_repo_contributors(self):
        contributors = []
        p = 1
        while True:
            url2 = 'https://api.github.com/repos/' + self.repo + '/contributors?page=' + str(p) + '&per_page=100'
            contributors_arrays, self.ct = Get_repo.GitHub(url2, self.ct).getResponse()
            p += 1
            if contributors_arrays != None:
                if p == 5:
                    break
                if len(contributors_arrays) == 0:
                    break
                contributors += contributors_arrays
            else:
                break
            time.sleep(60)
        return len(contributors), self.ct

    def get_commits(self):
        commits = []
        p = 1
        while True:
            url2 = 'https://api.github.com/repos/' + self.repo + '/commits?page=' + str(p) + '&per_page=100&state=all'
            commits_arrays, self.ct = Get_repo.GitHub(url2, self.ct).getResponse()
            p += 1
            if commits_arrays != None:
                if p == 5:
                    break
                if len(commits_arrays) == 0:
                    break
                commits += commits_arrays
            else:
                break
            time.sleep(60)
        return len(commits), self.ct

    def get_repo_desc(self):
        repos = []
        # p = 1

        # while True:

        url2 = 'https://api.github.com/repos/' + self.repo
        repos, self.ct = Get_repo.GitHub(url2, self.ct).getResponse()
        # if repos_arrays != None:
        #     if p == 1:
        #         repos.append(repos_arrays)
        #         return repos, self.ct
        #     else:
        #         break
        # else:
        #     break
        # p += 1
        time.sleep(60)
        return repos, self.ct


def read_csv(file):
    df = pd.read_csv(file)
    data = df.iloc[:, 0]
    repo_nam_column = data.drop_duplicates()
    print("Total value of repo :", len(repo_nam_column))
    return repo_nam_column


if __name__ == '__main__':
    ct = 0
    cp = 0
    data_csv = pd.DataFrame()
    repo_nam = []
    star_repo = []
    fork_repo = []
    contribut_repo = []
    commit_repo = []
    # cnt = 1
    # for file in os.listdir("./data/"):
    #     if file.endswith(".csv"):
    #         print(os.path.join("./data/", file))
    repo_name = read_csv("./data/my_data_final.csv")

    for rep_ in repo_name:
        cp += 1
        print("repo number :", cp)
        contribut, ct = GitMeta(rep_, ct).get_repo_contributors()
        print("repo name :", rep_)
        print("number of contributors", contribut)
        comit, ct = GitMeta(rep_, ct).get_commits()
        print("number of commit", comit)
        try:
            rep, ct = GitMeta(rep_, ct).get_repo_desc()
            print("number of stars", rep["stargazers_count"])
            number_stars = rep["stargazers_count"]
            number_fork = rep["forks_count"]
            print("number of forks:", number_fork)
        except Exception as e:
            print(e)
            continue
        repo_nam.append(rep["full_name"])
        star_repo.append(number_stars)
        fork_repo.append(number_fork)
        contribut_repo.append(contribut)
        commit_repo.append(comit)
        # if cp == 1537:
        #     break
    data_csv['repo_name'] = repo_nam
    data_csv['number_star'] = star_repo
    data_csv['number_fork'] = fork_repo
    data_csv['number_contribution'] = contribut_repo
    data_csv['number_commit'] = commit_repo
    data_csv.to_csv(PATH + 'my_data_characteristic.csv', mode='a', index=False, header=False)


        # cnt += 1
        # if cnt == 2:
        #     break

