import pandas as pd
from Filter_repo import load_data

PATH = './data/my_data_characteristic.csv'


def select_repo_by_stars(data):
    new_data = data.loc[data['num_stars'] >= 1]
    return new_data


def select_repo_by_commit(data):
    new_data = data.loc[data['num_commit'] >= 100]
    return new_data


def select_repo_by_contributor(data):
    new_data = data.loc[data['num_contributor'] >= 2]
    return new_data


if __name__ == '__main__':
    my_data = load_data(PATH)
    my_new_data = select_repo_by_stars(my_data)
    my_new_data_ = select_repo_by_commit(my_new_data)
    final_project = select_repo_by_contributor(my_new_data_)
    print('number of repo by stars ', my_new_data.shape)
    print('number of repo by commit ', my_new_data_.shape)
    print('final number of repo', final_project.shape)
    final_project.to_csv('./data/final_data.csv', mode='w', index=False, header=True)
